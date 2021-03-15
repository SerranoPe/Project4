from typing import cast
from django.http import request
from django.http.response import *
from trader.models import Stock
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .forms import StockForm, TickerForm
from .models import Account, Stock, Transaction
from .finance import getStockData, stockPlot
from .dates import getDate
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
import json

# Create your views here.
def home(request):
    account = Account.getAccount(1)
    balance = account.balance
    username = account.username
    stocks = Stock.getStocks()
    investValue = portValue()
    context = {
        'username': username, 
        'balance': round(balance, 2), 
        'investValue': round(investValue,2),
        'stocks': stocks
        }
    return render(request, 'trader/home.html', context)

def stock(request, symbol):
    print("symbol=",symbol)
    account = Account.getAccount(1)
    balance = account.balance
    username = account.username
    startDate = getDate('year')
    endDate = getDate()
    stock = getStockData(symbol, startDate, endDate)
    count = Stock.objects.filter(symbol=symbol).count()
    if count >= 1:
        ownedStock = Stock.objects.get(symbol=symbol)
        shares = ownedStock.shares
    else:
        shares = 0
    if stock['today'] < 0:
        todayColor = 'style=color:--red;'
    else:
        todayColor = 'style=color:green;'
    context = {
        'username': username, 
        'balance': round(balance, 2), 
        'stock': stock,
        'todayColor': todayColor,
        'shares': shares
        }
    return render(request, 'trader/stock.html', context)

def search(request):
    if request.method == "POST":
        tickerSymbol = request.POST.get('ticker')
        return HttpResponseRedirect('/stock/{}'.format(tickerSymbol))

def portValue():
    #stocks = Stock.getStocks()
    transactions = Transaction.getTransactions()
    value = 0
    total = 0
    for tran in transactions:
        value = tran.price * tran.shares
        total += value
    return total

def account(request):
    account = Account.getAccount(1)
    balance = account.balance
    username = account.username
    password = account.password
    firstname = account.first_name
    lastname = account.last_name
    investValue = portValue()
    transactions = Transaction.getTransactions()
    context = {
        'username': username, 
        'firstname': firstname, 
        'lastname': lastname, 
        'password': password, 
        'balance': round(balance, 2), 
        'transactions': transactions, 
        'investValue': investValue
        }
    return render(request, 'trader/account.html', context)

def resetAccount(request):
    Account.resetBalance()
    Stock.deleteAllStock()
    Transaction.deleteAllTransactions()
    return redirect('/account')


def buyStock(request):
    account = Account.getAccount(1)
    balance = account.balance
    resp = {}
    
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            symbol = data['symbol']
            name = data['name']
            shares = data['shares']
            price = data['price']
            if balance >= int(float(price)) * int(float(shares)):
                account.balance = balance - int(float(price)) * int(float(shares))
                account.save()
                newbalance = account.balance
                count = Stock.objects.filter(symbol=symbol).count()
                owned = 0
                if count >= 1:
                    stock = Stock.objects.get(symbol=symbol)
                    stock.shares += int(float(shares))
                    owned = stock.shares
                    stock.save()
                else:
                    Stock.objects.create(symbol=symbol, name=name, shares=shares, account_id = 1)
                    owned = shares
                Transaction.createTransaction('Buy', symbol, shares, price, accountId = 1)
                resp['result'] = 'Success'
                resp['message'] = 'Successfully ordered {} shares of {}!'.format(shares, symbol)
                resp['owned'] = owned
                resp['balance'] = round(newbalance, 2)
            else:
                resp['result'] = 'Failure'
                resp['message'] = 'Insufficent Funds'
        return JsonResponse(resp)

    except Exception as e:
        resp['result'] = 'Error'
        resp['message'] = e
        return JsonResponse(resp)

def sellStock(request):
    account = Account.getAccount(1)
    balance = account.balance
    resp = {}

    try:
        if request.method == "POST":
            data = json.loads(request.body)
            print("Json=" + str(data))
            symbol = data['symbol']
            shares = data['shares']
            price = data['price']
            count = Stock.objects.filter(symbol=symbol).count()
            if count >= 1:
                stock = Stock.getStock(symbol)
                if stock.shares >= int(float(shares)):
                    owned = 0
                    if stock.shares > int(float(shares)):
                        stock.shares -= int(float(shares))
                        owned = stock.shares
                        stock.save()
                    elif stock.shares == int(float(shares)):
                        stock.delete()
                    account.balance = balance + int((float(price)) * int(float(shares)))
                    newbalance = account.balance
                    account.save()
                    Transaction.createTransaction('Sell', symbol, shares, price, accountId = 1)
                    resp['result'] = 'Success'
                    resp['message'] = 'Successfully sold {} shares of {}!'.format(shares, symbol)
                    resp['owned'] = owned
                    resp['balance'] = round(newbalance, 2)
                else:
                    resp['result'] = 'Failure'
                    resp['message'] = 'Cannot sell more shares than you own.'
            else:
                resp['result'] = 'Failure'
                resp['message'] = 'You do not own this stock.'
            return JsonResponse(resp)

    except Exception as e:
        resp['result'] = 'Error'
        resp['message'] = e
        return JsonResponse(resp)


def login_view(request):
    user = authenticate(request, username='root', password='password123')
    if user is not None:
        print('username is authenticated')
        login(request, user)
        return redirect('/')


def logout_view(request):
    logout(request)
    return redirect('/')

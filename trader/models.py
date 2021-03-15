from typing import final
from django.db import models
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    balance = models.DecimalField(max_digits=20, decimal_places=4)

    def __str__(self):
        return "username=" + str(self.username) + ", password=" + str(self.password) + ", balance=" + str(self.balance)

    def getAccount(AccountId):
        account = get_object_or_404(Account, pk=AccountId)
        return account

    def resetBalance():
        account = get_object_or_404(Account, pk=1)
        account.balance = 10000.0000
        account.save()

class Stock(models.Model):
    symbol = models.CharField(max_length=5)
    name = models.CharField(max_length=25)
    shares = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)


    def __str__(self):
        return "symbol=" + str(self.symbol) + "name=" + str(self.name) + ", shares=" + str(self.shares)

    def getStock(ticker):
        stock = Stock.objects.get(symbol=ticker)
        return stock

    def getStocks():
        stocks = Stock.objects.all()
        return stocks

    def deleteAllStock():
        stocks = Stock.getStocks()
        stocks.delete()


class Transaction(models.Model):
    orderType = models.CharField(max_length=4)
    symbol = models.CharField(max_length=5)
    shares = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    orderDate = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return "symbol=" + str(self.symbol) + ", shares=" + str(self.shares) + ", price=" + str(self.price) + ", orderDate=" + str(self.orderDate)

    def getTransactions():
        transactions = Transaction.objects.all()
        return transactions

    def createTransaction(orderType, symbol, shares, price, accountId):
        Transaction.objects.create(orderType=orderType, symbol=symbol, shares=shares, price=price, account_id=accountId)

    def deleteAllTransactions():
        transactions = Transaction.getTransactions()
        transactions.delete()
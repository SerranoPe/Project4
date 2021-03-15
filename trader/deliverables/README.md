# project04
Web Development Project 04 Trader App

Home Page:
    1) User's account balance

    2) Stock search | display current stock info

    3) Links to Buy/Sell Stock and Portfolio

Stock Page:
    1) User's account balance

    2) Search stock

    3) Amount field

    4) Buy / Sell buttons

Portfolio Page:
    1) User's account balance

    2) Table of all stocks owned


Commands ran:

django-admin startporject project04
django-admin startapp trader
python manage.py runserver
python manage.py makemigrations trader
python manage.py migrate
python manage.py shell

pip install pandas
pip install pandas-datareader
pip install numpy
pip install matplotlib
pip install datetime
pip install yfinance --upgrade --no-cache-dir

python manage.py createsuperuser --username=root --email=root@abc.com
password: password123
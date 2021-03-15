from datetime import date, datetime, timedelta

# tday = date.today()
# print (tday)

# now = datetime.now()
# print(now)


# print(tday.weekday()) #Mon 0 Sun 6
# print(tday.isoweekday()) # Mon 1 Sun 7

# tdyear = (tday.year)
# tdmonth = (tday.month)
# tdday = (tday.day)

def getDate(range = 'today'):
    tday = date.today()
    week = timedelta(days=7)
    month = timedelta(days=30)
    year = timedelta(days=365)

    if range == 'week':
        weekAgo = tday - week
        return weekAgo
    
    elif range == 'month':
        monthAgo = tday - month
        return monthAgo
    
    elif range == 'year':
        yearAgo = tday - year
        return yearAgo

    else:
        return tday

import json
import itertools
from datetime import datetime, timedelta

def readFile(month):
    with open(f'calendar/{month}.json') as json_data:
        d = json.load(json_data)
        json_data.close()
        return d

def get_days_in(fromDate, toDate):
    fromMonthEvents = readFile(fromDate.month)
    without = list(itertools.dropwhile(lambda elem: elem["day"] < fromDate.day, fromMonthEvents))
    if toDate.month == fromDate.month:
        return list(itertools.takewhile(lambda elem: elem["day"] <= toDate.day, without))
    else:
        toMonthEvents = readFile(toDate.month)
        return without + list(itertools.takewhile(lambda elem: elem["day"] <= toDate.day, toMonthEvents))




print(get_days_in(datetime.now(), datetime.now() + timedelta(days=30)))
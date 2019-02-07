# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:46:32 2019

@author: LatizeExpress
"""
import requests
from_curr = input("From currency: ").upper()
to_curr = input("To currency: ").upper()
amount = float(input("Amount: "))
response = requests.get("http://api.fixer.io/latest?base="+from_curr+"&amp;symbols="+to_curr)
rate = response.json()['rates'][to_curr]
print("Exchange rate: "+ str(round(rate,4))+", "+str(amount)+" "+from_curr+" = " + str(round((rate * amount), 2)) + " " +to_curr)



import json
from urllib.request import urlopen
f = urlopen('http://api.wunderground.com/api/Your_Key/geolookup/conditions/q/IA/Cedar_Rapids.json')
json_string = f.read()
parsed_json = json.loads(json_string)
location = parsed_json['location']['city']
temp_f = parsed_json['current_observation']['temp_f']
print( "Current temperature in %s is: %s" % (location, temp_f))
f.close()


import os, sys, datetime, commands
from urllib.request import urlopen
import json

myweather = json.load(urlopen("http://api.wunderground.com/api/API_KEY/forecast/q/27.711,17.994.json"))
myweather_sum = myweather['forecast']['txt_forecast']['forecastday']

for period in myweather_sum:
    myforday = period['title']
    myfctxt = period['fcttext_metric']
    print myforday
    print myfctxt
    print "-----------------------------"






import requests
import pandas as pd
from dateutil import parser, rrule
from datetime import datetime, time, date
import time


path = "E:/Misc/"
def getRainfallData(station, day, month, year):
    """
    Function to return a data frame of minute-level weather data for a single Wunderground PWS station.

    Args:
        station (string): Station code from the Wunderground website
        day (int): Day of month for which data is requested
        month (int): Month for which data is requested
        year (int): Year for which data is requested

    Returns:
        Pandas Dataframe with weather data for specified station and date.
    """
    url = "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID={station}&day={day}&month={month}&year={year}&graphspan=day&format=1"
    full_url = url.format(station=station, day=day, month=month, year=year)
    # Request data from wunderground data
    response = requests.get(full_url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
    data = response.text
    # remove the excess <br> from the text data
    data = data.replace('<br>', '')
    # Convert to pandas dataframe (fails if issues with weather station)
    try:
        dataframe = pd.read_csv(io.StringIO(data), index_col=False)
        dataframe['station'] = station
    except Exception as e:
        print("Issue with date: {}-{}-{} for station {}".format(day,month,year, station))
        return None
    return dataframe

# Generate a list of all of the dates we want data for
start_date = "2019-01-01"
end_date = "2019-01-21"
start = parser.parse(start_date)
end = parser.parse(end_date)
dates = list(rrule.rrule(rrule.DAILY, dtstart=start, until=end))

# Create a list of stations here to download data for
stations = ["IDUBLINF3", "IDUBLINF2", "ICARRAIG2", "IGALWAYR2", "IBELFAST4", "ILONDON59", "IILEDEFR28"]
# Set a backoff time in seconds if a request fails
backoff_time = 10
data = {}

# Gather data for each station in turn and save to CSV.
for station in stations:
    print("Working on {}".format(station))
    data[station] = []
    for date in dates:
        # Print period status update messages
        if date.day % 10 == 0:
            print("Working on date: {} for station {}".format(date, station))
        done = False
        while done == False:
            try:
                weather_data = getRainfallData(station, date.day, date.month, date.year)
                done = True
            except ConnectionError as e:
                # May get rate limited by Wunderground.com, backoff if so.
                print("Got connection error on {}".format(date))
                print("Will retry in {} seconds".format(backoff_time))
                time.sleep(10)
        # Add each processed date to the overall data
        data[station].append(weather_data)
    # Finally combine all of the individual days and output to CSV for analysis.
    pd.concat(data[station]).to_csv(path+"data/{}_weather.csv".format(station))



import meteomatics_weather_api as api
import datetime as dt

username = 'latize_gaur'
password = 'mustermann'
lat = 47.11
lon = 11.47
startdate = dt.datetime.utcnow().replace(hour = 0, minute = 0, second = 0, microsecond = 0)


# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 12:52:07 2019

@author: LatizeExpress
"""
# Getting Started

# Need to get this key from https://www.mytransport.sg/content/mytransport/home/dataMall.html
key = open("lta-key.txt").read()

import requests
import pandas as pd
import csv
path = "E:/Misc/"
incidents = requests.get(
    'http://api.data.gov.sg/v1/environment/2-hour-weather-forecast').json()

len(incidents)

incidents.keys()

incidents.values()
print(incidents.get("area_metadata"))
print(incidents.get("items"))
print(incidents.get("api_info"))

len(incidents.values())

incidents.values()

for key, val in incidents.items():
    print(key, "=>", val)


with open(path+'test.csv', 'w') as f:
    for key in incidents.keys():
        f.write("%s,%s\n"%(key,incidents[key]))


forcst = incidents.get("items")
print(forcst[-1])
forcst1 = pd.DataFrame(forcst)
forecast2 = forcst1.forecasts
 for i, val in forecast2.items():
     print(i, val)

forecast3 = pd.DataFrame(forecast2)
forecast3.columns

#forcst1.to_csv(path+"forecast1.csv", header = True, index =  False)
with open(path+'forecast.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(forcst)
csvFile.close()


latlong = incidents.get("area_metadata")
latlong1 = pd.DataFrame.from_dict(latlong)
latlong1.to_csv(path+"latlong.csv", header = True, index =  False)



def find_place(string):
    return [stop for stop in forcst1.items if string in stop['Description']]


find_place("Sengkang")




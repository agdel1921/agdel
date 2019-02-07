# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 11:07:38 2019

@author: LatizeExpress
"""
import json
from urllib.request import urlopen
f = urlopen('http://api.data.gov.sg/v1/environment/2-hour-weather-forecast')
json_string = f.read()
parsed_json = json.loads(json_string)
location = parsed_json['location']['city']
temp_f = parsed_json['current_observation']['temp_f']
print( "Current temperature in %s is: %s" % (location, temp_f))
f.close()



http://api.data.gov.sg/v1/environment/2-hour-weather-forecast
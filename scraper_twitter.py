# -*- coding: utf-8 -*-
"""
Created on Mon Aug 08 14:40:57 2016

@author: Vidyut
"""

import tweepy
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os

ckey = ["TDdDg7XUOccCaFS9NvEg6ADr1","W2OCkMO2ybGFVU4s7BgXFk0MO","YlyNuGXxkCIwTbTENShCVyAV4","IhUFgQqUSJi668S81ifMQx3Mw"]
csecret = ["cFF44BcWwJm37Tqit2ATj1nJl2CaMm4Tah1OscpHov3nMDoDiQ","Hm5dGOZNCQ3SliwMiSMZTRo35k7ZFfQoGmvjpVkpUseuTGEjeJ","bj5dbh3RpsHohAxMuVN3zkjfNGrtZUbJlwYueWwqOeDfHaijCj","zepyErdr92kiCO68O4uT68JUHcVoACOi7FCakqh4inkGJj1pmo"]
atoken = ["16280903-SHcxm2NHJy1CpFYa1muJ7tdulN99Dlhql45Nj5LpY","16280903-EgpG7X9XQbmcajILrMAK7Tf6FOmqHEnNc8sCvZDbf","	16280903-hNz3jkAo2PePYt42gF0MaJLurEd6VWV744X0N52DO", "16280903-RvkGJ55mNd25DQiEplnd8a2OzIqroW4BoF63S7NZY"]
asecret = ["ehoStGnleKxgLl6tKxrwUjgWTTJ3rKp5PWhCHmKF2NTTf","GWrIwseUzVQwxJx2L1VfkF4gBs9hNu6Bq1UbtjBSvmhSG","pCt3HJLZ0ia3dlGQqAfmkY6erKIFaxtvpeH6CXwy5e5SG","oqWZg5sdVQkkFITq8VmQ2o7uTo599duFehU6tJ3uWKCtZ"]

access_token = ckey[2]
access_token_secret = csecret[2]
consumer_key = atoken[2]
consumer_secret = asecret[2]
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

start_time = time.time() #grabs the system time
keyword_list = ['twitter'] #track list

twitterStream = Stream(auth, listener(start_time, time_limit=20)) #initialize Stream object with a time out limit
twitterStream.filter(track=keyword_list, languages=['en'])  #call the filter method to run the Stre
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 08 17:16:56 2016

@author: Vidyut
"""

import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os



os.chdir('D:/CodeLah!/latize')

browser = webdriver.Chrome()
base_url = u'https://twitter.com/search?q='
query=u'sers%20singapore'

url = requests.get(base_url+query)

soup = BeautifulSoup(url.text, 'html.parser')

tweets = [p.text for p in soup.findAll('p', class_='tweet-text')]
print tweets

####### HDB

browser = webdriver.Chrome()
base_url = u'https://twitter.com/search?q='
query=u'sers%20singapore'

browser.get(base_url+query)
time.sleep(2)

body = browser.find_element_by_tag_name('body')

for _ in range(20):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    
tweets = browser.find_elements_by_class_name('tweet-text')
profiles = browser.find_element_by_class_name('"tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable-original-tweet js-original-tweet"')
ct=1
for tweet in tweets:
    print type(tweet), tweet.text
    print ""
    print ct
    ct=ct+1
    

##### MOE  
  
browser = webdriver.Chrome()
base_url = u'https://twitter.com/search?q='
query=u'sers%20singapore'

browser.get(u'https://www.youtube.com/watch?v=3AtDnEC4zak')
time.sleep(2)

body = browser.find_element_by_tag_name('body')

for _ in range(5):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    
viewCt = body.find_elements_by_class_name('watch-view-count')
publishTime = body.find_elements_by_class_name('watch-time-text')
desc = body.find_elements_by_class_name('watch-description-content')
category = body.find_elements_by_class_name('content watch-info-tag-list')
v=body.find_elements_by_tag_name("div")
ct=1
l=[]
for tweet in v:
    print tweet.text, type(tweet.text)
    print ""
    print ct
    #l.append[tweet.text]
    ct=ct+1
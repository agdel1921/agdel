# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 11:14:53 2016

@author: Vidyut
"""

import os
import sys
import pandas as pd
import codecs
import csv
import chardet
from chardet.universaldetector import UniversalDetector


# read in all the data files
# store all the CSV files
fin=[]
filePathSrc="D:\\training\\twg_copy\\Customer\\"
for root, dirs, files in os.walk(filePathSrc):
    for fn in files:
        if fn[-4:] == '.csv':
            fin.append(fn)
x=filePathSrc+fin[2]
#txt1 = codecs.code_page_decode(x,)

# create an algorithm which locates each Hotel file, extracts the content and date of each review for the concerned hotel 
# and then stores it in fileContent and fileDate
#
s = open(filePath, mode="rb").read()
sc = chard     et.detect(s)
print (sc)



for a in range(1):
    dat=[]
    m=""
    filePath=filePathSrc+"\\"+fin[a]
    lines = open(filePath, 'r',encoding="utf-8").read()
    for line in lines:
            item = line.rstrip()
            # get rid of the extra line seperating each review
            if item=='':
                continue
            else:
                #m=m+" " + line
                dat.append(line)

myfile = open("D:\\training\\twg_copy\\Customer\\vd.csv", 'w', newline='\n')
wr = csv.writer(myfile)
wr.writerow(dat)

resultFile = open("D:\\training\\twg_copy\\Customer\\vd1.csv",'w', newline='\n')
wr = csv.writer(resultFile, dialect='excel')
wr.writerow(dat)



    txt=[text_files[a]]
    txtDate=[text_files[a]]
    for m in range(len(dat)):
        if(m%2==0):
            p=dat[m]
            txt.append(p[9:len(p)-1])
            print (m,'1',m%2,len(txt),len(txtDate))
            continue
        elif(m%2==1):
            o=dat[m]
            txtDate.append(o[6:len(o)-1])
            print (m,'2',m%2,len(txt),len(txtDate))
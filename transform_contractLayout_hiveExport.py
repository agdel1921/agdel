# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 10:19:22 2017

@author: vsdaking
"""

# import required libraries
import pandas as pd
import os

# set the working directory
path = "/home/latize/Downloads/ds/"
os.chdir(path)
fls=os.listdir(path)

opPd = pd.read_csv("/home/latize/Downloads/ds/026.csv", header = 0)
print "done"
colNames = list(opPd.columns)

opPd = pd.DataFrame(columns = colNames)

ct=1
# run the program for all CSV files in the path
for a in fls:
    if a[0]=='x':
		if a!= "x00000000":
			# read in the CSV file and store it in a DF (data frame) called m
			csvPd = pd.read_csv(a, sep='","', header=None)
			csvPd.columns = colNames
			dst= path+a[-3:]+".csv"
			csvPd.to_csv(dst, header = True, index = False)
			print dst
print ""
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
path = "D:/training/TWG_overall/data_harmonisation/JPN/JPN_Hive_op/split/"
os.chdir(path)
fls=os.listdir(path)

opPd = pd.read_csv("D:/training/TWG_overall/data_harmonisation/JPN/JPN_Hive_op/split/x00000011", sep='","', header = None)



# run the program for all CSV files in the path
for a in fls:
    if a[0]=='x':
		if a!= "x00000000":
			# read in the CSV file and store it in a DF (data frame) called m
			csvPd = pd.read_csv(, sep='","', header=None)
              		print a
    			csvPd.columns = list(opPd.columns)
             		#opPd = opPd.append(csvPd, ignore_index=True)
			print a

dest = path+"bwcontractlayout.csv"
opPd.to_csv(dest, header=True, index=False)
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 17:44:29 2016

@author: Vidyut
"""

# import required libraries
import pandas as pd
import os
import numpy as np

# set the working directory
path = "D:/training/TWG_overall/data_harmonisation/JPN/SQL_dump/sql_csv_dumps/"
dst = "D:/training/TWG_overall/data_harmonisation/JPN/SQL_dump/final_sql_csv/"
os.chdir(path)
fls=os.listdir(path)

# run the program for all CSV files in the path
for a in range(len(fls)):
    if fls[a][-3:]=='csv':
        # read in the CSV file and store it in a DF (data frame) called m
        csvPd = pd.read_csv(fls[a], header=0)
        destination = dst+fls[a]
        csvPd.to_csv(destination,header=None, index=False, encode="utf-8")
        print a

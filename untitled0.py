# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 15:31:50 2016

@author: Vidyut
"""

# import required libraries
import pandas as pd
import os

# set the working directory
path = "D:/training/NER/VA/Infopedia for CV3 (150 articles) Aug2016/Content/"
os.chdir(path)
fls=os.listdir(path)

        
# run the program for all CSV files in the path
for a in fls:
    if a[-3:]=='csv':
        # read in the CSV file and store it in a DF (data frame) called m
        csvPd = pd.read_csv(a, header=0)

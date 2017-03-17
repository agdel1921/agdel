# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 11:31:12 2017

@author: vsdaking
"""

# import required libraries
import pandas as pd
import os

# set the working directory
path = "D:/training/TWG_overall/data_harmonisation/KR/Data/"
os.chdir(path)
fls=os.listdir(path)
exclude = ['AONA13.csv', 'ANROMP.csv', 'WSVRS01.csv', 'WTPMT01.csv', 'WXMVE01.csv','Y2VLLSP.csv', 'AONB02.csv', 'WTLCI01.csv', 'WXMVN01.csv','XXXM01.csv']
fls = [k for k in fls if k not in exclude]

# metadata contains the table name, the number of columns and the number of rows present
metadata = []

# run the program for all CSV files in the path
for a in fls:
    if a[-3:]=='csv':
        # read in the CSV file and store it in a DF (data frame) called m
        try:
            csvPd = pd.read_csv(a, header=None, low_memory=False)
            metadata.append([a[:-4],len(csvPd.columns), len(csvPd)])
            print a[:-4]
        except TypeError:
            continue

dest = path[:-5]+"metadata.csv"
metadataDf = pd.DataFrame(metadata, columns = ["Table_Name", "Num_of_columns","Num_of_rows"])
metadataDf.to_csv(dest,header=True, index=False)

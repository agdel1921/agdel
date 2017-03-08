# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 12:22:16 2016

@author: Vidyut
"""

# import required libraries
import pandas as pd
import os

# set the working directory
path = "D:/training/TWG_overall/data_harmonisation/mapping/JPN/"
os.chdir(path)
fls=os.listdir(path)

for x in fls:
    if x[-3:]=='txt':
        # Method 1
        with open(x, 'r') as file:
            fileList = file.readlines()
        len(fileList)
        op = [['Table_Name','Rows'] for i in range(1)]
        ct=0
        while ct<(len(fileList)-1):
            op.append([fileList[ct].rstrip(),int(fileList[ct+1].rstrip())])
            ct=ct+2

pd2 = pd.DataFrame(op[1:])
pd2.to_csv('D:/training/TWG_overall/data_harmonisation/mapping/JPN/hive_twg_tables_counts.csv', header= ['Table_name','Rows'],index=False)    

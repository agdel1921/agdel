# -*- coding: utf-8 -*-
"""
Created on Thu Oct 06 14:07:54 2016

@author: vsdaking
"""

# import required libraries
import pandas as pd
import numpy as np
import os

# set the working directory
path = "D:/training/TWG_overall/data_harmonisation/mapping/JPN/"
os.chdir(path)
fls=os.listdir(path)

fls = ['dtm_trial_map_of_columns_to_files_DTM.xlsx']

# run the program for all XLSX files in the path
for a in fls:
    if a[-4:]=='xlsx':   
        # read in the excel file and store it in a DF (data frame) called m
        xlsxPd = pd.read_excel(a, header=0)

m = xlsxPd.as_matrix()

cols = m[:,0]
dist_cols = np.unique(cols)
dist_cols.sort()

files = m[:,1]
dist_files = np.unique(files)
dist_files.sort()

output = [[0 for x in range(len(dist_files))] for y in range(len(dist_cols))]

for a in range(len(dist_cols)):
    for x in range(len(cols)):
        if dist_cols[a]==cols[x]:
            cls = files[x]
            for y in range(len(dist_files)):
                if dist_files[y]==files[x]:
                    output[a][y]=1
                    break
                
fin = pd.DataFrame(output, columns = dist_files, index = dist_cols)

fin.to_csv("D:/training/TWG_overall/data_harmonisation/mapping/JPN/try.csv", index=True, header=True)
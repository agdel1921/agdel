# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 23:01:22 2016

@author: Vidyut
"""

# import required libraries
import pandas as pd
import os

# set the working directory
path = "F:/random/c2r/"
os.chdir(path)
fls=os.listdir(path)


# run the program for all XLSX files in the path
for a in fls:
    if a[-4:]=='xlsx':   
        # read in the excel file and store it in a DF (data frame) called m
        xlsxPd = pd.read_excel(a, header=0)
        
        
# run the program for all CSV files in the path
for a in fls:
    if a[-3:]=='csv':
        # read in the CSV file and store it in a DF (data frame) called m
        csvPd = pd.read_csv(a, header=0)

        
# run the program for all TXT files in the path
for a in fls:
    if a[-3:]=='txt':
        # different ways to read in data from the file -
        
        # Method 1
        with open(a, 'r') as file:
            fileList = file.readlines()

        # Method 2        
        with open(a, 'r') as file:
            m=[]
            for line in file:
                m.append(line)
        
        
# write data to a file
with open("F:/random/c2r/hello.txt", "w") as f:
    f.write("Hello World")
    
    
# run the program to split data read in
# by default, split() will break the sentence read in based on blank spaces. 
# Change this by providing a parameter to split - e.g. split('o')
with open('hello.txt', 'r') as f:
    data = f.readlines()
    for line in data:
        words = line.split()
        print words            

# update cell values for DF df
#
# OG DF
#       x    y
#   A  NaN  NaN
#   B  NaN  NaN
#   C  NaN  NaN
#
#       x    y
#   A  NaN  NaN
#   B  NaN  NaN
#   C  10  NaN
df = pd.DataFrame(columns=['x','y'], index = ['A','B','C'])
df.set_value('C', 'x', 10)
df['x']['C'] = 10
df.ix['C','x'] = 10
df.xs('C', copy=False)['x'] = 10



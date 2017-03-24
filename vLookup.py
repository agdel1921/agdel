# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 15:31:50 2016

@author: Vidyut
"""

# import required libraries
import pandas as pd
import numpy as np
import os


# set the working directory
# "D:/training/NER/VA/output/" - VA
# "D:/training/NER/ITQ/Attachment9_Sample Test Articles/" - ITQ
path = "D:/training/NER/ITQ/Attachment9_Sample Test Articles/"
os.chdir(path)
fls=os.listdir(path)


# 'D:/training/NER/VA/TTE terms (20160901)_Latize1.xlsx' - VA
# 'D:/training/NER/ITQ/Attachment1_Sample NLB TTE Terms.xlsx' - ITQ
dict1 = pd.ExcelFile('D:/training/NER/VA/TTE terms (20160901)_Latize1.xlsx')
dict1.sheet_names  # see all sheet names


dictPd = []


for s in dict1.sheet_names:
    tempPd = dict1.parse(s)  # read a specific sheet to DataFrame
    print len(tempPd)
    dictPd.append(tempPd)
    
    
dictPd = pd.concat(dictPd)
print len(dictPd)


pName = list(dictPd['Preferred name'].values.ravel())
npName = [t for t in dictPd['Non-preferred name'].values.ravel()]


word=[]
entity=[]
np_entity=[]


# run the program for all CSV files in the path
for a in fls:
    if a[-3:]=='csv':
        # read in the CSV file and store it in a DF (data frame) called m
        index = []
        csvPd = pd.read_csv(a, header=0)
        print a[:-3]
        print "Check in Preferred"        
        for tz in range(len(csvPd.values.ravel())):
            if type(tz)!=float:
                for u in range(len(pName)):
                    if csvPd.values.ravel()[tz]==pName[u]:
                        print tz, u, pName[u]
                        word.append(csvPd.values.ravel()[tz])                        
                        entity.append(pName[u])
                        index.append(u)
        print "Check in Non-Preferred"
        for tz in range(len(csvPd.values.ravel())):
            if type(tz)!=float:
                for u in range(len(npName)):
                    if csvPd.values.ravel()[tz]==npName[u]:
                        print tz, u, pName[u]
                        word.append(csvPd.values.ravel()[tz])                        
                        np_entity.append(npName[u])
                        index.append(u)
        print "\n"
        lo = dictPd.as_matrix()
        if len(index)>0:        
            t4 = []
            fin =[]
            for r in index:
                t4.append(lo[r][0])
                #t4.append([dictPd.iloc[[r]]['Key UID'],dictPd.iloc[[r]]['Preferred name'],dictPd.iloc[[r]]['Vocabulary Class']])
            r6 =[]
            for ew in t4:
                if ew not in r6:
                    r6.append(ew)
            fin = pd.DataFrame(r6)
            #fin.columns = ['Key UID', 'TTE Preferred Name', 'TTE Vocabulary Class']
            fin.columns = ['TTE Preferred Name']
            outputDest = a[:-4]+'_final.csv'
            fin.to_csv(outputDest, index=False, header = True)
            
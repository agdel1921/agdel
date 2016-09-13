# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 23:00:04 2016

@author: Vidyut
"""

# import required libraries
import pandas as pd
import os
import numpy as np
import random
import time
from passlib.hash import md5_crypt
import datetime

start = []
end = []
start.append(datetime.datetime.now().time())

# set the working directory
#path = "D:/training/randomProg/cryptoAnon/"

path = "D:/training/TWG_overall/data_harmonisation/JPN/twg_ag/trial/"

os.chdir(path)
fls=os.listdir(path)


# set the number of decimal places to see in DFs
pd.set_eng_float_format(accuracy=15, use_eng_prefix=True)


# ask the user for the names of the columns that they want to anonymize
inpCols = raw_input("Please enter the names of the column to anonymize. Seperate each column by a comma \n")
inpColsSplit = inpCols.split(',')
inpColsLower1 = [f.strip().lower() for f in inpColsSplit]

inpo =[]
inpColsLower = [ui for ui in inpColsLower1 if ui not in inpo and (inpo.append(ui) or True)]

inpColsLower.append('randnum')
inpColsLower.append('hash')
print inpColsLower

# run the program for all XLSX files in the path
for a in fls:
    if a[-4:]=='xlsx':   
        start.append(datetime.datetime.now().time())
        inpColsLower.append(a[:-4].strip().lower()+'_checksum')

        # read in the excel file and store it in a DF (data frame) called m
        print a        
        xlsxPd = pd.read_excel(a, header=0)
        
        # create a copy of the original Data Frame read in - for safety sake & backup purposes
        xlsxPd1 = xlsxPd.copy()
        
        # create storage for each randomly generated number assigned to a given record, the hash generated and the checksum
        num =[]
        encrpyt =[]
        chkSum = []
        
        # generate a uniquely random number to identify each record by - store this random no in the randNum column of DF
        for i in range(len(xlsxPd1)):
            # generate a uniquely random number - generated based on the System's current state            
            ch = str(random.SystemRandom(time.time).random())            
            num.append(ch)
            # hash the uniquely random number            
            hashed = md5_crypt.encrypt(ch)
            encrpyt.append(hashed)
            chkSum.append(hashed[(hashed.rfind('$')+1):])
        
        # add the 3 new lists to the DF being used
        xlsxPd1['randNum'] = pd.Series(num)
        xlsxPd1['hash'] = pd.Series(encrpyt)
        xlsxPd1[a[:-4].strip().lower()+'_checksum'] = pd.Series(chkSum) 
        col = xlsxPd1.columns
        col = [m.strip() for m in col]
        colLower = [m.strip().lower() for m in col]
        colAnon =[]            
        for i in inpColsLower:
            for j in range(len(colLower)):
                if i==colLower[j]:
                    print j, col[j]
                    colAnon.append(j)
                else:
                    continue
        
        print colAnon, '\n'
        pdAnon = pd.DataFrame()
        for l in colAnon:
            print col[l]
            pdAnon[col[l]] = xlsxPd1.ix[:,l:(l+1)].copy()
        remCols = [l for l in colAnon if col[l]!=a[:-4].strip().lower()+'_checksum']
        xlsxPd1.drop(xlsxPd1.columns[remCols], axis=1, inplace=True)
        
        # export the Anonymised & PII files to specified path
        anonLoc = path+a[:-4]+'_anon.csv'
        xlsxPd1.to_csv(anonLoc, sep=',', index=False)
        piiLoc = path+a[:-4]+'_pii.csv'        
        pdAnon.to_csv(piiLoc, sep=',', index=False)
        end.append(datetime.datetime.now().time())
        
# run the program for all XLSX files in the path
for a in fls:
    if a[-3:]=='csv':   
        start.append(datetime.datetime.now().time())
        inpColsLower.append(a[:-4].strip().lower()+'_checksum')

        # read in the excel file and store it in a DF (data frame) called m
        print a        
        xlsxPd = pd.read_csv(a, header=0, low_memory=False)
        
        # create a copy of the original Data Frame read in - for safety sake & backup purposes
        xlsxPd1 = xlsxPd.copy()
        
        # create storage for each randomly generated number assigned to a given record, the hash generated and the checksum
        num =[]
        encrpyt =[]
        chkSum = []
        
        # generate a uniquely random number to identify each record by - store this random no in the randNum column of DF
        for i in range(len(xlsxPd1)):
            # generate a uniquely random number - generated based on the System's current state            
            ch = str(random.SystemRandom(time.time).random())            
            num.append(ch)
            # hash the uniquely random number            
            hashed = md5_crypt.encrypt(ch)
            encrpyt.append(hashed)
            chkSum.append(hashed[(hashed.rfind('$')+1):])
        
        # add the 3 new lists to the DF being used
        xlsxPd1['randNum'] = pd.Series(num)
        xlsxPd1['hash'] = pd.Series(encrpyt)
        xlsxPd1[a[:-4].strip().lower()+'_checksum'] = pd.Series(chkSum) 
        col = xlsxPd1.columns
        col = [m.strip() for m in col]
        colLower = [m.strip().lower() for m in col]
        colAnon =[]            
        for i in inpColsLower:
            for j in range(len(colLower)):
                if i==colLower[j]:
                    print j, col[j]
                    colAnon.append(j)
                else:
                    continue
        
        print colAnon, '\n'
        pdAnon = pd.DataFrame()
        for l in colAnon:
            print col[l]
            pdAnon[col[l]] = xlsxPd1.ix[:,l:(l+1)].copy()
        remCols = [l for l in colAnon if col[l]!=a[:-4].strip().lower()+'_checksum']
        xlsxPd1.drop(xlsxPd1.columns[remCols], axis=1, inplace=True)
        
        # export the Anonymised & PII files to specified path
        anonLoc = path+a[:-4]+'_anon.csv'
        xlsxPd1.to_csv(anonLoc, sep=',', index=False)
        piiLoc = path+a[:-4]+'_pii.csv'        
        pdAnon.to_csv(piiLoc, sep=',', index=False)
        end.append(datetime.datetime.now().time())

end.append(datetime.datetime.now().time())

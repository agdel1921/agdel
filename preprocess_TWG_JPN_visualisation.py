# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 19:01:19 2017

@author: Ashu & vsdaking
"""

import os
import pandas as pd
import random
import numpy as np
import copy
import math
from collections import Counter
import datetime

path = "D:/training/TWG_overall/data_harmonisation/final_output_JPN/og_files/"

os.chdir(path)

fls = os.listdir(path)

# Return a randomly chosen list of n positive integers summing to total.
# Each such list is equally likely to occur.
def constrained_sum_sample_pos(n, total):
    dividers = sorted(random.sample(xrange(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

# Redistribute the data sets 
def redistribute_col_values(arr_containing_postns, vals_to_replace_with):
    kNew = [0]
    kTmp = [sum(arr_containing_postns[:l+1]) for l in range(len(arr_containing_postns))]
    kNew.extend(kTmp)
    cpy = []
    for l in range(len(kNew)-1):
            for j in range(kNew[l],kNew[l+1]):
                cpy.append(vals_to_replace_with[l])
    arrReturned  = copy.deepcopy(cpy)
    return arrReturned

# function to eliminate all empty columns from DF (threshold set at 98%  - update if need be)
def remove_empty_cols_from_pd(df1):
    copyDf1 = df1.copy()
    for cNum in range(len(df1.columns)):
        colName = df1.columns[cNum]
        lstTmp = list(df1[[colName]].values.flatten())
        nan_Cols = [1 for elmnt in lstTmp if elmnt==0.0]
        print colName, cNum
        if len(nan_Cols)>0:
            if sum(nan_Cols)/float(len(df1))>0.95:
                print "\t", sum(nan_Cols), len(lstTmp)
                copyDf1.drop(colName, axis=1, inplace=True, errors = 'ignore')
    return copyDf1
    
# function to format Date columns in DF
def format_date(df2):
    for col in range(len(df2.columns)):
        colName2 = df2.columns[col]
        lstTmp2 = list(df2[[colName2]].values.flatten())
        if 'date' in colName2:
            df2[[colName2]] = pd.to_datetime(lstTmp2, format= '%Y%m%d', errors = 'coerce')
    return df2
    
#fls = ['bw_claims-000.csv']
#fls = [u for u in fls if u!='bw_claims-057.txt']

for a in fls:
    if a=='bw_claims.csv':
        print a
        claimPd = pd.read_csv(a, header = 0, low_memory = True)
        #claimPd = claimPd.head(500000)
        #m.columns = cols
        #m.to_csv(path+a[:-3]+"csv", header=True, index=False)
        print "read ", a
        
        # populate the countries randomly
        place = list(claimPd['country'])
        plc_options= 'JPN','AUS','KOR','MYS','IND','CHN'
        k = constrained_sum_sample_pos(len(plc_options),len(place))
        plc_reorganised = redistribute_col_values(k, plc_options)
        
        # populate the business types randomly
        bus_type_ctry = list(claimPd['businesstype']) 
        bType_option = 'BW','A&T','MR'
        k2 = constrained_sum_sample_pos(len(bType_option),len(bus_type_ctry))
        bType_reorganised = redistribute_col_values(k2, bType_option)
        
        # modify the claimevententereddate format - split into the date and hour of entry
        clmEvntEntrdDate = list(claimPd['claimevententereddate'])
        split1 = []
        split2 = []
        for rw in range(len(clmEvntEntrdDate)):
            if type(clmEvntEntrdDate[rw])==str:
                split1.append(clmEvntEntrdDate[rw][:10])
                split2.append(clmEvntEntrdDate[rw][11:13])
            else:
                split1.append("")
                split2.append("")
        
        # remove the empty columns from DF to get a leaner and more useful DF
        copyClaimPd = remove_empty_cols_from_pd(claimPd)   
        
        copyClaimPd = format_date(copyClaimPd)     
        
        # update the original DF with the newly updated values
        copyClaimPd['country'] = plc_reorganised
        copyClaimPd['businesstype'] = bType_reorganised
        copyClaimPd['clmEventEnteredDate'] = pd.Series(split1, index = copyClaimPd.index)
        copyClaimPd['clmEventEnteredHr'] = pd.Series(split2, index = copyClaimPd.index)
        
        # store the claimPd into a new csv
        copyClaimPd.to_csv(path+a[:-4]+"_modified.csv", header=True, index=False)
        claimPd = None
        
    elif a == "bw_contracts_matched.csv":
        print a
        contractPd = pd.read_csv(a, header = 0, low_memory = True)
        #m.columns = cols
        #m.to_csv(path+a[:-3]+"csv", header=True, index=False)
        print "read ", a
        #contractPd = contractPd.head(500000)
        
        # populate the countries randomly
        place2 = list(contractPd['country'])
        plc_options2= 'JPN','AUS','KOR','MYS','IND','CHN'
        k3 = constrained_sum_sample_pos(len(plc_options2),len(place2))
        plc_reorganised2 = redistribute_col_values(k3, plc_options2)
        
        # populate the business types randomly
        bus_type_ctry2 = list(contractPd['businesstype']) 
        bType_option2 = 'BW','A&T','MR'
        k4 = constrained_sum_sample_pos(len(bType_option2),len(bus_type_ctry2))
        bType_reorganised2 = redistribute_col_values(k4, bType_option2)
        
        # remove the empty columns from DF to get a leaner and more useful DF
        copyContractPd = remove_empty_cols_from_pd(contractPd)
        
        copyContractPd = format_date(copyContractPd)     
        
        
        # update the original DF with the newly updated values
        copyContractPd['country'] = plc_reorganised2
        copyContractPd ['businesstype'] = bType_reorganised2
        
        # store the claimPd into a new csv
        copyContractPd .to_csv(path+a[:-4]+"_modified.csv", header=True, index=False)
        contractPd = None

x = pd.merge(copyClaimPd.drop_duplicates(subset=['contractseqnum','company','contractnum']), copyContractPd.drop_duplicates(subset=['contractseqnum','company','contractnum']), how = 'inner', on = ['contractseqnum','company','contractnum'])

claimStatusLst = list(x.claimstatus)
clmPaid = list(x.claimamt_adjnet)
clmPaid1 = x.claimamt_adjnet
prdPurchsPrice = list(x.productpurchaseprice)
premiumPrice = list(x.contractpurchaseprice)
clmMoreThanPrdPrice = []
profitLst = []

ct=0
ct2 = 0
for z in range(len(clmPaid)):
    if claimStatusLst[z]=="PAID" or claimStatusLst[z]=="PAYMENT ORDERED" or claimStatusLst[z]=="COMPLETED PAYMENT PENDING":
        if clmPaid[z] >= prdPurchsPrice[z]:
            print z, claimStatusLst[z], clmPaid[z], prdPurchsPrice[z]
            ct=ct+1
            clmMoreThanPrdPrice.append(z)
        if clmPaid[z] >= premiumPrice[z]:
            print '\t', z, claimStatusLst[z], clmPaid[z], premiumPrice[z]
            ct2=ct2+1
        profitLst.append(math.fabs(float(premiumPrice[z]) - float(clmPaid[z])))
    else:
        profitLst.append(float(premiumPrice[z]))
print ct, ct2
x['profit'] = pd.Series(profitLst)

#y = x.copy()
y = remove_empty_cols_from_pd(x)
#y = format_date(y)
y.to_csv(path+"merged_both_trial.csv", header=True, index=False)
len(x)
len(y)

#copyClaimPd = None
#copyContractPd = None


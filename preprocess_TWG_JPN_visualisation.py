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

path = "D:/training/TWG_overall/data_harmonisation/final_output_JPN/og_files/"

os.chdir(path)

fls = os.listdir(path)

def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""
    
    dividers = sorted(random.sample(xrange(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

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
            
#fls = ['bw_claims-000.csv']
cols = pd.read_csv("D:/training/TWG_overall/data_harmonisation/final_output_JPN/og_files/claims/bw_claims-000.csv", header = 0, low_memory = True).columns
#fls = [u for u in fls if u!='bw_claims-057.txt']
for a in fls:
    if a[-4:]=='.csv':
        print a
        m = pd.read_csv(a, header = 0, low_memory = True)
        m.columns = cols
        #m.to_csv(path+a[:-3]+"csv", header=True, index=False)
        print "read ", a
        
        # populate the countries randomly
        place = list(m['country'])
        plc_options= 'JP','AU','KR','ML','IN','CY'
        k = constrained_sum_sample_pos(len(plc_options),len(place))
        plc_reorganised = redistribute_col_values(k, plc_options)
        
        # populate the business types randomly
        bus_type_ctry = list(m['businesstype']) 
        bType_option = 'BW','A&T','MR'
        k2 = constrained_sum_sample_pos(len(bType_option),len(bus_type_ctry))
        bType_reorganised = redistribute_col_values(k2, bType_option)
        
        
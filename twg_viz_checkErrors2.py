# -*- coding: utf-8 -*-
"""
Created on Wed Apr 05 11:48:46 2017

@author: vsdaking
"""

import os
import pandas as pd
import numpy as np
import math
import datetime
from collections import Counter

path = "D:/training/TWG_overall/data_harmonisation/final_output_JPN/og_files/"


abPd = pd.read_csv(path+"merged_both.csv", header = 0, low_memory = True)
sd = list(abPd.claimamt_adjnet)        
indx = []
for r in range(len(sd)):
    if sd[r]>-1:
        indx.append(r)
        
clmStatus = list(abPd.claimstatus)
clmAmt = list(abPd.claimamt_adjnet)
warrAmt = list(abPd.contractpurchaseprice)

distClmSts = Counter(clmStatus).keys()
distClmStsVals = Counter(clmStatus).values()

new_arr = []

for z in range(len(distClmSts)):
    tmp_arr = []
    ct=0
    for y in range(len(clmStatus )):
        if clmStatus[y]==distClmSts[z]:
            tmp_arr.append(y)
            if math.isnan(clmAmt[y]):
                ct=ct+1
    new_arr.append([distClmSts[z], tmp_arr, ct, len(tmp_arr)])

z1 = [[clmStatus[r],clmAmt[r], r] for r in range(len(clmStatus)) if clmAmt[r]!=0.0]
x = [z1[rw][0] for rw in range(len(z1))]
Counter(x).keys()
Counter(x).values()

z2 = [[clmStatus[r],clmAmt[r], r] for r in range(len(clmStatus))]
x2 = [z2[rw][0] for rw in range(len(z2))]
Counter(x2).keys()
Counter(x2).values()

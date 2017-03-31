# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 19:41:34 2017

@author: Vd
"""

import os
import pandas as pd

path = "D:/training/TWG_overall/data_harmonisation/final_output_JPN/split/work/"

os.chdir(path)

fls = os.listdir("D:/training/TWG_overall/data_harmonisation/final_output_JPN/split/work/")
#fls = [u for u in fls if u!='bw_claims-057.txt']
for a in fls:
    if a[-4:]=='.txt':
        if a[:-4]+'.csv' not in fls:
            print a
            m = pd.read_csv(a, sep = '","', header = 0, low_memory = True)
            m.to_csv(path+a[:-3]+"csv", header=True, index=False)
            print "done with", a
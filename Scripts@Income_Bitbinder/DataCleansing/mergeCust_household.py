# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 14:15:17 2018

@author: LatizeExpress
"""

import pandas as pd
path = "C:/Users/LatizeExpress/NTUC/abc_trial.csv"
path1 = "C:/Users/LatizeExpress/NTUC/cust_trial.csv"
first = pd.read_csv(path)
second = pd.read_csv(path1)

merged = pd.merge(second, first, how='left', on='Num')
merged.to_csv('merged.csv', index=False)
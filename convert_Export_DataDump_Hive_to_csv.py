# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 15:30:27 2017

@author: vsdaking
"""

import os
import pandas as pd

path = '/home/latize/Downloads/KR/contracts/kr_contracts/'

fls = os.listdir(path)

n = pd.read_csv(path+'x00000000', header=0, sep='","')
n.to_csv(path+"0000.csv", header=True, index=False)
mcols = n.columns

for i in fls:
    if i[0]=='x':
        if i!='x00000000':
            m = pd.read_csv(path+i, header=None, sep='","')
            m.columns = mcols
            m.to_csv(path+ i[-5:]+".csv", header = False, index = False)
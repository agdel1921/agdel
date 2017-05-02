# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 16:28:48 2017

@author: vsdaking
"""

import os
import pandas as pd

#path = "/home/latize/Downloads/KR/contracts/kr_contracts"
path = "D:/training/TWG_overall/data_harmonisation/final_output_KR/contracts/"

fls = os.listdir(path)

fls = ["kr_contracts.csv"]

if __name__ == '__main__':
    for i in fls:
        m = pd.read_csv(path+i, header=0, low_memory=True)
        cols = m.columns
        newCol = []
        for s in cols:
            if "kr_contracts." in s:
                newCol.append(s.replace("kr_contracts.",""))
            else:
                newCol.append(s)
        m.columns = newCol
        m.to_csv(path+i[:-4]+"_1.csv", header=True, index=False)
                
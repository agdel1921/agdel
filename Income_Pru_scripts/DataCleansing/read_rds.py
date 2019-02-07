# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 12:18:34 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy
import matplotlib
import matplotlib.pyplot as plt
import rpy2.robjects as robjects
from rpy2.robjects import r, pandas2ri

pandas2ri.activate()
path = "E:/Working/INNERJOIN_WORKING/RefinedData_groupby5.rds"
#path ="D:/NTUC/raw_data/rds_source/TransactionalData/customer1.rds"
r.data(path)
readRDS = robjects.r['readRDS']
df = readRDS(path)
df = pandas2ri.ri2py(df)
# Writing ot csv f
df.to_csv("income_groupby1.csv", index=False, encoding='utf8')
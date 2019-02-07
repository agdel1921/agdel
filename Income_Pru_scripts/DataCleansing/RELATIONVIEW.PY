# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 14:10:57 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy
#import ggplot2
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
pandas2ri.activate()
path = "D:/trial/relation_latize"
readRDS = robjects.r['readRDS']
df = readRDS(path)
df = pandas2ri.ri2py(df)
df.isnull().sum()
count_nan = len(df) - df.count()
#print(count_nan)
df.info()
df.shape
df.ndim
df.dtypes
pd.isnull(df).any
df.describe()
df.head(5)
df.cov()
df.corr()
df.to_csv("HomeRelation.csv", index=False, encoding='utf8')
df.plot(kind = 'scatter', x = 'MembersCount', y = 'totalkids')
df['TodCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['YoungCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['TeenCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['GradCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['TodCount'].sum()
df['TeenCount'].sum()

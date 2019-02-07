# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s
"""
import pandas as pd
import numpy
import matplotlib
import matplotlib.pyplot as plt
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
pandas2ri.activate()
path = "C:/Users/LatizeExpress/NTUC/houseview_latize.rds"
readRDS = robjects.r['readRDS']
df = readRDS(path)
df = pandas2ri.ri2py(df)
df['full_count'] = df.apply(lambda x: x.count(), axis=1)



df.isnull().sum()

df.isnull().sum()
count_nan = len(df) - df.count()
#print(count_nan)

df.apply(lambda x: x.nunique())


df.info()
df.shape
df.ndim
df.dtypes
pd.isnull(df).any
df.describe()
df.head(5)
df.cov()
df.corr()
df.to_csv("abc_trial.csv", index=False, encoding='utf8')

result = df.apply(pd.value_counts).fillna(0);













df.plot(kind = 'scatter', x = 'MembersCount', y = 'totalkids')
X= df['H.ID']
Y = ['CustomerSeqID']
plt.scatter(df['H.ID'], Y, s=60, c='red', marker='^')
df['TodCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['YoungCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['TeenCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['GradCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['TodCount'].sum()
df['TeenCount'].sum()
df['H.ID'].unique()

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 13:44:08 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy

import matplotlib.pyplot as plt
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri
pandas2ri.activate()
path = "customerview_latize.rds"
readRDS = robjects.r['readRDS']
df = readRDS(path)
df = pandas2ri.ri2py(df)
# Writing ot csv f
df.to_csv("customer_view.csv", index=False, encoding='utf8')
#df_t = df.T
# General Information
df.info()
df.shape
df.unique()
df.ndim
df.dtypes
pd.isnull(df).any
abc = df.describe()
abc.to_csv("description.csv", index=False, encoding='utf8')
df.head(5)
df.cov()
df.corr()




# Missing Value report
df.isnull().sum()
count_nan = len(df) - df.count()
print(count_nan)

def missing_values_table(df):
        mis_val = df.isnull().sum()
        mis_val_percent = 100 * df.isnull().sum() / len(df)
        mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        mis_val_table_ren_columns = mis_val_table.rename(
        columns = {0 : 'Missing Values', 1 : '% of Total Values'})
        mis_val_table_ren_columns = mis_val_table_ren_columns[
        mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)
        print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"
            "There are " + str(mis_val_table_ren_columns.shape[0]) +
              " columns that have missing values.")
        return mis_val_table_ren_columns


missing_values_table(df)

#df['Decision_maker'].isnull().sum()
##df['Decision_maker'].isnull().any()
#df.isnull().values.ravel().sum()


# Counting Unique records
col_uni_val={}
for i in df.columns:
    col_uni_val[i] = len(df[i].unique())

#Import pprint to display dic nicely:
import pprint
pprint.pprint(col_uni_val)

df.apply(lambda x: x.nunique())
col_un= {}
for i in df.columns:
    col_un[i]=df[i].unique()
    print(i, col_un[i])
pd = pd.DataFrame.from_dict(col_un, orient='index')
pd.to_csv("cust_unique.csv",sep=',')



df['CustomerType'].unique()

for col in df:
    print(df[col].unique())


df_dict = dict(zip([i for i in df.columns], [pd.DataFrame(df[i].unique(),columns=[i]) for i in df.columns]))

for i in df.columns:
    print(df_dict['CustomerSeqID'])
#X= df['H.ID']
#Y = ['CustomerSeqID']
#plt.scatter(df['H.ID'], Y, s=60, c='red', marker='^')


newdf = df[df.columns[19:21]]
for i in newdf.columns:
    abc = newdf.groupby(i).count()
print(abc)




abc = df['Adult'].value_counts()

abc = df['ReachScore10'].unique.count()


df['ReachScore10'].count()



df.plot(kind = 'scatter', x = 'MembersCount', y = 'totalkids')
df['TodCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['YoungCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['TeenCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['GradCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
df['TodCount'].sum()
df['TeenCount'].sum()
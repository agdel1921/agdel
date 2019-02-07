#@author: LatizeExpress

import pandas as pd
import numpy
import matplotlib
import matplotlib.pyplot as plt
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri

# Reading RDS object in pandas
pandas2ri.activate()
path1 = "C:/Users/LatizeExpress/NTUC/houseview_latize.rds"
readRDS = robjects.r['readRDS']
df1 = readRDS(path1)
df1 = pandas2ri.ri2py(df1)
# Writing ot csv file
df1.to_csv("house_trial_new.csv", index=False, encoding='utf8')
# General Information

df1.info()
df1.shape
df1.unique()
df1.ndim
df1.dtypes
pd.isnull(df).any
df1.describe()
df1.head(5)
df1.cov()
df1.corr()


# Missing Value report
df1.isnull().sum()
count_nan = len(df1) - df1.count()
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


missing_values_table(df1)

#df['Decision_maker'].isnull().sum()

##df['Decision_maker'].isnull().any()

#df.isnull().values.ravel().sum()


# Counting Unique records
col_uni_val={}
for i in df1.columns:
    col_uni_val[i] = len(df1[i].unique())

#Import pprint to display dic nicely:
import pprint
pprint.pprint(col_uni_val)

df1.apply(lambda x: x.nunique())
col_un= {}
for i in df1.columns:
    col_un[i]=df1[i].unique()
    print(i, col_un[i])
# writing csv of unique values
import pandas as pd
pd = pd.DataFrame.from_dict(col_un, orient='index')
pd.to_csv("house_unique.csv",sep=',')




for i in df1.columns:
    abc1 = df1['GI.active'].value_counts()


newdf1 = df1[df1.columns[21:23]]
for i in newdf1.columns:
    abc1 = newdf1.groupby(i).count()
print(abc1)









## looking unique for a specific column
#df['CustomerType'].unique()

#for col in df:
#    print(df[col].unique())

#df_dict = dict(zip([i for i in df.columns], [pd.DataFrame(df[i].unique(),columns=[i]) for i in df.columns]))
#
#for i in df.columns:
#    print(df_dict['CustomerSeqID'])
##X= df['H.ID']
##Y = ['CustomerSeqID']
##plt.scatter(df['H.ID'], Y, s=60, c='red', marker='^')
#
#
#
#df.plot(kind = 'scatter', x = 'MembersCount', y = 'totalkids')
#df['TodCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
#df['YoungCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
#df['TeenCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
#df['GradCount'].plot(kind = 'hist', bins = 50, figsize=(12,6))
#df['TodCount'].sum()
#df['TeenCount'].sum()

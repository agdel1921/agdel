# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 18:43:55 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np
path = "E:/NTUC/Processed/Categorical_output_/aff_freq.csv"
path1= "E:/NTUC/Processed/Categorical_output_/"
df = pd.read_csv(path, low_memory = True)
df1 = df1.drop(df1.columns[0], axis =1)
df1.head(2)
#df2 = df1[(df1["totalpremium"]>1000000)]
len(df1)
#df1.to_csv(path1+"aff_final.csv", header = True, index = False)
pd.cut(df1['count.17'], 15).head()
df1['AgePH'].min()
df1['AgePH'].max()
pd.cut(df1['totalpremium'], 15).head()
custom_bucket_array = np.linspace(1,5000000,10000)
custom_bucket_array

df1['premium bucket'] = pd.cut(df1['count.17'], custom_bucket_array)

df1['premium total'] = pd.cut(df1['totalpremium'], custom_bucket_array)




df['chi'] = pd.cut(df['chi'], custom_bucket_array)
df1






import matplotlib.pyplot as plt
#%matplotlib inline

plt.style.use('ggplot')

a = df1.groupby('premium total').size()
b = df1.groupby('premium bucket').size()

categories = df1['premium total'].cat.categories
ind = np.array([x for x, _ in enumerate(categories)])
width = 0.35
plt.bar(ind, a, width, label='premium total')
plt.bar(ind + width, b, width,label='premium bucket')

plt.xticks(ind + width / 2, categories)
plt.legend(loc='best')
plt.xticks(rotation = 90)
plt.show()
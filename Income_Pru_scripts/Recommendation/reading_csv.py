# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 01:40:06 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy
df = pd.read_csv("categorical_output_customer_data.csv")
df_sub = df.iloc[:,2:]
df_sub = df_sub.drop(["entityid","count.2"],1)
df_sub =df_sub.iloc[:400000,:]
df_sub.to_csv("Description_sub.csv", index=False)
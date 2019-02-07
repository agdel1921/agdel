# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 00:37:21 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np
#from factor_analyzer import FactorAnalyzer

path = "E:/Working/INNERJOIN_WORKING/RefinedData_groupby6.csv"
path1= "E:/NTUC/Processed/Categorical_output_/"
df = pd.read_csv(path, low_memory = True)
df.head(0)
df = df[['customerseqid','totalpremium']].astype(int)
df['AggPremium'] = df.groupby('customerseqid')['totalpremium'].sum()

df1 = df[['customerseqid','totalpremium', 'AggPremium']].astype(int)
df.head(5)



df1 = df[['educationlevel','PolicyCount','DwellingTypeInfo','totalpremium', 'originalsumassured', 'vehbrand','vehtypename','vehcapacity', 'vehage', 'productsubcategory','travelcountry']]

numeric = df[['PolicyCount','totalpremium', 'originalsumassured','vehcapacity', 'vehage']]


# factor Analysis
fa = FactorAnalyzer()

fa.analyze(numeric, 3, rotation = None)

ans = fa.loadings

print(ans)

bca = fa.get_uniqueness()
print(bca)

xyz = fa.get_factor_variance()

print(xyz)
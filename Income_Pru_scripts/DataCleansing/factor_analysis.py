# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 22:16:04 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np
#from factor_analyzer import *


path = "E:/Working/INNERJOIN_WORKING/RefinedData_groupby6.csv"
path1= "E:/NTUC/Processed/Categorical_output_/"
df = pd.read_csv(path, low_memory = True)
df.head(0)

df1 = df[['educationlevel','PolicyCount','DwellingTypeInfo','totalpremium', 'originalsumassured', 'vehbrand','vehtypename','vehcapacity', 'vehage', 'productsubcategory','travelcountry']]

fa = FactorAnalyzer()

fa.analyze(df1, 3, rotation = None)

ans = fa.loadings

print(ans)

bca = fa.get_uniqueness()
print(bca)

xyz = fa.get_factor_variance()

print(xyz)

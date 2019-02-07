# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 22:16:04 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
#from factor_analyzer import FactorAnalyzer
from sklearn.feature_selection import RFE

path = "E:/Working/INNERJOIN_WORKING/RefinedData_groupby6.csv"
path1= "E:/NTUC/Processed/Categorical_output_/"
df = pd.read_csv(path, low_memory = True)
df.head(0)

df1 = df[['educationlevel','PolicyCount','DwellingTypeInfo','totalpremium', 'originalsumassured', 'vehbrand','vehtypename','vehcapacity', 'vehage', 'productsubcategory','travelcountry']]


# checking the percentage of missing values in each variable
a = df1.isnull().sum()/len(df1)*100


# saving column names in a variable
variables = df1.columns
variable = [ ]
for i in range(0,12):
    if a[i]<=90:   #setting the threshold as 50%
        variable.append(variables[i])


#Variance
variance = df1.var()

######
numeric = df[['PolicyCount','totalpremium', 'originalsumassured','vehcapacity', 'vehage']]
b = numeric.isnull().sum()/len(df1)*100
df3 = df3.drop(df3.columns[3], axis =1)
df3.isnull().sum()/len(df1)*100
var1 = numeric.var()
numeric = numeric.columns
variable1 = [ ]
for i in range(0,len(var1)):
    if var1[i]>=10:   #setting the threshold as 10%
       variable1.append(numeric[i+1])

#correlation

numeric.corr()








# factor Analysis
fa = FactorAnalyzer()

fa.analyze(df1, 3, rotation = None)

ans = fa.loadings

print(ans)

bca = fa.get_uniqueness()
print(bca)

xyz = fa.get_factor_variance()

print(xyz)


# Random Forest

model = RandomForestRegressor(random_state=1, max_depth=10)
df1=pd.get_dummies(df1)
df2 = pd.get_dummies(numeric)
model.fit(df3,df.totalpremium)
##Not Suitable as datapoints have null values
features = df1.columns
importances = model.feature_importances_
indices = np.argsort(importances)[-9:]  # top 10 features
plt.title('Feature Importances')
plt.barh(range(len(indices)), importances[indices], color='b', align='center')
plt.yticks(range(len(indices)), [features[i] for i in indices])
plt.xlabel('Relative Importance')
plt.show()

# Linear Regression

from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE
from sklearn import datasets
lreg = LinearRegression()
rfe = RFE(lreg, 10)
rfe = rfe.fit_transform(df3, df.totalpremium)
c = rfe.ranking_

#Forward Feature Selection

from sklearn.feature_selection import f_regression
ffs = f_regression(df1,df.totalpremium )

variable2 = [ ]
for i in range(0,len(df1.columns)-1):
    if ffs[0][i] >=10:
       variable2.append(df1.columns[i])



import pandas as pd
import numpy as np
from glob import glob
import cv2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 01:06:28 2018

@author: LatizeExpress
"""
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np


pathread =  "E:/NTUC/raw_data/Final/hh_result_final/FinalResults_with_Bucket/"

pathwrite =  "E:/NTUC/raw_data/clean_raw_data/Final_recom_data/"

amgPd = pd.read_csv(pathread+'final_data_recom.csv', low_memory = True)
amgPd.columns

amgPd['FinalCategory'] = amgPd.Category_list

amgPd_noHealth = amgPd.loc[~amgPd['Category_list'].isin(['Health'])]
amgPd_noHealth['FinalCategory'] = amgPd_noHealth['FinalCategory'].replace('Savings ','Savings')


amgPd_noHealth.info()
amgPd_noHealth.describe()

X, y = amgPd_noHealth.iloc[:,:-1],amgPd_noHealth.iloc[:,-1]


data_dmatrix = xgb.DMatrix(data=X,label=y)


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

xg_reg = xgb.XGBRegressor(objective ='reg:linear', colsample_bytree = 0.3, learning_rate = 0.1, max_depth = 5, alpha = 10, n_estimators = 10)

xg_reg.fit(X_train,y_train)

preds = xg_reg.predict(X_test)
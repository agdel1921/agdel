# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 13:44:48 2019

@author: LatizeExpress
"""
import pandas as pd
import numpy as np
import copy


pathread =  "E:/NTUC/raw_data/Final/hh_result_final/FinalResults_with_Bucket/"
pathwrite =  "E:/NTUC/raw_data/clean_raw_data/Final_recom_data/"
top_products_to_predict = 5

nb_Pd1 = pd.read_csv(pathread+'Finalsorted_result55TMP.csv', low_memory = True)
nb_Pd2 = pd.read_csv(pathread+'result_Validation281218.csv', low_memory = True)
len(nb_Pd1)
len(nb_Pd2)
nb_Pd1 = nb_Pd1.loc[~nb_Pd1['hid'].isin(nb_Pd2.hid)]
nb_Pd1.to_csv(pathread+'CF_final_recom_17012019.csv', header = True, index = False)
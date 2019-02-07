# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 09:38:39 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np

path_hid = "E:/NTUC/raw_data/Final/hh_result_final/hid_sample.csv"
path_samp ="E:/NTUC/raw_data/Final/hh_result_final/sampleData.csv"
path_cldata= "E:/NTUC/raw_data/clean_raw_data/customerview_houseview_merge.csv"
path_tran= "E:/NTUC/raw_data/clean_raw_data/uniqueIds_transaction_merge.csv"
path_cst= "E:/NTUC/raw_data/clean_raw_data/uniqueIds_customer_merge.csv"

def readfile(path):
    df = pd.read_csv(path, low_memory = True)
    return df

df_hid = readfile(path_hid)
df_samp = readfile(path_samp)
df_samp.columns
df_cldata = readfile(path_cldata)
df_cldata.columns
df_tran = readfile(path_tran)
df_tran.columns
df_cst = readfile(path_cst)
df_cst.columns
df_fnl = df_samp.merge(df_cldata, on = 'hid', how = 'left')
df_fnl.columns
df_fnl = df_fnl[df_fnl.CustomerStatus != 'ESTATE' ]
df_fnl = df_fnl.merge(df_tran, on = 'hid', how = 'left')
df_fnl.columns
df_fnl = df_fnl.drop_duplicates(subset=None, keep='first', inplace=False)
df_fnl = df_fnl.merge(df_cst, on = 'hid', how = 'left')
df_fnl.columns
df_fnl = df_fnl.drop_duplicates(subset=None, keep='first', inplace=False)
df_fnl.to_csv(path_out+"sampleData_HH.csv", header = True, index = False)
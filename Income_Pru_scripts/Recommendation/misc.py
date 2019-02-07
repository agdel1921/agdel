# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 17:25:03 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np
path_hid = "E:/NTUC/raw_data/clean_raw_data/houseview_clean.csv"
path_cst = "E:/NTUC/raw_data/clean_raw_data/customerview_clean.csv"
path_tran ="E:/NTUC/raw_data/clean_raw_data/transaction_clean.csv"

path_prod1 ="E:/NTUC/raw_data/clean_raw_data/product_clean.csv"

path_prod ="E:/NTUC/working/ProductClassification.csv"


def readfile(path):
    df = pd.read_csv(path, low_memory = True)
    return df

df_hid = readfile(path_hid)
df_cst = readfile(path_cst)
df_trn = readfile(path_tran)

df_prod = readfile(path_prod)
df_prod1 = readfile(path_prod1)
df_prod2 = df_prod1.merge(df_prod, on = 'productname', how = "left")
df_prod2.columns
df_prod2.to_csv(path+"productClassification.csv", index = False, header = True)

df_trn = df_trn[['policyseqid', 'totalpremium', 'sumassured', 'businesstype', 'productseqid', 'PolicyStatusCategory', 'customerseqid']]
df_trn.columns = ['policyseqid', 'totalpremium', 'sumassured', 'businesstype', 'productseqid', 'PolicyStatusCategory', 'CustomerSeqID']

df_cmp = df_hid.merge(df_cst, on = 'hid', how = 'left')
df_cmp.columns
len(df_cmp)
df_cmp = df_cmp.drop_duplicates(subset=None, keep='first', inplace=False)

df_cmp = df_cmp.merge(df_trn, on = 'CustomerSeqID', how = 'left')
df_cmp.columns
len(df_cmp)
df_cmp = df_cmp.drop_duplicates(subset=None, keep='first', inplace=False)



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
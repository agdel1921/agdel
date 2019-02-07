# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 16:31:59 2017

@author: Latize
"""

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import os
import time
import copy
import matplotlib.pyplot as plt
import collections


pathread =  "E:/NTUC/raw_data/Final/hh_result_final/FinalResults_with_Bucket/"
pathwrite =  "E:/NTUC/raw_data/clean_raw_data/Final_recom_data/"
df_segment = pd.read_csv(pathread + "MicroSegmentProfile_final.csv", low_memory = True)
df_segment.columns

os.chdir(pathread)

listPath = []
listPath.append(pathread)
listPath.append(pathwrite)

for pth in listPath:
    if not os.path.exists(pth):
        os.makedirs(pth)
        print ( "Created path "+pth)
    else:
        print (pth +" already exists")

#os.chdir(path1_crosstab)

dirs = [x[0] for x in os.walk(pathwrite)]
dirs = dirs[1:]
print (dirs)

amgPd = pd.read_csv(pathread+'final_data_temp_recom.csv', low_memory = True)
amgPd.columns
print (amgPd.shape)
amgPd.head()
custNum = list(amgPd.hid)
print (np.unique(np.array(amgPd.Category_list)))
amgPd['Category_list'] = amgPd['Category_list'].replace('Savings ','Savings')
# Removing Health
amgPd = amgPd[amgPd['Category_list'] != 'Health']
amgPd_catCount = amgPd.reset_index().groupby('hid')['Category_list'].count()
amgPd_catCount = amgPd_catCount.to_frame()
amgPd = amgPd.merge(amgPd_catCount, on = 'hid', how = 'left')
amgPd.columns = ['hid', 'customerseqid', 'customerstatus', 'genderph', 'policyseqid',
       'totalpremium', 'sumassured', 'productseqid', 'productname',
       'policystatuscategory', 'policytype', 'productline', 'productcategory',
       'productsubcategory', 'ismain', 'Category_list', 'householdid',
       'premiumbucket', 'PremiumCategory', 'EducationLevel', 'vehage',
       'vehClass', 'vehbrand', 'travelcountry', 'addr_type_desc',
       'DwellingTypeCategory', 'District_Iiving', 'vehtypename',
       'vehtypename_cat', 'Affluence_Bucket', 'gicount', 'licount', 'iscount',
       'membersactive', 'weight_productSubcategory',
       'productline_bucket_affinity', 'PRODUCT_SCORE_BUCKET_affinity',
       'Affinity_Bucket', 'customertype', 'MembersCount', 'TodCount',
       'YoungCount', 'TeenCount', 'GradCount', 'totalkids', 'maritalstatus',
       'AgeGroup', 'PH_AgeGroup', 'LifeStageBucket', 'FinalSegment',
       'MicroSegmentProfile', 'Category_count']

## Adding policy start date to eleminate 2015 and 2016 data from training data
df_policy = pd.read_csv(pathread + "policydate.csv", low_memory = True)
df_policy.columns
#Merging policy info with data policy start date
amgPd_w_time =amgPd.merge(df_policy, on = 'policyseqid', how = 'left')
amgPd_w_time.columns
amgPd_w_time.PolicyStartDate.unique()
len(amgPd_w_time)
# training data till 31/03/2016  # records
amgPd_w_time1 = amgPd_w_time[amgPd_w_time['PolicyStartDate'] < '2016-04-01 00:00:00.0000000']
##REmoving Health
amgPd_w_time1 = amgPd_w_time1[amgPd_w_time1['Category_list'] != 'Health']
amgPd_w_time1['Category_list'] = amgPd_w_time1['Category_list'].replace('Savings ','Savings')
amgPd_w_time1.to_csv(pathwrite+'training_Data_withTime2016.csv', header = True, index = False)

len(amgPd_w_time1)
# test data after 31/03/2018   #323313 records
amgPd_w_time2 = amgPd_w_time[amgPd_w_time['PolicyStartDate'] > '2016-03-31 00:00:00.0000000']
amgPd_w_time2['Category_list'] = amgPd_w_time2['Category_list'].replace('Savings ','Savings')
amgPd_w_time2 = amgPd_w_time2[amgPd_w_time2['Category_list'] != 'Health']
amgPd_w_time2.to_csv(pathwrite+'test_Data_withTime2016_nohealth_Full.csv', header = True, index = False)

len(amgPd_w_time2)
#amgPd['fullProdName'] = amgPd['productseqid']+' '+amgPd['productname']

### Feature sets
amgPd_sgmt = amgPd[['MicroSegmentProfile','productname']]
amgPd_sgmt_count = amgPd[['MicroSegmentProfile','Category_count']]
amgPd_hid = amgPd[['hid','productname']]
amgPd_hid_count = amgPd[['hid','Category_count']]
amgPd_general = amgPd[['hid', 'totalpremium', 'productseqid', 'productname',
       'policystatuscategory', 'productline', 'productcategory',
       'productsubcategory', 'ismain', 'Category_list', 'premiumbucket', 'PremiumCategory', 'EducationLevel', 'DwellingTypeCategory', 'District_Iiving', 'Affluence_Bucket', 'gicount', 'licount', 'iscount', 'membersactive', 'weight_productSubcategory',
       'productline_bucket_affinity', 'PRODUCT_SCORE_BUCKET_affinity',
       'Affinity_Bucket', 'MembersCount', 'TodCount', 'YoungCount', 'TeenCount', 'GradCount', 'totalkids', 'maritalstatus','AgeGroup', 'PH_AgeGroup', 'LifeStageBucket', 'FinalSegment',
       'MicroSegmentProfile', 'Category_count']]
amgPd_segment_gen = amgPd[['hid', 'productname','productline', 'Category_list', 'premiumbucket', 'PremiumCategory', 'EducationLevel', 'DwellingTypeCategory', 'District_Iiving', 'Affluence_Bucket', 'membersactive','Affinity_Bucket', 'MembersCount', 'TodCount', 'YoungCount', 'TeenCount', 'GradCount', 'totalkids', 'maritalstatus','AgeGroup', 'PH_AgeGroup', 'LifeStageBucket', 'FinalSegment','MicroSegmentProfile', 'Category_count']]

## Training and Test data
temp = np.random.rand(len(amgPd)) < 0.6
amgPd_training = amgPd[temp]
amgPd_training.to_csv(pathwrite+'training_randomData.csv', header = True, index = False)
amgPd_test = amgPd[~temp]
amgPd_test.to_csv(pathwrite+'test_randomData.csv', header = True, index = False)
### 1. hid Vs Category_list
user_u = list(sorted(amgPd.hid.unique()))
item_u = list(sorted(amgPd.Category_list.unique()))

row = amgPd.hid.astype('category', categories=user_u).cat.codes
col = amgPd.Category_list.astype('category', categories=item_u).cat.codes

data = np.array([1 for k in range(len(amgPd))])

sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_u), len(item_u)))

df_tmp1 = pd.SparseDataFrame([pd.SparseSeries(sparse_matrix[i].toarray().ravel(), fill_value=0) for i in np.arange(sparse_matrix.shape[0])],index=user_u, columns=item_u, default_fill_value=0)
finCols = ['hid']
len(finCols)
finCols.extend(df_tmp1.columns)
len(finCols)

dfMtrx = np.empty(shape = (df_tmp1.shape[0]+1,df_tmp1.shape[1]+1), dtype=np.ndarray)
dfMtrx[:1,:][0] = finCols
dfMtrx[1:,0] = user_u
dfMtrx[1:,1:] = df_tmp1.values
print(dfMtrx.shape)

np.savetxt(pathwrite+'Final_Data_recom1_fin.csv', dfMtrx, delimiter=",",fmt='%s')


### 1.1 hid Vs Category_list training data
user_u = list(sorted(amgPd_training.hid.unique()))
item_u = list(sorted(amgPd_training.Category_list.unique()))

row = amgPd_training.hid.astype('category', categories=user_u).cat.codes
col = amgPd_training.Category_list.astype('category', categories=item_u).cat.codes

data = np.array([1 for k in range(len(amgPd_training))])

sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_u), len(item_u)))

df_tmp1 = pd.SparseDataFrame([pd.SparseSeries(sparse_matrix[i].toarray().ravel(), fill_value=0) for i in np.arange(sparse_matrix.shape[0])],index=user_u, columns=item_u, default_fill_value=0)
finCols = ['hid']
len(finCols)
finCols.extend(df_tmp1.columns)
len(finCols)
dfMtrx = np.empty(shape = (df_tmp1.shape[0]+1,df_tmp1.shape[1]+1), dtype=np.ndarray)
dfMtrx[:1,:][0] = finCols
dfMtrx[1:,0] = user_u
dfMtrx[1:,1:] = df_tmp1.values
print(dfMtrx.shape)

np.savetxt(pathwrite+'training_recom1_final.csv', dfMtrx, delimiter=",",fmt='%s')




### 1.2 hid Vs Category_list training data with policy date till 31/03/2018
user_u = list(sorted(amgPd_w_time1.hid.unique()))
item_u = list(sorted(amgPd_w_time1.Category_list.unique()))

row = amgPd_w_time1.hid.astype('category', categories=user_u).cat.codes
col = amgPd_w_time1.Category_list.astype('category', categories=item_u).cat.codes

data = np.array([1 for k in range(len(amgPd_w_time1))])

sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_u), len(item_u)))

df_tmp1 = pd.SparseDataFrame([pd.SparseSeries(sparse_matrix[i].toarray().ravel(), fill_value=0) for i in np.arange(sparse_matrix.shape[0])],index=user_u, columns=item_u, default_fill_value=0)
finCols = ['hid']
len(finCols)
finCols.extend(df_tmp1.columns)
len(finCols)
dfMtrx = np.empty(shape = (df_tmp1.shape[0]+1,df_tmp1.shape[1]+1), dtype=np.ndarray)
dfMtrx[:1,:][0] = finCols
dfMtrx[1:,0] = user_u
dfMtrx[1:,1:] = df_tmp1.values
print(dfMtrx.shape)

np.savetxt(pathwrite+'training_recom1_no_Health_withTime2016.csv', dfMtrx, delimiter=",",fmt='%s')


### 1.3 hid Vs Category_list test data with policy date till 31/03/2018
user_u = list(sorted(amgPd_w_time2.hid.unique()))
item_u = list(sorted(amgPd_w_time2.Category_list.unique()))

row = amgPd_w_time2.hid.astype('category', categories=user_u).cat.codes
col = amgPd_w_time2.Category_list.astype('category', categories=item_u).cat.codes

data = np.array([1 for k in range(len(amgPd_w_time2))])

sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_u), len(item_u)))

df_tmp1 = pd.SparseDataFrame([pd.SparseSeries(sparse_matrix[i].toarray().ravel(), fill_value=0) for i in np.arange(sparse_matrix.shape[0])],index=user_u, columns=item_u, default_fill_value=0)
finCols = ['hid']
len(finCols)
finCols.extend(df_tmp1.columns)
len(finCols)
dfMtrx = np.empty(shape = (df_tmp1.shape[0]+1,df_tmp1.shape[1]+1), dtype=np.ndarray)
dfMtrx[:1,:][0] = finCols
dfMtrx[1:,0] = user_u
dfMtrx[1:,1:] = df_tmp1.values
print(dfMtrx.shape)

np.savetxt(pathwrite+'test_recom1_final_withTime2016.csv', dfMtrx, delimiter=",",fmt='%s')



### 2. microsegment Vs Category_list
user_u = list(sorted(amgPd.MicroSegmentProfile.unique()))
item_u = list(sorted(amgPd.Category_list.unique()))

row = amgPd.MicroSegmentProfile.astype('category', categories=user_u).cat.codes
col = amgPd.Category_list.astype('category', categories=item_u).cat.codes

data = np.array([1 for k in range(len(amgPd))])

sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_u), len(item_u)))

df_tmp1 = pd.SparseDataFrame([pd.SparseSeries(sparse_matrix[i].toarray().ravel(), fill_value=0) for i in np.arange(sparse_matrix.shape[0])],index=user_u, columns=item_u, default_fill_value=0)
finCols = ['MicroSegmentProfile']
len(finCols)
finCols.extend(df_tmp1.columns)
len(finCols)

dfMtrx = np.empty(shape = (df_tmp1.shape[0]+1,df_tmp1.shape[1]+1), dtype=np.ndarray)
dfMtrx[:1,:][0] = finCols
dfMtrx[1:,0] = user_u
dfMtrx[1:,1:] = df_tmp1.values
print(dfMtrx.shape)

np.savetxt(pathwrite+'MicroSegmentProfile_recom1_fin.csv', dfMtrx, delimiter=",",fmt='%s')

### 3. hid Vs productname
user_u = list(sorted(amgPd.hid.unique()))
item_u = list(sorted(amgPd.productname.unique()))

row = amgPd.hid.astype('category', categories=user_u).cat.codes
col = amgPd.productname.astype('category', categories=item_u).cat.codes

data = np.array([1 for k in range(len(amgPd))])

sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_u), len(item_u)))

df_tmp1 = pd.SparseDataFrame([pd.SparseSeries(sparse_matrix[i].toarray().ravel(), fill_value=0) for i in np.arange(sparse_matrix.shape[0])],index=user_u, columns=item_u, default_fill_value=0)
finCols = ['hid']
len(finCols)
finCols.extend(df_tmp1.columns)
len(finCols)

dfMtrx = np.empty(shape = (df_tmp1.shape[0]+1,df_tmp1.shape[1]+1), dtype=np.ndarray)
dfMtrx[:1,:][0] = finCols
dfMtrx[1:,0] = user_u
dfMtrx[1:,1:] = df_tmp1.values
print(dfMtrx.shape)

np.savetxt(pathwrite+'hid_productName_recom_final.csv', dfMtrx, delimiter=",",fmt='%s')


### 4. microsegment Vs productname
user_u = list(sorted(amgPd.MicroSegmentProfile.unique()))
item_u = list(sorted(amgPd.productname.unique()))

row = amgPd.MicroSegmentProfile.astype('category', categories=user_u).cat.codes
col = amgPd.productname.astype('category', categories=item_u).cat.codes

data = np.array([1 for k in range(len(amgPd))])

sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_u), len(item_u)))

df_tmp1 = pd.SparseDataFrame([pd.SparseSeries(sparse_matrix[i].toarray().ravel(), fill_value=0) for i in np.arange(sparse_matrix.shape[0])],index=user_u, columns=item_u, default_fill_value=0)
finCols = ['MicroSegmentProfile']
len(finCols)
finCols.extend(df_tmp1.columns)
len(finCols)

dfMtrx = np.empty(shape = (df_tmp1.shape[0]+1,df_tmp1.shape[1]+1), dtype=np.ndarray)
dfMtrx[:1,:][0] = finCols
dfMtrx[1:,0] = user_u
dfMtrx[1:,1:] = df_tmp1.values
print(dfMtrx.shape)

np.savetxt(pathwrite+'MicroSegmentProfile_product_recom1_fin.csv', dfMtrx, delimiter=",",fmt='%s')



#whitelist = ['gc', 'whitelist','path_prog']
#
#for name in locals().keys():
#    if not name.startswith('_') and name not in whitelist:
#        del locals()[name]
#
#execfile(path_prog+'3_h1b1_2_ag_170718.py')
#
#
import gc
gc.collect()

## additional stuff to identify the reasons of each product recommendation

amgPd.columns
amgPd.Category_list.unique()
amgPd_savings = amgPd[amgPd['Category_list']=='Savings']
amgPd_annuity = amgPd.loc[amgPd['Category_list'].isin(['Annuity'])]
amgPd_protection = amgPd.loc[~amgPd['Category_list'].isin(['Annuity','Health', 'Savings', 'Savings ', 'ILP', 'Others' ])]
amgPd_savings = amgPd.loc[~amgPd['Category_list'].isin(['Health','Protection', 'ILP', 'Annuity','Others' ])]
amgPd_savings['Category_list'] = amgPd_savings['Category_list'].replace('Savings ','Savings')
amgPd_ILP = amgPd.loc[~amgPd['Category_list'].isin(['Health', 'Savings', 'Protection', 'Savings ','Annuity', 'Others' ])]
amgPd_others = amgPd.loc[~amgPd['Category_list'].isin(['Health', 'Savings', 'Protection', 'Savings ', 'ILP', 'Annuity' ])]

amgPd_savings.to_csv(pathread+'savingsonly.csv', header = True, index = False)
amgPd_annuity.to_csv(pathread+'annuityonly.csv', header = True, index = False)
amgPd_protection.to_csv(pathread+'protectiononly.csv', header = True, index = False)
amgPd_ILP.to_csv(pathread+'ILPonly.csv', header = True, index = False)
amgPd_others.to_csv(pathread+'otherssonly.csv', header = True, index = False)

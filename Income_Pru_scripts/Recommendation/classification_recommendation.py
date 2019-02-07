# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 12:11:07 2018

@author: LatizeExpress
"""
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
import matplotlib.pylab as plt
from sklearn.model_selection  import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import sklearn.metrics

pathread =  "E:/NTUC/raw_data/Final/hh_result_final/FinalResults_with_Bucket/"
amgPd = pd.read_csv(pathread+'final_data_recom.csv', low_memory = True)
amgPd.columns
print (amgPd.shape)
custNum = list(amgPd.hid)
print (np.unique(np.array(amgPd.Category_list)))
amgPd['Category_list'] = amgPd['Category_list'].replace('Savings ','Savings')
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


amgPd.dtypes

#Do summary statistics analysis of the data
amgPd.describe()

crl = amgPd.corr() #[‘Category_count’]
#Drop columns with low correlation

predictors = prospect_data[[‘REVIEWS’,’BOUGHT_TOGETHER’,’COMPARE_SIMILAR’,’WARRANTY’,’SPONSORED_LINKS’]]

targets = prospect_data.BUY

pred_train, pred_test, tar_train, tar_test = train_test_split(predictors, targets, test_size=.3)

print( “Predictor — Training : “, pred_train.shape, “Predictor — Testing : “, pred_test.shape )

from sklearn.naive_bayes import GaussianNB

classifier=GaussianNB()

classifier=classifier.fit(pred_train,tar_train)

predictions=classifier.predict(pred_test)

#Analyze accuracy of predictions

sklearn.metrics.confusion_matrix(tar_test,predictions)

sklearn.metrics.accuracy_score(tar_test, predictions)

pred_prob=classifier.predict_proba(pred_test)

pred_prob[0,1]

browsing_data = np.array([0,0,0,0,0]).reshape(1, -1)

print(“New visitor: propensity :”,classifier.predict_proba(browsing_data)[:,1]

browsing_data = np.array([0,0,1,0,0]).reshape(1, -1)

print(“After checking similar products: propensity :”,classifier.predict_proba(browsing_data)[:,1] )

browsing_data = np.array([1,0,1,0,0]).reshape(1, -1)

print(“After checking reviews: propensity :”,classifier.predict_proba(browsing_data)[:,1] )



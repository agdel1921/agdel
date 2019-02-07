# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 13:49:34 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np
import copy
path_ls = "E:/NTUC/raw_data/Final/hh_result_final/FinalResults_with_Bucket/hh_lifeStage_result_score_broad_Final.csv"
path_affl ="E:/NTUC/raw_data/Final/hh_result_final/FinalResults_with_Bucket/Household_Affluence_Result.csv"
path_afi= "E:/NTUC/raw_data/Final/hh_result_final/FinalResults_with_Bucket/Household_Affinity_Result_with_bucket_v1.1.csv"


def readfile(path):
    df = pd.read_csv(path, low_memory = True)
    return df

# Reading lifestage file
df_ls = readfile(path_ls)
len(df_ls)
df_ls.columns

df_ls = df_ls[['hid', 'customertype', 'MembersCount', 'TodCount',
       'YoungCount', 'TeenCount', 'GradCount', 'totalkids', 'maritalstatus',
       'AgeGroup', 'PH_AgeGroup','FamilyGrp_status']]

df_ls.columns = ['hid', 'customertype', 'MembersCount', 'TodCount',
       'YoungCount', 'TeenCount', 'GradCount', 'totalkids', 'maritalstatus',
       'AgeGroup', 'PH_AgeGroup','LifeStageBucket']

# Reading affluence file
df_affl = readfile(path_affl)
len(df_affl)
df_affl.columns
df_affl = df_affl[['hid', 'premiumbucket', 'PremiumCategory', 'EducationLevel',
       'vehage', 'vehClass', 'vehbrand', 'travelcountry', 'addr_type_desc',
       'DwellingTypeCategory', 'District_Iiving', 'vehtypename','vehtypename_cat', 'Bucket']]
df_affl.columns = ['hid', 'premiumbucket', 'PremiumCategory', 'EducationLevel',
       'vehage', 'vehClass', 'vehbrand', 'travelcountry', 'addr_type_desc',
       'DwellingTypeCategory', 'District_Iiving', 'vehtypename','vehtypename_cat', 'Affluence_Bucket']

#Reading affinity file
df_ffi = readfile(path_afi)
len(df_ffi)
df_ffi.columns
df_ffi = df_ffi[['hid', 'gicount', 'licount', 'iscount', 'membersactive',
       'weight_productSubcategory', 'Final_productline_bucket','Final_Product_Score_Bucket', 'FinalBucket']]

df_ffi.columns = ['hid', 'gicount', 'licount', 'iscount', 'membersactive',
       'weight_productSubcategory', 'productline_bucket_affinity',      'PRODUCT_SCORE_BUCKET_affinity', 'Affinity_Bucket']
#df_ffi_tmp['abc'] = df_affl.groupby('FinalAffluenceScore').quantile(q =[0,.25,.5,.75,1], axis = 1)

### microsegmentation
df_seg = df_affl.merge(df_ffi, on = 'hid', how = 'left')
df_seg = df_seg.merge(df_ls, on = 'hid', how = 'left')
df_seg.columns
# Concatenating different buckets
df_seg['FinalSegment'] = "Affluence: "+ df_seg['Affluence_Bucket'].map(str) + ", LifeStage: "+ df_seg['LifeStageBucket'].map(str) + ", Affinity: "+ df_seg['Affinity_Bucket'].map(str)

path_out = "E:/NTUC/raw_data/Final/hh_result_final/FinalResults_with_Bucket/"
df_seg.to_csv(path_out+"microsegment.csv", header = True, index = False)



# microsegment Score
path_pro = "E:/NTUC/raw_data/Final/hh_result_final/FinalResults_with_Bucket/microsegment.csv"
df_processed = readfile(path_pro)
df_processed.columns

path_score = "E:/NTUC/raw_data/Final/hh_result_final/FinalResults_with_Bucket/MicroSegmentCode_Final.csv"
df_score = readfile(path_score)

df_final = df_processed.merge(df_score, on = 'FinalSegment', how = 'left')
df_final.to_csv(path_out+"MicroSegmentProfile_final.csv", header = True, index = 'False')
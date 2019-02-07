# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 20:13:38 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np
import os


#path defination

path = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/HouseHold_FinalDataClean.csv"
path1 = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_premium_score_final.csv"
path2 = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/Premium_buckets.csv"
path3 = "E:/NTUC/raw_data/Final/FinalScore_v1.csv"
path_edu = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_education_data_final.csv"
path_veh = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_veh_age_data_final.csv"
path_brand = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_veh_brand_data_final.csv"
path_country = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_travelCountry_data_final.csv"
path_dwelling = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_addresstype_data_final.csv"
path_product = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_product_score_final.csv"
path_postal = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_postal_data_final.csv"
path_veh_type = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_vehicleTypeName.csv"
vehage = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_vehage_score_final.csv"
edulavel = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_edu_score_final.csv"
vehBrand = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_vehbrand_score_final.csv"
travel = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/HH_COUNTRY_SCORE_final.csv"
dwel = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_addresstype_score_final.csv"
post = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_postal_score_final.csv"
product = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_product_score_final.csv"
vehtype = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_vehtypename_score_final.csv"
#dwel = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_dwelling_final.csv"

## Reading files in pandas data frame
df = pd.read_csv(path, low_memory = True)
# few updates the column names to be modified or Changed to NA
#df.addr_type_desc.unique()
#df['addr_type_desc'] = df.addr_type_desc.replace('', 'NA')
#df.columns
#df.addr_type_desc.unique()
#df.to_csv(path+"dwellingclean.csv", header = True, index=False)
len(df)
df.columns
df = df.drop_duplicates(subset=None, keep='first', inplace=False)

######## Generating PremiumScore to all hh data #############
#Reading Premium_Score file
df1 = pd.read_csv(path1, low_memory = True)
df1.columns

#Reading hh data with Premium_Bucket
df2 = pd.read_csv(path2, low_memory = True)
df2.columns
# Lookup / merge
result = df2.merge(df1, on='premiumbucket', how ='left'  )
result.columns
result = result.fillna(0)
len(result)
result = result.drop_duplicates(subset=None, keep='first', inplace=False)
len(result)
###################################################################

####### Generating education Score to all hh data #############
#Reading hh_educationdata
edu = pd.read_csv(path_edu, low_memory = True)
edu.columns
# Merging hh_educationData with result data
result = result.merge(edu, on='hid', how ='left'  )
result.columns
len(result)
result = result.drop_duplicates(subset=None, keep='first', inplace=False)
len(result)


#reading education_score data
edu_score = pd.read_csv(edulavel, low_memory = True)
edu_score.columns

# Merging education_score with result data
result = result.merge(edu_score, on='educationlevel', how ='left'  )
result.columns
len(result)
result = result.drop_duplicates(subset=None, keep='first', inplace=False)
len(result)
result = result.fillna(0)
result1 = result.groupby('hid', group_keys=False).apply(lambda x: x.loc[x.FinalScoreEdu.idxmax()])
len(result1)
type(result1)
result1.columns
###################################################################################
####### Generating hh_vehAge Score to all hh data #############
#Reading hh_vehAge
veh_age = pd.read_csv(path_veh, low_memory = True)
veh_age.columns
# Merging veh_age with result1 data
result1 = result1.merge(veh_age, on='hid', how ='left'  )
result1.columns
len(result1)
result1 = result1.drop_duplicates(subset=None, keep='first', inplace=False)
len(result1)


#reading hh_vehAge_score data
vegAge_score = pd.read_csv(vehage, low_memory = True)
vegAge_score.columns

# Merging hh_vehAge_score with result1 data
result1 = result1.merge(vegAge_score, on='vehage', how ='left'  )
result1.columns
result1 = result1.fillna(0)
len(result1)
result1 = result1.drop_duplicates(subset=None, keep='first', inplace=False)
len(result1)
result1 = result1.groupby('hid', group_keys=False).apply(lambda x: x.loc[x.finalscore_vehage.idxmax()])
len(result1)
result1.columns
##############################################################################

####### Generating hh_vhbrand Score to all hh data #############
#Reading hh_vhbrand
veh_brand = pd.read_csv(path_brand, low_memory = True)
veh_brand.columns
# Merging hh_vhbrand with result1 data
result1 = result1.merge(veh_brand, on='hid', how ='left'  )
result1.columns
len(result1)
result1 = result1.drop_duplicates(subset=None, keep='first', inplace=False)
len(result1)

#reading hh_vhbrand_score data
vegbrand_score = pd.read_csv(vehBrand, low_memory = True)
vegbrand_score.columns

# Merging hh_vhbrand_score with result1 data
result1 = result1.merge(vegbrand_score, on='vehbrand', how ='left'  )
result1 = result1.fillna(0)
result1.columns
len(result1)
result1 = result1.drop_duplicates(subset=None, keep='first', inplace=False)
len(result1)
result1 = result1.groupby('hid', group_keys=False).apply(lambda x: x.loc[x.vehbrand_finalScore.idxmax()])
len(result1)
result1.columns
##############################################################################

####### Generating hh_country Score to all hh data #############
#Reading hh_country
trav_country = pd.read_csv(path_country, low_memory = True)
trav_country.columns
# Merging hh_trav_country with result1 data
result1 = result1.merge(trav_country, on='hid', how ='left'  )
result1.columns
len(result1)
result1 = result1.drop_duplicates(subset=None, keep='first', inplace=False)
len(result1)

#reading hh_trav_country_score data
trav_country_score = pd.read_csv(travel, low_memory = True)
trav_country_score.columns

# Merging hh_vhbrand_score with result1 data
result1 = result1.merge(trav_country_score, on='travelcountry', how ='left'  )
result1 = result1.fillna(0)
result1.columns
len(result1)
result1 = result1.drop_duplicates(subset=None, keep='first', inplace=False)
len(result1)
result1 = result1.groupby('hid', group_keys=False).apply(lambda x: x.loc[x.FinalScoreCountry.idxmax()])
len(result1)
#result1.columns

##############################################################################

####### Generating hh_product Score to all hh data #############
#Reading hh_product
hh_product = pd.read_csv(path_product, low_memory = True)
hh_product.columns
# Merging hh_product with result1 data
result1 = result1.merge(hh_product, on='hid', how ='left'  )
result1.columns
len(result1)
result1 = result1.drop_duplicates(subset=None, keep='first', inplace=False)
len(result1)
result1 = result1.fillna(0)
result1 = result1.groupby('hid', group_keys=False).apply(lambda x: x.loc[x.ProductScore.idxmax()])
len(result1)
result1.columns

##############################################################################

####### Generating hh_dwellingInfo Score to all hh data #############
#Reading hh_dwellingInfo
dwellingInfo = pd.read_csv(path_dwelling, low_memory = True)
dwellingInfo.columns
# Merging hh_dwellingInfo with result1 data
result1 = result1.merge(dwellingInfo, on='hid', how ='left'  )
result1.columns
len(result1)
result1 = result1.drop_duplicates(subset=None, keep='first', inplace=False)
len(result1)

#reading hh_dwellingInfo_score data
dwellingInfo_score = pd.read_csv(dwel, low_memory = True)
dwellingInfo_score.columns

# Merging hh_dwellingInfo_score with result1 data
result1 = result1.merge(dwellingInfo_score, on='addr_type_desc', how ='left')
result1 = result1.fillna(0)
result1.columns
len(result1)
result1 = result1.drop_duplicates(subset=None, keep='first', inplace=False)
len(result1)
result1 = result1.groupby('hid', group_keys=False).apply(lambda x: x.loc[x.final_score_address.idxmax()])
len(result1)
result1.columns

##############################################################################

####### Generating hh_postalCode Score to all hh data #############
#Reading hh_postalCode
hh_postalCode = pd.read_csv(path_postal, low_memory = True)
#hh_postalCode['postalcode'] = hh_postalCode['postalcode'].apply(int)
hh_postalCode.columns

# Merging hh_dwellingInfo with result1 data
result1 = result1.merge(hh_postalCode, on='hid', how ='left'  )
result1.columns

#hh_postalCode = hh_postalCode
#reading hh_postalCode_score data
hh_postalCode_score = pd.read_csv(post, low_memory = True)
hh_postalCode_score.columns
#hh_postalCode_score['postalcode'] = hh_postalCode_score['postalcode'].apply(int)
# Merging hh_postalCode_score with result1 data
result1 = result1.merge(hh_postalCode_score, on='postalcode', how ='left')
result1 = result1.fillna(0)
result1.columns
len(result1)
result1 = result1.drop_duplicates(subset=None, keep='first', inplace=False)
len(result1)
result1 = result1.groupby('hid', group_keys=False).apply(lambda x: x.loc[x.FinalScore_Post.idxmax()])
len(result1)

##############################################################################

####### Generating hh_vehType Score to all hh data #############
#Reading hh_vehType
hh_vehType = pd.read_csv(path_veh_type, low_memory = True)
hh_vehType.columns
# Merging hh_dwellingInfo with result1 data
result1 = result1.merge(hh_vehType, on='hid', how ='left'  )
result1.columns
len(result1)
result1 = result1.drop_duplicates(subset=None, keep='first', inplace=False)
len(result1)


#reading hh_dwellingInfo_score data
vehType_score = pd.read_csv(vehtype, low_memory = True)
vehType_score.columns

# Merging hh_dwellingInfo_score with result1 data
result1 = result1.merge(vehType_score, on='vehtypename', how ='left'  )
result1 = result1.fillna(0)
result1.columns
len(result1)
result1 = result1.drop_duplicates(subset=None, keep='first', inplace=False)
len(result1)
result1 = result1.groupby('hid', group_keys=False).apply(lambda x: x.loc[x.Vehtype_finalScore.idxmax()])
len(result1)
result1.columns

##############################################################################


#CalculatingFinalScore: Vehicle
result1['FinalVehScore'] = result1['finalscore_vehage']+result1['vehbrand_finalScore']+result1['Vehtype_finalScore']
# Final Area Score : DwellingType and Area together
result1['FinalAreaScore'] = result1['final_score_address']+result1['FinalScore_Post']

result1['FinalPremiumWeight'] = result1['FinalScore_Premium']*0.35
## add '0' to all blanks if any
result1['FinalAreaWeight'] = result1['FinalAreaScore']*0.25
result1['FinalVehWeight'] = result1['FinalVehScore']*0.05
result1['FinalcountryWeight'] = result1['FinalScoreCountry']*0.05
result1['FinalEducationWeight'] = result1['FinalScoreEdu']*0.20
result1['FinalProductWeight'] = result1['ProductScore']*0.10

# Final Result Calculation

result1['FinalAffluenceScore'] = result1['FinalPremiumWeight'] + result1['FinalAreaWeight'] + result1['FinalVehWeight'] + result1['FinalcountryWeight'] + result1['FinalEducationWeight'] + result1['FinalProductWeight']

# Writhing Results
path_out = "E:/NTUC/raw_data/Final/hh_result_final/"

#result.head(5)
len(result1)
result1.to_csv(path_out+'hh_Affluence_final_Result.csv', header =True, index = False)


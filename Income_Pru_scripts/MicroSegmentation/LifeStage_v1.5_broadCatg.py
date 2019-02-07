# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 19:47:27 2018

@author: LatizeExpress
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 20:13:38 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np
import os


#path defination

#path = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/HouseHold_FinalDataClean.csv"


path = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/HouseHold_FinalDataClean.csv"
df = pd.read_csv(path, low_memory = True)
df.columns
#df_prod = df[['productname']]
#df_prod.to_csv(path+"productinfo.csv", header = True, index = False)
 #cleaning  customertype like 'CL', 'CO', etc.
df_tmp = df[['hid', 'customerseqid_x', 'customerstatus', 'genderph', 'ageph',
       'customertype']]
df_tmp = df[df.customertype != 'CO']
df_tmp = df_tmp[df.customertype != 'NM']
df_tmp = df_tmp[df.customertype != 'CL']
df_tmp = df_tmp[df.customertype != 'OT']
df_tmp.customertype.unique()
# copy the content
import copy
df = copy.deepcopy(df_tmp)

file_path =  "E:/NTUC/raw_data/clean_raw_data/"
uniID = pd.read_csv(file_path+"houseview_clean.csv", low_memory = True)
uniID.columns
uniID = uniID[[ 'hid', 'MembersCount', 'MembersActive',
       'TodCount', 'YoungCount', 'TeenCount', 'GradCount',  'totalkids','Total_Policies', 'Decision_maker']]

fin_df = df[['hid', 'customerseqid_x', 'customerstatus', 'genderph', 'ageph','customertype', 'totalpremium', 'productname', 'productcategory', 'vehbrand', 'vehtypename', 'policytype', 'policystatuscategory', 'educationlevel', 'postalcode',  'addr_type_desc']]

fin_df.columns = ['hid', 'customerseqid', 'customerstatus', 'genderph', 'ageph','customertype', 'totalpremium', 'productname', 'productcategory', 'vehbrand', 'vehtypename', 'policytype', 'policystatuscategory', 'educationlevel', 'postalcode',  'addr_type_desc']
# reading customer data
path = "E:/NTUC/raw_data/clean_raw_data/customer_clean.csv"
df = pd.read_csv(path, low_memory = True)
df.columns
cdata = df[['customerseqid', 'dateofbirth', 'gender',
        'maritalstatus']]
# generating age from the date of birth from customer data
cdata['dob'] = cdata['dateofbirth']
cdata['dob'] = pd.to_datetime(cdata['dob'],format='%Y-%m-%d')

import datetime as DT
now = pd.Timestamp(DT.datetime.now())
cdata['dob1'] = cdata['dob'].where(cdata['dob'] < now, cdata['dob'] -  np.timedelta64(100, 'Y'))   # 2
cdata['age'] = (now - cdata['dob1']).astype('<m8[Y]')    # 3
print(cdata['age'])
## counting nan in the age field Total 253398 nan are there
print(cdata['age'].isna().sum()) ## 253398
## counting '0' in the age value Total 1880 '0' values are there
len(cdata[cdata.age == 0])  ## 1880

## Replacing all nan values with 'NA'
cdata['age'] = cdata['age'].fillna('NA')
##creating a data of age == '0' records
cdata_zero = cdata[cdata.age == 0]

# merging houseview data
fin_df1 = fin_df.merge(uniID, on='hid', how ='left')
fin_df1.columns
len(fin_df1)
# merging customer data
fin_df2 = fin_df1.merge(cdata, on='customerseqid', how ='left')
fin_df2.columns
len(fin_df2)
fin_df2 = fin_df2[['hid', 'customerseqid', 'customerstatus', 'genderph', 'ageph',
       'customertype', 'totalpremium', 'productname', 'productcategory',
       'vehbrand', 'vehtypename', 'policytype', 'policystatuscategory',
       'educationlevel', 'postalcode', 'addr_type_desc', 'MembersCount',
       'MembersActive', 'TodCount', 'YoungCount', 'TeenCount', 'GradCount',
       'totalkids', 'Total_Policies', 'Decision_maker', 'dateofbirth',
       'gender', 'maritalstatus', 'age']]
fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)
len(fin_df2)
#fin_df2['age'] = fin_df2['age'].fillna(0)

path2 = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/Premium_buckets.csv"
#Reading hh data with Premium_Bucket
df2 = pd.read_csv(path2, low_memory = True)
df2.columns
fin_df2 = fin_df2.merge(df2, on='hid', how ='left')
fin_df2.columns
#fin_df2 = fin_df2.fillna('NA')
## Creating data for exploratory and weight framework
#fin_df3 = fin_df2.drop(['customerseqid'], axis = 1)
#fin_df3.to_csv(path2+"lifestageData.csv", index = False, header = True)
##len(fin_df3)

### Data Cleansing
fin_df2.policytype.unique()
fin_df2['ageph'] = fin_df2.ageph.replace('NA', 0)
fin_df2['policytype'] = fin_df2.policytype.replace('INDIVIDUAL','Individual')
fin_df2['customertype'] = fin_df2['customertype'].fillna('NA')
fin_df2.customertype.unique()
fin_df2.columns
fin_df2.ageph.unique()
fin_df2['ageph'] = fin_df2['ageph'].fillna(0)

###age group buckets
def agegrp_df(value):
    if int(value['age'] == 0 ):
        return "value NA or Insured New born baby"
    elif int(value['age'] < 6 and int (value['age']) > 0):
        return "toddler"
    elif int(value['age'] < 13 and int (value['age']) >5):
        return "Young child"
    elif int(value['age'] < 20 and int (value['age']) >12):
        return "Teen child"
    elif int(value['age'] < 31 and int (value['age']) >19):
        return "YoungCustomer"
    elif int(value['age'] < 51 and int (value['age']) >30):
        return "Matured Customer"
    elif int(value['age'] > 50) :
        return "Old Customer"
    else:
        return "Others"
### generating age group on the basis of current age
fin_df2['age'] =fin_df2['age'].replace('NA', 0)
fin_df2['AgeGroup'] = fin_df2.apply(agegrp_df, axis=1)
fin_df2.AgeGroup.unique()
fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)
len(fin_df2)

### ageph group buckets
def agegrp_df(value):
    if int(value['ageph'] == 0 ):
        return "value NA or Insured New born baby"
    elif int(value['ageph'] < 6 and int (value['ageph']) > 0):
        return "toddler"
    elif int(value['ageph'] < 13 and int (value['ageph']) >5):
        return "Young child"
    elif int(value['ageph'] < 20 and int (value['ageph']) >12):
        return "Teen child"
    elif int(value['ageph'] < 31 and int (value['ageph']) >19):
        return "YoungCustomer"
    elif int(value['ageph'] < 51 and int (value['ageph']) >30):
        return "Matured Customer"
    elif int(value['ageph'] > 50):
        return "Old Customer"
    else:
        return "Others"

### generating age group on the basis of ageph
fin_df2['ageph'] = fin_df2['ageph'].fillna(0)
fin_df2['ageph'] = fin_df2['ageph'].astype(np.int64)
fin_df2['PH_AgeGroup'] = fin_df2.apply(agegrp_df, axis=1)
fin_df2.PH_AgeGroup.unique()
fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)
len(fin_df2)
#########################################################
fin_df2['maritalstatus'] = fin_df2['maritalstatus'].fillna('NA')
########PH_Age and Marital Status

def agegrp_df(value):
    if (value['AgeGroup'] == 'value NA or Insured New born baby' ) and (value['maritalstatus'] == 'Single' or value['maritalstatus'] == 'Married' or value['maritalstatus'] == 'NA' or value['maritalstatus'] == 'Other'):
        return "New born baby family"
    elif(value['AgeGroup'] == 'value NA or Insured New born baby' or value['AgeGroup'] == 'Young child' or value['AgeGroup'] == 'YoungCustomer' or value['AgeGroup'] == 'Matured Customer' or value['AgeGroup'] == 'Old Customer' or value['AgeGroup'] == 'Teen child') and (value['maritalstatus'] == 'Divorce' or value['maritalstatus'] == 'Widow'):
        return "Divorced / Widowed family"
    elif(value['AgeGroup'] == 'Young child' or value['AgeGroup'] == 'Teen child') and (value['maritalstatus'] == 'Other' or value['maritalstatus'] == 'NA' or value['maritalstatus'] == 'Single' or value['maritalstatus'] == 'Married'):
        return "Family with teen/Young/Grad Kids"
    elif(value['AgeGroup'] == 'YoungCustomer' ) and (value['maritalstatus'] == 'Other' or value['maritalstatus'] == 'NA' or value['maritalstatus'] == 'Single' or value['maritalstatus'] == 'Married'):
        return "Young Family Customer"
    elif(value['AgeGroup'] == 'Matured Customer' ) and (value['maritalstatus'] == 'Other' or value['maritalstatus'] == 'NA' or value['maritalstatus'] == 'Single' or value['maritalstatus'] == 'Married'):
        return "Matured family customer"
    elif(value['AgeGroup'] == 'Old Customer' ) and (value['maritalstatus'] == 'Other' or value['maritalstatus'] == 'NA' or value['maritalstatus'] == 'Single' or value['maritalstatus'] == 'Married' ):      return "Old Customer Family"
    else:
        return "Small Family"

### generating age group on the basis of AgeGroup
fin_df2['Family_Marital_status'] = fin_df2.apply(agegrp_df, axis=1)
fin_df2.Family_Marital_status.unique()
fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)

#####Testing
#fin_df3 = fin_df2[['hid','maritalstatus','premiumbucket','PH_AgeGroup','AgeGroup', 'age', 'FamilyGrp_status']]
#fin_df3.to_csv(path_out+"hh_lifeStage_result_for_score_temp.csv", header = True, index = False)

#####################################################3
###MArital and kids

def agegrp_df(value):
    if (value['Family_Marital_status'] == 'Old Customer Family' ) and (value['totalkids'] == 0 ):
        return "Old family with no kids info"
    elif(value['Family_Marital_status'] == 'Old Customer Family' ) and (value['totalkids'] < 3 ):
        return "Old small family"
    elif(value['Family_Marital_status'] == 'Old Customer Family' ) and (value['totalkids'] > 2 ):
        return "Old large family"
    elif(value['Family_Marital_status'] == 'Matured family customer' ) and (value['totalkids'] == 0 ):
        return "Matured family with no kid info"
    elif(value['Family_Marital_status'] == 'Matured family customer' ) and (value['totalkids'] < 3 ):
        return "Matured small family"
    elif(value['Family_Marital_status'] == 'Matured family customer' ) and (value['totalkids'] > 2 ):
        return "Matured large Family"
    elif(value['Family_Marital_status'] == 'Divorced / Widowed family' ) and (value['totalkids'] == 0 ):
        return "Divorced / Widowed family with no kids info"
    elif(value['Family_Marital_status'] == 'Divorced / Widowed family' ) and (value['totalkids'] < 3 ):
        return "Divorced / Widowed Small Family"
    elif(value['Family_Marital_status'] == 'Divorced / Widowed family' ) and (value['totalkids'] > 2 ):
        return "Divorced / Widowed large Family"
    elif(value['Family_Marital_status'] == 'Young Family Customer' ) and (value['totalkids'] == 0 ):
        return "Young Family with no kids info"
    elif(value['Family_Marital_status'] == 'Young Family Customer' ) and (value['totalkids'] < 3):
        return "Young Small Family"
    elif(value['Family_Marital_status'] == 'Young Family Customer' ) and (value['totalkids'] > 2):
        return "Young large Family"
    elif(value['Family_Marital_status'] == 'New born baby family' ):
        return "Family with new born"
    elif(value['Family_Marital_status'] == 'Small Family' ):
        return "Small Family"
    elif(value['Family_Marital_status'] == 'Family with teen/Young/Grad Kids' ) and (value['totalkids'] < 3 or value['totalkids'] > 2):
        return "Small Family with teen/Young/Grad Kids"
    elif(value['Family_Marital_status'] == 'Family with teen/Young/Grad Kids' ) and (value['totalkids'] > 2):
        return "Large Family with teen/grad Kids"
    else:
        return "Other Family"

### generating age group on the basis of ageph
fin_df2['FamilyGrp_status'] = fin_df2.apply(agegrp_df, axis=1)
fin_df2.FamilyGrp_status.unique()
fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)

#####Testing
#fin_df3 = fin_df2[['hid','maritalstatus','premiumbucket','PH_AgeGroup','AgeGroup', 'age', 'FamilyGrp_status']]
#fin_df3.to_csv(path_out+"hh_lifeStage_result_for_score_temp.csv", header = True, index = False)


################################################################
#def agegrp_df(value):
#    if (value['FamilyGrp_status'] == 'Young Single' or value['FamilyGrp_status'] == 'Young Single large Family' or value['FamilyGrp_status'] == 'Young Single Customer no kids' or value['FamilyGrp_status'] == 'Young Single Small Family' or value['FamilyGrp_status'] == 'Young Divorsed / Widow Customer') and (value['TodCount'] == 0 or value['YoungCount'] == 0):
#        return "Young Family"
#    elif (value['FamilyGrp_status'] == 'Young Single' or value['FamilyGrp_status'] == 'Young Single large Family' or value['FamilyGrp_status'] == 'Young Single Customer no kids' or value['FamilyGrp_status'] == 'Young Single Small Family' or value['FamilyGrp_status'] == 'Young Divorsed / Widow Customer') and (value['TodCount'] == 0 or value['YoungCount'] == 0):
#        return "Young Parent family with Tod / Young"
#    elif (value['FamilyGrp_status'] == 'Young Single' or value['FamilyGrp_status'] == 'Young Single large Family' or value['FamilyGrp_status'] == 'Young Single Customer no kids' or value['FamilyGrp_status'] == 'Young Single Small Family' or value['FamilyGrp_status'] == 'Young Divorsed / Widow Customer') and (value['GradCount'] == 0 or value['TeenCount'] == 0):
#        return "Young Single Parent family with Teen / Grad kids"
#    elif value['FamilyGrp_status'] == 'Young Married Customer no kids' and (value['TodCount'] == 0 or value['YoungCount'] == 0):
#        return "Young Couple"
#    elif  (value['FamilyGrp_status'] == 'Young Small Family' or value['FamilyGrp_status'] == 'Young Married Small Family' or value['FamilyGrp_status'] == 'Young Divorsed / Widow Customer Small Family') and (value['TodCount'] > 0 or value['YoungCount'] >0) :
#        return "Young Small Family with Tod / Young"
#    elif  (value['FamilyGrp_status'] == 'Young Small Family' or value['FamilyGrp_status'] == 'Young Married Small Family' or value['FamilyGrp_status'] == 'Young Divorsed / Widow Customer Small Family') and (value['GradCount'] > 0 or value['TeenCount'] >0) :
#        return "Young Small Family with Teen / Grad kids"
#    elif  (value['FamilyGrp_status'] == 'Young Married large Family' or value['FamilyGrp_status'] == 'Young large Family' or value['FamilyGrp_status'] == 'Young Divorsed / Widow Customer large Family') and (value['TodCount'] > 0 or value['YoungCount'] > 0):
#        return "Young large Family with Tod / Young"
#    elif (value['FamilyGrp_status'] == 'Young Married large Family' or value['FamilyGrp_status'] == 'Young large Family' or value['FamilyGrp_status'] == 'Young Divorsed / Widow Customer large Family') and (value['TeenCount'] > 0 or value['GradCount'] > 0):
#        return "Young large Family with Teen / Grad kids"
#    elif  (value['FamilyGrp_status'] == 'Matured Single no kid' or value['FamilyGrp_status'] == 'Matured Single') and (value['TodCount'] == 0 or value['YoungCount'] == 0):
#        return "Matured Family"
#    elif  value['FamilyGrp_status'] == 'Matured Single Parent' and (value['TodCount'] > 0 or value['YoungCount'] > 0):
#        return "Matured Single Parent with Tod / Young family"
#    elif  value['FamilyGrp_status'] == 'Matured Single Parent' and (value['TeenCount'] > 0 or value['GradCount'] > 0):
#        return "Matured Single Parent with Teen / Grad kids family"
#    elif (value['FamilyGrp_status'] == 'Matured Couple no kid') and (value['TodCount'] == 0 or value['YoungCount'] == 0):
#        return "Matured Couple"
#    elif  (value['FamilyGrp_status'] == 'Matured Small Family' or value['FamilyGrp_status'] == 'Matured Single Small Family') and (value['TodCount'] > 0 or value['YoungCount'] >0) :
#        return "Matured Small Family with Tod / Young"
#    elif  (value['FamilyGrp_status'] == 'Matured Small Family' or value['FamilyGrp_status'] == 'Matured Single Small Family') and (value['TeenCount'] > 0 or value['GradCount'] >0) :
#        return "Matured Small Family with Teen / Grad kids"
#    elif  (value['FamilyGrp_status'] == 'Matured large Family' or value['FamilyGrp_status'] == 'Matured Single large Family') and (value['TodCount'] > 0 or value['YoungCount'] > 0):
#        return "Matured large Family with Tod / Young"
#    elif (value['FamilyGrp_status'] == 'Matured large Family' or value['FamilyGrp_status'] == 'Matured Single large Family') and (value['TeenCount'] > 0 or value['GradCount'] > 0):
#        return "Matured large Family with Teen / Grad kids"
#    elif  (value['FamilyGrp_status'] == 'Old Single no kid' or value['FamilyGrp_status'] == 'Single Senior Citizen Customer no kid' or value['FamilyGrp_status'] == 'Senior Citizen Divorsed / Widow Customer no kid' or value['FamilyGrp_status'] == 'Old Divorsed / Widow Customer no kid') and (value['TodCount'] == 0 or value['YoungCount'] == 0):
#        return "Old Family"
#    elif  value['FamilyGrp_status'] == 'Old Single Parent' and (value['TodCount'] > 0 or value['YoungCount'] > 0):
#        return "Old Single Parent with Tod / Young family"
#    elif  value['FamilyGrp_status'] == 'Old Single Parent' and (value['TeenCount'] > 0 or value['GradCount'] > 0):
#        return "Old Single Parent with Teen / Grad kids family"
#    elif (value['FamilyGrp_status'] == 'Old Couple no kid' or value['FamilyGrp_status'] == 'Senior Citizen Couple no kid') and (value['TodCount'] == 0 or value['YoungCount'] == 0):
#        return "Old Couple"
#    elif  (value['FamilyGrp_status'] == 'Old Small Family' or value['FamilyGrp_status'] == 'Old Divorsed / Widow Customer Small Family' or value['FamilyGrp_status'] == 'Senior Citizen Divorsed / Widow Customer Small Family' or value['FamilyGrp_status'] == 'Single Senior Citizen Customer Small Family' or value['FamilyGrp_status'] == 'Senior Citizen Small Family' or value['FamilyGrp_status'] == 'Single Old Small Family') and (value['TodCount'] > 0 or value['YoungCount'] >0) :
#        return "Old Small Family with Tod / Young"
#    elif  (value['FamilyGrp_status'] == 'Old Small Family' or value['FamilyGrp_status'] == 'Old Divorsed / Widow Customer Small Family' or value['FamilyGrp_status'] == 'Senior Citizen Divorsed / Widow Customer Small Family' or value['FamilyGrp_status'] == 'Single Senior Citizen Customer Small Family' or value['FamilyGrp_status'] == 'Senior Citizen Small Family' or value['FamilyGrp_status'] == 'Single Old Small Family') and (value['TeenCount'] > 0 or value['GradCount'] >0) :
#        return "Old Small Family with Teen / Grad kids"
#    elif  (value['FamilyGrp_status'] == 'Single Old large Family' or value['FamilyGrp_status'] == 'Old large Family' or value['FamilyGrp_status'] == 'Senior Citizen large Family' or value['FamilyGrp_status'] == 'Single Senior Citizen Customer large Family' or value['FamilyGrp_status'] == 'Senior Citizen Divorsed / Widow Customer large Family' or value['FamilyGrp_status'] == 'Old Divorsed / Widow Customer large Family') and (value['TodCount'] > 0 or value['YoungCount'] > 0):
#        return "Old large Family with Tod / Young"
#    elif (value['FamilyGrp_status'] == 'Single Old large Family' or value['FamilyGrp_status'] == 'Old large Family' or value['FamilyGrp_status'] == 'Senior Citizen large Family' or value['FamilyGrp_status'] == 'Single Senior Citizen Customer large Family' or value['FamilyGrp_status'] == 'Senior Citizen Divorsed / Widow Customer large Family' or value['FamilyGrp_status'] == 'Old Divorsed / Widow Customer large Family') and (value['TeenCount'] > 0 or value['GradCount'] > 0):
#        return "Old large Family with Teen / Grad kids"
#    else:
#        return "Small Family"
#
#fin_df2['familyKidgrp1'] = fin_df2.apply(agegrp_df, axis=1)
#fin_df2.familyKidgrp1.unique()
#fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)

#Writing Results
path_out = "E:/NTUC/raw_data/Final/hh_result_final/"
fin_df2.to_csv(path_out+"hh_lifeStage_result_noScore.csv", header = True, index = False)
fin_df2.columns
fin_df3 = fin_df2[['hid','maritalstatus','premiumbucket','PH_AgeGroup','AgeGroup', 'age', 'FamilyGrp_status']]
fin_df3.to_csv(path_out+"hh_lifeStage_result_for_score.csv", header = True, index = False)

# Generating Final Score

life = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/lifeStage_score_broadCategory_Final.csv"
#reading hh_lifestageScore data
lifeStage_score = pd.read_csv(life, low_memory = True)
lifeStage_score.columns

# Merging lifeStageScore with result1 data
life_result = fin_df3.merge(lifeStage_score, on='FamilyGrp_status', how ='left'  )
life_result = life_result.fillna('NA')
life_result.columns
len(life_result)
# Merging with overall big file i.e.fin_df2
life_result1 = fin_df2.merge(lifeStage_score, on='FamilyGrp_status', how ='left'  )
life_result1 = life_result1.fillna('NA')
life_result1.columns
len(life_result1)


life_result2 = life_result1[['hid', 'ageph',   'customertype',  'MembersCount',
        'TodCount', 'YoungCount', 'TeenCount', 'GradCount',
       'totalkids',  'maritalstatus', 'total_premium', 'premiumbucket', 'AgeGroup','PH_AgeGroup','FamilyGrp_status',
        'FinalWeightScore']]

life_result2['FinalWeightScore'] = life_result2['FinalWeightScore'].replace('NA',0)
##Groupby on hid
life_result2 = life_result2.groupby('hid', group_keys=False).apply(lambda x: x.loc[x.FinalWeightScore.idxmax()])
len(life_result2)
life_result2 = life_result2.drop_duplicates(subset=None, keep='first', inplace=False)
life_result2.to_csv(path_out+"hh_lifeStage_result_score_broad.csv", header = True, index = False)





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
# Creating data for exploratory and weight framework
fin_df3 = fin_df2.drop(['customerseqid'], axis = 1)
fin_df3.to_csv(path2+"lifestageData.csv", index = False, header = True)
#len(fin_df3)

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
        return "value NA or New born baby"
    elif int(value['age'] < 6 and int (value['age']) > 0):
        return "toddler"
    elif int(value['age'] < 13 and int (value['age']) >5):
        return "Young child"
    elif int(value['age'] < 20 and int (value['age']) >12):
        return " Teen child"
    elif int(value['age'] < 31 and int (value['age']) >19):
        return "Young Customer "
    elif int(value['age'] < 46 and int (value['age']) >30):
        return "Matured Customer"
    elif int(value['age'] > 45 and int (value['age']) < 65):
        return "Old Customer"
    elif int(value['age'] > 64):
        return "Senior Citizen Customer"
    else:
        return "Others"
### generating age group on the basis of current age
fin_df2['age'] =fin_df2['age'].replace('NA', 0)
fin_df2['AgeGroup'] = fin_df2.apply(agegrp_df, axis=1)
fin_df2.AgeGroup.unique()
fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)

### ageph group buckets
def agegrp_df(value):
    if int(value['ageph'] == 0 ):
        return "value NA or New born baby"
    elif int(value['ageph'] < 6 and int (value['ageph']) > 0):
        return "toddler"
    elif int(value['ageph'] < 13 and int (value['ageph']) >5):
        return "Young child"
    elif int(value['ageph'] < 20 and int (value['ageph']) >12):
        return " Teen child"
    elif int(value['ageph'] < 31 and int (value['ageph']) >19):
        return "Young Customer "
    elif int(value['ageph'] < 46 and int (value['ageph']) >30):
        return "Matured Customer"
    elif int(value['ageph'] > 45 and int (value['ageph']) < 65):
        return "Old Customer"
    elif int(value['ageph'] > 64):
        return "Senior Citizen Customer"
    else:
        return "Others"

### generating age group on the basis of ageph
fin_df2['ageph'] = fin_df2['ageph'].fillna(0)
fin_df2['ageph'] = fin_df2['ageph'].astype(np.int64)
fin_df2['PH_AgeGroup'] = fin_df2.apply(agegrp_df, axis=1)
fin_df2.PH_AgeGroup.unique()
fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)
#########################################################

########PH_Age and Marital Status

def agegrp_df(value):
    if (value['PH_AgeGroup'] == 'value NA or New born baby' ) and (value['maritalstatus'] == 'Single' or value['maritalstatus'] == 'Married' or value['maritalstatus'] == 'Divorce' or value['maritalstatus'] == 'Widow'):
        return " New born baby"
    elif(value['PH_AgeGroup'] == 'value NA or New born baby' ) and (value['maritalstatus'] == 'Other' or value['maritalstatus'] == 'NA'):
        return "Info NA"
    elif(value['PH_AgeGroup'] == 'Young child' or value['PH_AgeGroup'] == 'Teen child') and (value['maritalstatus'] == 'Other' or value['maritalstatus'] == 'NA'):
        return "Info NA"
    elif(value['PH_AgeGroup'] == 'Young child' or value['PH_AgeGroup'] == 'Teen child') and (value['maritalstatus'] == 'Single' or value['maritalstatus'] == 'Married' or value['maritalstatus'] == 'Divorce' or value['maritalstatus'] == 'Widow'):
        return "Young Child pol "
    elif(value['PH_AgeGroup'] == 'Young Customer ' ) and (value['maritalstatus'] == 'Other' or value['maritalstatus'] == 'NA'):
        return "Info NA"
    elif(value['PH_AgeGroup'] == 'Young Customer ' ) and (value['maritalstatus'] == 'Married'):
        return "Young Married Customer"
    elif(value['PH_AgeGroup'] == 'Young Customer ' ) and (value['maritalstatus'] == 'Single'):
        return "Young Single Customer"
    elif(value['PH_AgeGroup'] == 'Young Customer ' ) and (value['maritalstatus'] == 'Divorce' or value['maritalstatus'] == 'Widow'):
        return "Young Divorsed / Widow Customer"
    elif(value['PH_AgeGroup'] == 'Matured Customer' ) and (value['maritalstatus'] == 'Married'):
        return " Married Matured Customer"
    elif(value['PH_AgeGroup'] == 'Matured Customer' ) and (value['maritalstatus'] == 'Single'):
        return "Single Matured Customer"
    elif(value['PH_AgeGroup'] == 'Matured Customer' ) and (value['maritalstatus'] == 'Divorce' or value['maritalstatus'] == 'Widow'):
        return "Young Divorsed / Widow Customer"
    elif(value['PH_AgeGroup'] == 'Matured Customer' ) and (value['maritalstatus'] == 'Other' or value['maritalstatus'] == 'NA'):
        return "Info NA"
    elif(value['PH_AgeGroup'] == 'Old Customer' ) and (value['maritalstatus'] == 'Married'):
        return " Married Old Customer"
    elif(value['PH_AgeGroup'] == 'Old Customer' ) and (value['maritalstatus'] == 'Single'):
        return "Single Old Customer"
    elif(value['PH_AgeGroup'] == 'Old Customer' ) and (value['maritalstatus'] == 'Divorce' or value['maritalstatus'] == 'Widow'):
        return "Old Divorsed / Widow Customer"
    elif(value['PH_AgeGroup'] == 'Old Customer' ) and (value['maritalstatus'] == 'Other' or value['maritalstatus'] == 'NA'):
        return "Info NA"
    elif(value['PH_AgeGroup'] == 'Senior Citizen Customer' ) and (value['maritalstatus'] == 'Married'):
        return " Married Senior Citizen Customer"
    elif(value['PH_AgeGroup'] == 'Senior Citizen Customer' ) and (value['maritalstatus'] == 'Single'):
        return "Single Senior Citizen Customer"
    elif(value['PH_AgeGroup'] == 'Senior Citizen Customer' ) and (value['maritalstatus'] == 'Divorce' or value['maritalstatus'] == 'Widow'):
        return "Senior Citizen Divorsed / Widow Customer"
    elif(value['PH_AgeGroup'] == 'Senior Citizen Customer' ) and (value['maritalstatus'] == 'Other' or value['maritalstatus'] == 'NA'):
        return "Info NA"
    else:
        return "Others"

### generating age group on the basis of ageph
fin_df2['Marital_status'] = fin_df2.apply(agegrp_df, axis=1)
fin_df2.Marital_status.unique()
fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)

#####################################################3
###MArital and kids

def agegrp_df(value):
    if (value['Marital_status'] == 'Single Old Customer' ) and (value['totalkids'] == 0 ):
        return "Old Single no kid"
    elif(value['Marital_status'] == 'Single Old Customer' ) and (value['totalkids'] < 3 ):
        return "Single Old Small Family"
    elif(value['Marital_status'] == 'Single Old Customer' ) and (value['totalkids'] > 2 ):
        return "Single Old large Family"
    elif(value['Marital_status'] == 'Single Matured Customer' ) and (value['totalkids'] == 0 ):
        return "Matured Single no kid"
    elif(value['Marital_status'] == 'Single Matured Customer' ) and (value['totalkids'] < 3 ):
        return "Matured Single Small Family"
    elif(value['Marital_status'] == 'Single Matured Customer' ) and (value['totalkids'] > 2 ):
        return "Matured Single large Family"
    elif(value['Marital_status'] == ' Married Matured Customer' ) and (value['totalkids'] == 0 ):
        return "Matured Couple no kid"
    elif(value['Marital_status'] == ' Married Matured Customer' ) and (value['totalkids'] < 3 ):
        return "Matured Small Family"
    elif(value['Marital_status'] == ' Married Matured Customer' ) and (value['totalkids'] > 2 ):
        return "Matured large Family"
    elif(value['Marital_status'] == 'Old Divorsed / Widow Customer' ) and (value['totalkids'] == 0 ):
        return "Old Divorsed / Widow Customer no kid"
    elif(value['Marital_status'] == 'Old Divorsed / Widow Customer' ) and (value['totalkids'] < 3 ):
        return "Old Divorsed / Widow Customer Small Family"
    elif(value['Marital_status'] == 'Old Divorsed / Widow Customer' ) and (value['totalkids'] > 3 ):
        return "Old Divorsed / Widow Customer large Family"
    elif(value['Marital_status'] == ' Married Old Customer' ) and (value['totalkids'] == 0 ):
        return "Old Couple no kid"
    elif(value['Marital_status'] == ' Married Old Customer' ) and (value['totalkids'] < 3 ):
        return "Old Small Family"
    elif(value['Marital_status'] == ' Married Old Customer' ) and (value['totalkids'] > 2 ):
        return "Old large Family"
    elif(value['Marital_status'] == ' Married Senior Citizen Customer' ) and (value['totalkids'] == 0 ):
        return "Senior Citizen Couple no kid"
    elif(value['Marital_status'] == ' Married Senior Citizen Customer' ) and (value['totalkids'] < 3 ):
        return "Senior Citizen Small Family"
    elif(value['Marital_status'] == ' Married Senior Citizen Customer' ) and (value['totalkids'] > 2 ):
        return "Senior Citizen large Family"
    elif(value['Marital_status'] == 'Senior Citizen Divorsed / Widow Customer' ) and (value['totalkids'] == 0 ):
        return "Senior Citizen Divorsed / Widow Customer no kid"
    elif(value['Marital_status'] == 'Senior Citizen Divorsed / Widow Customer' ) and (value['totalkids'] < 3 ):
        return "Senior Citizen Divorsed / Widow Customer Small Family"
    elif(value['Marital_status'] == 'Senior Citizen Divorsed / Widow Customer' ) and (value['totalkids'] > 3 ):
        return "Senior Citizen Divorsed / Widow Customer large Family"
    elif(value['Marital_status'] == 'Single Senior Citizen Customer' ) and (value['totalkids'] == 0 ):
        return "Single Senior Citizen Customer no kid"
    elif(value['Marital_status'] == 'Single Senior Citizen Customer' ) and (value['totalkids'] < 3 ):
        return "Single Senior Citizen Customer Small Family"
    elif(value['Marital_status'] == 'Single Senior Citizen Customer' ) and (value['totalkids'] > 2 ):
        return "Single Senior Citizen Customer large Family"
    elif(value['Marital_status'] == 'Young Single Customer' ) and (value['totalkids'] == 0 ):
        return "Young Single Customer no kids"
    elif(value['Marital_status'] == 'Young Single Customer' ) and (value['totalkids'] < 3 ):
        return "Young Single Small Family"
    elif(value['Marital_status'] == 'Young Single Customer' ) and (value['totalkids'] > 3 ):
        return "Young Single large Family"
    elif(value['Marital_status'] == 'Young Married Customer' ) and (value['totalkids'] == 0 ):
        return "Young Married Customer no kids"
    elif(value['Marital_status'] == 'Young Married Customer' ) and (value['totalkids'] < 3 ):
        return "Young Married Small Family"
    elif(value['Marital_status'] == 'Young Married Customer' ) and (value['totalkids'] > 3 ):
        return "Young Married large Family"
    elif(value['Marital_status'] == 'Young Divorsed / Widow Customer' ) and (value['totalkids'] == 0 ):
        return "Young Divorsed / Widow Customer"
    elif(value['Marital_status'] == 'Young Divorsed / Widow Customer' ) and (value['totalkids'] < 3 ):
        return "Young Divorsed / Widow Customer Small Family"
    elif(value['Marital_status'] == 'Young Divorsed / Widow Customer' ) and (value['totalkids'] > 3 ):
        return "Young Divorsed / Widow Customer large Family"

    else:
        return "Info NA"

### generating age group on the basis of ageph
fin_df2['FamilyGrp_status'] = fin_df2.apply(agegrp_df, axis=1)
fin_df2.FamilyGrp_status.unique()
fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)


################################################################
def agegrp_df(value):
    if (value['FamilyGrp_status'] == 'Young Single' or value['FamilyGrp_status'] == 'Young Single large Family' or value['FamilyGrp_status'] == 'Young Single Customer no kids' or value['FamilyGrp_status'] == 'Young Single Small Family' or value['FamilyGrp_status'] == 'Young Divorsed / Widow Customer') and (value['TodCount'] == 0 or value['YoungCount'] == 0):
        return "Young Single"
    elif (value['FamilyGrp_status'] == 'Young Single' or value['FamilyGrp_status'] == 'Young Single large Family' or value['FamilyGrp_status'] == 'Young Single Customer no kids' or value['FamilyGrp_status'] == 'Young Single Small Family' or value['FamilyGrp_status'] == 'Young Divorsed / Widow Customer') and (value['TodCount'] == 0 or value['YoungCount'] == 0):
        return "Young Single Parent with Tod / Young"
    elif (value['FamilyGrp_status'] == 'Young Single' or value['FamilyGrp_status'] == 'Young Single large Family' or value['FamilyGrp_status'] == 'Young Single Customer no kids' or value['FamilyGrp_status'] == 'Young Single Small Family' or value['FamilyGrp_status'] == 'Young Divorsed / Widow Customer') and (value['GradCount'] == 0 or value['TeenCount'] == 0):
        return "Young Single Parent with Teen / Grad kids"
    elif value['FamilyGrp_status'] == 'Young Married Customer no kids' and (value['TodCount'] == 0 or value['YoungCount'] == 0):
        return "Young Couple"
    elif  (value['FamilyGrp_status'] == 'Young Small Family' or value['FamilyGrp_status'] == 'Young Married Small Family' or value['FamilyGrp_status'] == 'Young Divorsed / Widow Customer Small Family') and (value['TodCount'] > 0 or value['YoungCount'] >0) :
        return "Young Small Family with Tod / Young"
    elif  (value['FamilyGrp_status'] == 'Young Small Family' or value['FamilyGrp_status'] == 'Young Married Small Family' or value['FamilyGrp_status'] == 'Young Divorsed / Widow Customer Small Family') and (value['GradCount'] > 0 or value['TeenCount'] >0) :
        return "Young Small Family with Teen / Grad kids"
    elif  (value['FamilyGrp_status'] == 'Young Married large Family' or value['FamilyGrp_status'] == 'Young large Family' or value['FamilyGrp_status'] == 'Young Divorsed / Widow Customer large Family') and (value['TodCount'] > 0 or value['YoungCount'] > 0):
        return "Young large Family with Tod / Young"
    elif (value['FamilyGrp_status'] == 'Young Married large Family' or value['FamilyGrp_status'] == 'Young large Family' or value['FamilyGrp_status'] == 'Young Divorsed / Widow Customer large Family') and (value['TeenCount'] > 0 or value['GradCount'] > 0):
        return "Young large Family with Teen / Grad kids"
    elif  (value['FamilyGrp_status'] == 'Matured Single no kid' or value['FamilyGrp_status'] == 'Matured Single') and (value['TodCount'] == 0 or value['YoungCount'] == 0):
        return "Matured Single"
    elif  value['FamilyGrp_status'] == 'Matured Single Parent' and (value['TodCount'] > 0 or value['YoungCount'] > 0):
        return "Matured Single Parent with Tod / Young"
    elif  value['FamilyGrp_status'] == 'Matured Single Parent' and (value['TeenCount'] > 0 or value['GradCount'] > 0):
        return "Matured Single Parent with Teen / Grad kids"
    elif (value['FamilyGrp_status'] == 'Matured Couple no kid') and (value['TodCount'] == 0 or value['YoungCount'] == 0):
        return "Matured Couple"
    elif  (value['FamilyGrp_status'] == 'Matured Small Family' or value['FamilyGrp_status'] == 'Matured Single Small Family') and (value['TodCount'] > 0 or value['YoungCount'] >0) :
        return "Matured Small Family with Tod / Young"
    elif  (value['FamilyGrp_status'] == 'Matured Small Family' or value['FamilyGrp_status'] == 'Matured Single Small Family') and (value['TeenCount'] > 0 or value['GradCount'] >0) :
        return "Matured Small Family with Teen / Grad kids"
    elif  (value['FamilyGrp_status'] == 'Matured large Family' or value['FamilyGrp_status'] == 'Matured Single large Family') and (value['TodCount'] > 0 or value['YoungCount'] > 0):
        return "Matured large Family with Tod / Young"
    elif (value['FamilyGrp_status'] == 'Matured large Family' or value['FamilyGrp_status'] == 'Matured Single large Family') and (value['TeenCount'] > 0 or value['GradCount'] > 0):
        return "Matured large Family with Teen / Grad kids"
    elif  (value['FamilyGrp_status'] == 'Old Single no kid' or value['FamilyGrp_status'] == 'Single Senior Citizen Customer no kid' or value['FamilyGrp_status'] == 'Senior Citizen Divorsed / Widow Customer no kid' or value['FamilyGrp_status'] == 'Old Divorsed / Widow Customer no kid') and (value['TodCount'] == 0 or value['YoungCount'] == 0):
        return "Old Single"
    elif  value['FamilyGrp_status'] == 'Old Single Parent' and (value['TodCount'] > 0 or value['YoungCount'] > 0):
        return "Old Single Parent with Tod / Young"
    elif  value['FamilyGrp_status'] == 'Old Single Parent' and (value['TeenCount'] > 0 or value['GradCount'] > 0):
        return "Old Single Parent with Teen / Grad kids"
    elif (value['FamilyGrp_status'] == 'Old Couple no kid' or value['FamilyGrp_status'] == 'Senior Citizen Couple no kid') and (value['TodCount'] == 0 or value['YoungCount'] == 0):
        return "Old Couple"
    elif  (value['FamilyGrp_status'] == 'Old Small Family' or value['FamilyGrp_status'] == 'Old Divorsed / Widow Customer Small Family' or value['FamilyGrp_status'] == 'Senior Citizen Divorsed / Widow Customer Small Family' or value['FamilyGrp_status'] == 'Single Senior Citizen Customer Small Family' or value['FamilyGrp_status'] == 'Senior Citizen Small Family' or value['FamilyGrp_status'] == 'Single Old Small Family') and (value['TodCount'] > 0 or value['YoungCount'] >0) :
        return "Old Small Family with Tod / Young"
    elif  (value['FamilyGrp_status'] == 'Old Small Family' or value['FamilyGrp_status'] == 'Old Divorsed / Widow Customer Small Family' or value['FamilyGrp_status'] == 'Senior Citizen Divorsed / Widow Customer Small Family' or value['FamilyGrp_status'] == 'Single Senior Citizen Customer Small Family' or value['FamilyGrp_status'] == 'Senior Citizen Small Family' or value['FamilyGrp_status'] == 'Single Old Small Family') and (value['TeenCount'] > 0 or value['GradCount'] >0) :
        return "Old Small Family with Teen / Grad kids"
    elif  (value['FamilyGrp_status'] == 'Single Old large Family' or value['FamilyGrp_status'] == 'Old large Family' or value['FamilyGrp_status'] == 'Senior Citizen large Family' or value['FamilyGrp_status'] == 'Single Senior Citizen Customer large Family' or value['FamilyGrp_status'] == 'Senior Citizen Divorsed / Widow Customer large Family' or value['FamilyGrp_status'] == 'Old Divorsed / Widow Customer large Family') and (value['TodCount'] > 0 or value['YoungCount'] > 0):
        return "Old large Family with Tod / Young"
    elif (value['FamilyGrp_status'] == 'Single Old large Family' or value['FamilyGrp_status'] == 'Old large Family' or value['FamilyGrp_status'] == 'Senior Citizen large Family' or value['FamilyGrp_status'] == 'Single Senior Citizen Customer large Family' or value['FamilyGrp_status'] == 'Senior Citizen Divorsed / Widow Customer large Family' or value['FamilyGrp_status'] == 'Old Divorsed / Widow Customer large Family') and (value['TeenCount'] > 0 or value['GradCount'] > 0):
        return "Old large Family with Teen / Grad kids"
    else:
        return "Info NA"

fin_df2['familyKidgrp1'] = fin_df2.apply(agegrp_df, axis=1)
fin_df2.familyKidgrp1.unique()
fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)

#Writing Results
path_out = "E:/NTUC/raw_data/Final/hh_result_final/"
fin_df2.to_csv(path_out+"hh_lifeStage_result_noScore.csv", header = True, index = False)
fin_df2.columns
fin_df3 = fin_df2[['hid','Marital_status','premiumbucket','PH_AgeGroup','AgeGroup', 'age', 'FamilyGrp_status','familyKidgrp1']]
fin_df3.to_csv(path_out+"hh_lifeStage_result_for_score.csv", header = True, index = False)

# Generating Final Score

life = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/lifeStage_score.csv"
#reading hh_trav_country_score data
lifeStage_score = pd.read_csv(life, low_memory = True)
lifeStage_score.columns

# Merging hh_vhbrand_score with result1 data
life_result = fin_df3.merge(lifeStage_score, on='familyKidgrp1', how ='left'  )
life_result = life_result.fillna('NA')
life_result.columns
len(life_result)
# Merging with overall big file i.e.fin_df2
life_result1 = fin_df2.merge(lifeStage_score, on='familyKidgrp1', how ='left'  )
life_result1 = life_result1.fillna('NA')
life_result1.columns
len(life_result1)


life_result2 = life_result1[['hid', 'ageph',   'customertype',  'MembersCount',
        'TodCount', 'YoungCount', 'TeenCount', 'GradCount',
       'totalkids',  'maritalstatus', 'total_premium', 'premiumbucket', 'AgeGroup','PH_AgeGroup','FamilyGrp_status',
        'familyKidgrp1', 'FinalWeightScore']]

life_result2['FinalWeightScore'] = life_result2['FinalWeightScore'].replace('NA',0)
##Groupby on hid
life_result2 = life_result2.groupby('hid', group_keys=False).apply(lambda x: x.loc[x.FinalWeightScore.idxmax()])
len(life_result2)
life_result2 = life_result2.drop_duplicates(subset=None, keep='first', inplace=False)
life_result2.to_csv(path_out+"hh_lifeStage_result_score.csv", header = True, index = False)





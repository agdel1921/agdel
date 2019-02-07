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
df_tmp.customertype.unique()
df = df_tmp

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
fin_df2.columns
fin_df2.ageph.unique()

##################### //Not used currently ##############

##Grouing
#grp1 = fin_df2.groupby(['hid','ageph','maritalstatus','TodCount',
#       'YoungCount', 'TeenCount', 'GradCount', 'totalkids', 'premiumbucket','MembersCount', 'MembersActive' ]).groups
#
#grp2 = fin_df2.groupby(['hid','ageph','maritalstatus','TodCount',
#       'YoungCount', 'TeenCount', 'GradCount', 'totalkids', 'premiumbucket','MembersCount', 'MembersActive', 'educationlevel','vehbrand','vehtypename','addr_type_desc' ]).groups
#
#grp3 = fin_df2.groupby(['hid','ageph','genderph','customertype','maritalstatus','TodCount','YoungCount', 'TeenCount', 'GradCount', 'totalkids', 'premiumbucket','MembersCount', 'MembersActive', 'educationlevel','productcategory',  'vehbrand', 'vehtypename', 'postalcode', 'addr_type_desc' ]).groups
#
#grp4 = fin_df2.groupby(['hid','ageph','genderph','customertype','maritalstatus','TodCount','YoungCount', 'TeenCount', 'GradCount', 'totalkids', 'premiumbucket','MembersCount', 'MembersActive', 'educationlevel','productcategory',  'vehbrand', 'vehtypename', 'postalcode', 'addr_type_desc','Total_Policies']).groups
#
#grp11 = fin_df2.groupby(['ageph','maritalstatus','TodCount',
#       'YoungCount', 'TeenCount', 'GradCount', 'totalkids', 'premiumbucket','MembersCount', 'MembersActive']).groups
#
#grp22 = fin_df2.groupby(['ageph','maritalstatus','TodCount',
#       'YoungCount', 'TeenCount', 'GradCount', 'totalkids', 'premiumbucket','MembersCount', 'MembersActive', 'educationlevel','vehbrand','vehtypename','addr_type_desc' ]).groups
#
#
#grp33 = fin_df2.groupby(['ageph','genderph','customertype','maritalstatus','TodCount','YoungCount', 'TeenCount', 'GradCount', 'totalkids', 'premiumbucket','MembersCount', 'MembersActive', 'educationlevel','productcategory',  'vehbrand', 'vehtypename', 'postalcode', 'addr_type_desc' ]).groups
#
#grp44 = fin_df2.groupby(['ageph','genderph','customertype','maritalstatus','TodCount','YoungCount', 'TeenCount', 'GradCount', 'totalkids', 'premiumbucket','MembersCount', 'MembersActive', 'educationlevel','productcategory',  'vehbrand', 'vehtypename', 'postalcode', 'addr_type_desc','Total_Policies']).groups
#
## converting dictionaries to dataframe
#
#grp = pd.DataFrame([grp1])
#grp2 = pd.DataFrame([grp2])
#grp11 = pd.DataFrame([grp11])
#grp22 = pd.DataFrame([grp22])
#grp3 = pd.DataFrame([grp3])
#grp33 = pd.DataFrame([grp33])
#grp4 =pd.DataFrame([grp4])
#grp44 =pd.DataFrame([grp44])

######################################################

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

fin_df2['AgeGroup'] = fin_df2.apply(agegrp_df, axis=1)
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



####################CustomerType
fin_df2['customertype'] = fin_df2['customertype'].fillna('NA')
fin_df2.customertype.unique()

###age and customertype group buckets
def agegrp_df(value):
    if int(value['age'] == 0 ) and (value['customertype'] == 'DS' or value['customertype'] == 'DP'):
        return "value NA or New born baby Dependent customer"
    elif int(value['age'] == 0 ) and (value['customertype'] == 'PH'):
        return "value NA or New born baby PH customer"
    elif int(value['age'] == 0 ) and (value['customertype'] == 'NA'):
        return "Info NA"
    elif int(value['age'] < 6 and int (value['age']) > 0) and (value['customertype'] == 'DS' or value['customertype'] == 'DP'):
        return "toddler Dependent customer"
    elif int(value['age'] < 6 and int (value['age']) > 0) and (value['customertype'] == 'PH'):
        return "toddler PH customer"
    elif int(value['age'] < 6 and int (value['age']) > 0) and (value['customertype'] == 'NA'):
        return "Info NA"
    elif int(value['age'] < 13 and int (value['age']) >5) and (value['customertype'] == 'DS' or value['customertype'] == 'DP'):
        return "Young child Dependent customer"
    elif int(value['age'] < 13 and int (value['age']) >5) and (value['customertype'] == 'PH'):
        return "Young child PH customer"
    elif int(value['age'] < 13 and int (value['age']) >5) and (value['customertype'] == 'NA'):
        return "Info NA"
    elif int(value['age'] < 20 and int (value['age']) >12)and (value['customertype'] == 'DS' or value['customertype'] == 'DP'):
        return "Teen child Dependent customer"
    elif int(value['age'] < 20 and int (value['age']) >12)and (value['customertype'] == 'PH' ):
        return "Teen child PH customer"
    elif int(value['age'] < 20 and int (value['age']) >12)and (value['customertype'] == 'NA' ):
        return "Info NA"
    elif int(value['age'] < 31 and int (value['age']) >19)and (value['customertype'] == 'DS' or value['customertype'] == 'DP'):
        return "Young Dependent Customer"
    elif int(value['age'] < 31 and int (value['age']) >19)and (value['customertype'] == 'PH'):
        return "Young PH Customer"
    elif int(value['age'] < 31 and int (value['age']) >19)and (value['customertype'] == 'NA'):
        return "Info NA"
    elif int(value['age'] < 46 and int (value['age']) >30)and (value['customertype'] == 'DS'or value['customertype'] == 'DP'):
        return "Matured Dependent Customer"
    elif int(value['age'] < 46 and int (value['age']) >30)and ( value['customertype'] == 'PH'):
        return "Matured PH Customer"
    elif int(value['age'] < 46 and int (value['age']) >30)and (value['customertype'] == 'NA'):
        return "Info NA"
    elif int(value['age'] > 45 and int (value['age']) < 65)and (value['customertype'] == 'DS'or value['customertype'] == 'DP'):
        return "Old Dependent Customer"
    elif int(value['age'] > 45 and int (value['age']) < 65)and ( value['customertype'] == 'PH'):
        return "Old PH Customer"
    elif int(value['age'] > 45 and int (value['age']) < 65)and (value['customertype'] == 'NA'):
        return "Info NA"
    elif int(value['age'] > 64)and (value['customertype'] == 'DS' or value['customertype'] == 'DP'):
        return "Senior Citizen Dependent Customer"
    elif int(value['age'] > 64)and (value['customertype'] == 'PH'):
        return "Senior Citizen PH Customer"
    elif int(value['age'] > 64)and (value['customertype'] == 'NA'):
        return "Info NA"
    else:
        return "Others"


fin_df2['CustomerTypeAge'] = fin_df2.apply(agegrp_df, axis=1)
fin_df2.CustomerTypeAge.unique()
fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)

### ageph and customertype group buckets
def agegrp_df(value):
    if int(value['ageph'] == 0 ) and (value['customertype'] == 'DS' or value['customertype'] == 'DP'):
        return "value NA or New born baby Dependent customer"
    elif int(value['ageph'] == 0 ) and (value['customertype'] == 'PH'):
        return "value NA or New born baby PH customer"
    elif int(value['ageph'] == 0 ) and (value['customertype'] == 'NA'):
        return "Info NA"
    elif int(value['ageph'] < 6 and int (value['ageph']) > 0) and (value['customertype'] == 'DS' or value['customertype'] == 'DP'):
        return "toddler Dependent customer"
    elif int(value['ageph'] < 6 and int (value['ageph']) > 0) and (value['customertype'] == 'PH'):
        return "toddler PH customer"
    elif int(value['ageph'] < 6 and int (value['ageph']) > 0) and (value['customertype'] == 'NA'):
        return "Info NA"
    elif int(value['ageph'] < 13 and int (value['ageph']) >5) and (value['customertype'] == 'DS' or value['customertype'] == 'DP'):
        return "Young child Dependent customer"
    elif int(value['ageph'] < 13 and int (value['ageph']) >5) and (value['customertype'] == 'PH'):
        return "Young child PH customer"
    elif int(value['ageph'] < 13 and int (value['ageph']) >5) and (value['customertype'] == 'NA'):
        return "Info NA"
    elif int(value['ageph'] < 20 and int (value['ageph']) >12)and (value['customertype'] == 'DS' or value['customertype'] == 'DP'):
        return "Teen child Dependent customer"
    elif int(value['ageph'] < 20 and int (value['ageph']) >12)and (value['customertype'] == 'PH' ):
        return "Teen child PH customer"
    elif int(value['ageph'] < 20 and int (value['ageph']) >12)and (value['customertype'] == 'NA' ):
        return "Info NA"
    elif int(value['ageph'] < 31 and int (value['ageph']) >19)and (value['customertype'] == 'DS' or value['customertype'] == 'DP'):
        return "Young Dependent Customer"
    elif int(value['ageph'] < 31 and int (value['ageph']) >19)and (value['customertype'] == 'PH'):
        return "Young PH Customer"
    elif int(value['ageph'] < 31 and int (value['ageph']) >19)and (value['customertype'] == 'NA'):
        return "Info NA"
    elif int(value['ageph'] < 46 and int (value['ageph']) >30)and (value['customertype'] == 'DS'or value['customertype'] == 'DP'):
        return "Matured Dependent Customer"
    elif int(value['ageph'] < 46 and int (value['ageph']) >30)and ( value['customertype'] == 'PH'):
        return "Matured PH Customer"
    elif int(value['ageph'] < 46 and int (value['ageph']) >30)and (value['customertype'] == 'NA'):
        return "Info NA"
    elif int(value['ageph'] > 45 and int (value['ageph']) < 65)and (value['customertype'] == 'DS'or value['customertype'] == 'DP'):
        return "Old Dependent Customer"
    elif int(value['ageph'] > 45 and int (value['ageph']) < 65)and ( value['customertype'] == 'PH'):
        return "Old PH Customer"
    elif int(value['ageph'] > 45 and int (value['ageph']) < 65)and (value['customertype'] == 'NA'):
        return "Info NA"
    elif int(value['ageph'] > 64)and (value['customertype'] == 'DS' or value['customertype'] == 'DP'):
        return "Senior Citizen Dependent Customer"
    elif int(value['ageph'] > 64)and (value['customertype'] == 'PH'):
        return "Senior Citizen PH Customer"
    elif int(value['ageph'] > 64)and (value['customertype'] == 'NA'):
        return "Info NA"
    else:
        return "Others"

fin_df2['CustomerTypeAgePH'] = fin_df2.apply(agegrp_df, axis=1)
fin_df2.CustomerTypeAgePH.unique()
fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)

####ageph and customertype group buckets
#def agegrp_df(value):
#    if int(value['ageph'] == 0 ) and (value['customertype'] == 'DS' or value['customertype'] == 'DP'or value['customertype'] == 'PH'):
#        return "value NA or New born baby customer"
#    elif int(value['ageph'] == 0 ) and (value['customertype'] == 'NA'):
#        return "Info NA"
#    elif int(value['ageph'] < 6 and int (value['ageph']) > 0) and (value['customertype'] == 'DS' or value['customertype'] == 'DP'or value['customertype'] == 'PH'):
#        return "toddler customer"
#    elif int(value['ageph'] < 6 and int (value['ageph']) > 0) and (value['customertype'] == 'NA'):
#        return "Info NA"
#    elif int(value['ageph'] < 13 and int (value['ageph']) >5) and (value['customertype'] == 'DS' or value['customertype'] == 'DP'or value['customertype'] == 'PH'):
#        return "Young child customer"
#    elif int(value['ageph'] < 13 and int (value['ageph']) >5) and (value['customertype'] == 'NA'):
#        return "Info NA"
#    elif int(value['ageph'] < 20 and int (value['ageph']) >12)and (value['customertype'] == 'DS' or value['customertype'] == 'DP'or value['customertype'] == 'PH'):
#        return "Teen child customer"
#    elif int(value['ageph'] < 20 and int (value['ageph']) >12)and (value['customertype'] == 'NA' ):
#        return "Info NA"
#    elif int(value['ageph'] < 31 and int (value['ageph']) >19)and (value['customertype'] == 'DS' or value['customertype'] == 'DP'or value['customertype'] == 'PH'):
#        return "Young Customer"
#    elif int(value['ageph'] < 31 and int (value['ageph']) >19)and (value['customertype'] == 'NA'):
#        return "Info NA"
#    elif int(value['ageph'] < 46 and int (value['ageph']) >30)and (value['customertype'] == 'DS' or value['customertype'] == 'DP'or value['customertype'] == 'PH'):
#        return "Matured Customer"
#    elif int(value['ageph'] < 46 and int (value['ageph']) >30)and (value['customertype'] == 'NA'):
#        return "Info NA"
#    elif int(value['ageph'] > 45 and int (value['ageph']) < 65)and (value['customertype'] == 'DS' or value['customertype'] == 'DP'or value['customertype'] == 'PH'):
#        return "Old Customer"
#    elif int(value['ageph'] > 45 and int (value['ageph']) < 65)and (value['customertype'] == 'NA'):
#        return "Info NA"
#    elif int(value['ageph'] > 64)and (value['customertype'] == 'DS' or value['customertype'] == 'DP'or value['customertype'] == 'PH'):
#        return "Senior Citizen Customer"
#    elif int(value['ageph'] > 64)and (value['customertype'] == 'NA'):
#        return "Info NA"
#    else:
#        return "Others"
#
#
#fin_df2['PH_CustomerType'] = fin_df2.apply(agegrp_df, axis=1)
#fin_df2.PH_CustomerType.unique()
#fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)
#
#

###### AgeGroup and MaritalStatus #########
fin_df2['maritalstatus']=fin_df2['maritalstatus'].fillna('NA')

def agegrp_df(value):
    if value['CustomerTypeAgePH'] == 'Teen child Dependent customer' and value['maritalstatus'] == 'Single':
        return "Single Teen child Dependent customer"
    elif value['CustomerTypeAgePH'] == 'value NA or New born baby Dependent customer' and value['maritalstatus'] == 'Single':
        return "value NA or Single New born baby Dependent customer"
    elif  value['CustomerTypeAgePH'] == 'Young child PH customer' and value['maritalstatus'] == 'Single':
        return "Young Single child PH customer"
    elif  value['CustomerTypeAgePH'] == 'Teen child PH customer' and value['maritalstatus'] == 'Single':
        return "Teen Single child PH customer"
    elif  value['CustomerTypeAgePH'] == 'Young Dependent Customer' and value['maritalstatus'] == 'Single':
        return "Young Single Dependent Customer"
    elif  value['CustomerTypeAgePH'] == 'value NA or New born baby PH customer' and value['maritalstatus'] == 'Single':
        return "value NA or Single New born baby PH customer"
    elif  value['CustomerTypeAgePH'] == 'Matured Dependent Customer' and value['maritalstatus'] == 'Single':
        return "Matured Dependent Single Customer"
    elif  value['CustomerTypeAgePH'] == 'Young PH Customer' and value['maritalstatus'] == 'Single':
        return "Young PH Single Customer"
    elif  value['CustomerTypeAgePH'] == 'Senior Citizen Dependent Customer' and value['maritalstatus'] == 'Single':
        return "Senior Citizen Single Dependent Customer"
    elif  value['CustomerTypeAgePH'] == 'Old Dependent Customer' and value['maritalstatus'] == 'Single':
        return "Old Dependent Single Customer"
    elif  value['CustomerTypeAgePH'] == 'Senior Citizen PH Customer' and value['maritalstatus'] == 'Single':
        return "Senior Citizen PH Single Customer"
    elif  value['CustomerTypeAgePH'] == 'Info NA' and (value['maritalstatus'] == 'Single' or value['maritalstatus'] == 'Married' or value['maritalstatus'] == 'Divorce' or value['maritalstatus'] == 'Other' or value['maritalstatus'] == 'Widow' or value['maritalstatus'] == 'NA'):
        return "Info NA"
    elif (value['CustomerTypeAgePH'] == 'Teen child Dependent customer' or value['CustomerTypeAgePH'] == 'Info NA' or value['CustomerTypeAgePH'] == 'value NA or New born baby Dependent customer' or  value['CustomerTypeAgePH'] == 'Young child PH customer' or value['CustomerTypeAgePH'] == 'Teen child PH customer' or value['CustomerTypeAgePH'] == 'Young Dependent Customer' or value['CustomerTypeAgePH'] == 'value NA or New born baby PH customer' or value['CustomerTypeAgePH'] == 'Matured Dependent Customer' or  value['CustomerTypeAgePH'] == 'Young PH Customer' or value['CustomerTypeAgePH'] == 'Senior Citizen Dependent Customer' or  value['CustomerTypeAgePH'] == 'Old Dependent Customer' or value['CustomerTypeAgePH'] == 'Senior Citizen PH Customer') and value['maritalstatus'] == 'NA' :
        return "Info NA"
    elif value['CustomerTypeAgePH'] == 'Young Dependent Customer' and value['maritalstatus'] == 'Married':
        return "Married Young Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Young PH Customer' and value['maritalstatus'] == 'Married':
        return "Married Young PH Customer"
    elif value['CustomerTypeAgePH'] == 'Matured PH Customer' and value['maritalstatus'] == 'Married':
        return "Married Matured PH Customer"
    elif value['CustomerTypeAgePH'] == 'Matured Dependent Customer' and value['maritalstatus'] == 'Married':
        return "Married Matured Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Senior Citizen PH Customer' and value['maritalstatus'] == 'Married':
        return "Married Senior Citizen PH Customer"
    elif value['CustomerTypeAgePH'] == 'Senior Citizen Dependent Customer' and value['maritalstatus'] == 'Married':
        return "Married Senior Citizen Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Old Dependent Customer' and value['maritalstatus'] == 'Married':
        return "Married Old Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Senior Citizen PH Customer' and value['maritalstatus'] == 'Married':
        return "Married Senior Citizen PH Customer"
    elif value['CustomerTypeAgePH'] == ' Matured PH Customer' and value['maritalstatus'] == 'Married':
        return "Married Matured PH Customer"
    elif  value['CustomerTypeAgePH'] == 'Old PH Customer' and value['maritalstatus'] == 'Married':
        return "Married Old PH Customer"
    elif value['CustomerTypeAgePH'] == 'Young Dependent Customer' and value['maritalstatus'] == 'Divorce':
        return "Divorce Young Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Young PH Customer' and value['maritalstatus'] == 'Divorce':
        return "Divorce Young PH Customer"
    elif value['CustomerTypeAgePH'] == 'Matured PH Customer' and value['maritalstatus'] == 'Divorce':
        return "Divorce Matured PH Customer"
    elif value['CustomerTypeAgePH'] == 'Matured Dependent Customer' and value['maritalstatus'] == 'Divorce':
        return "Divorce Matured Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Senior Citizen PH Customer' and value['maritalstatus'] == 'Divorce':
        return "Divorce Senior Citizen PH Customer"
    elif value['CustomerTypeAgePH'] == 'Senior Citizen Dependent Customer' and value['maritalstatus'] == 'Divorce':
        return "Divorce Senior Citizen Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Old Dependent Customer' and value['maritalstatus'] == 'Divorce':
        return "Divorce Old Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Senior Citizen PH Customer' and value['maritalstatus'] == 'Divorce':
        return "Divorce Senior Citizen PH Customer"
    elif value['CustomerTypeAgePH'] == ' Matured PH Customer' and value['maritalstatus'] == 'Divorce':
        return "Divorce Matured PH Customer"
    elif  value['CustomerTypeAgePH'] == 'Old PH Customer' and value['maritalstatus'] == 'Divorce':
        return "Divorce Old PH Customer"
    elif value['CustomerTypeAgePH'] == 'Young Dependent Customer' and value['maritalstatus'] == 'Widow':
        return "Widow Young Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Young PH Customer' and value['maritalstatus'] == 'Widow':
        return "Widow Young PH Customer"
    elif value['CustomerTypeAgePH'] == 'Matured PH Customer' and value['maritalstatus'] == 'Widow':
        return "Widow Matured PH Customer"
    elif value['CustomerTypeAgePH'] == 'Matured Dependent Customer' and value['maritalstatus'] == 'Widow':
        return "Widow Matured Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Senior Citizen PH Customer' and value['maritalstatus'] == 'Widow':
        return "Widow Senior Citizen PH Customer"
    elif value['CustomerTypeAgePH'] == 'Senior Citizen Dependent Customer' and value['maritalstatus'] == 'Widow':
        return "Widow Senior Citizen Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Old Dependent Customer' and value['maritalstatus'] == 'Widow':
        return "Widow Old Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Senior Citizen PH Customer' and value['maritalstatus'] == 'Widow':
        return "Widow Senior Citizen PH Customer"
    elif value['CustomerTypeAgePH'] == ' Matured PH Customer' and value['maritalstatus'] == 'Widow':
        return "Widow Matured PH Customer"
    elif  value['CustomerTypeAgePH'] == 'Old PH Customer' and value['maritalstatus'] == 'Widow':
        return "Widow Old PH Customer"
    elif value['CustomerTypeAgePH'] == 'Young Dependent Customer' and value['maritalstatus'] == 'Other':
        return "Other Young Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Young PH Customer' and value['maritalstatus'] == 'Other':
        return "Other Young PH Customer"
    elif value['CustomerTypeAgePH'] == 'Matured PH Customer' and value['maritalstatus'] == 'Other':
        return "Other Matured PH Customer"
    elif value['CustomerTypeAgePH'] == 'Matured Dependent Customer' and value['maritalstatus'] == 'Other':
        return "Other Matured Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Senior Citizen PH Customer' and value['maritalstatus'] == 'Other':
        return "Other Senior Citizen PH Customer"
    elif value['CustomerTypeAgePH'] == 'Senior Citizen Dependent Customer' and value['maritalstatus'] == 'Other':
        return "Other Senior Citizen Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Old Dependent Customer' and value['maritalstatus'] == 'Other':
        return "Other Old Dependent Customer"
    elif value['CustomerTypeAgePH'] == 'Senior Citizen PH Customer' and value['maritalstatus'] == 'Other':
        return "Other Senior Citizen PH Customer"
    elif value['CustomerTypeAgePH'] == ' Matured PH Customer' and value['maritalstatus'] == 'Other':
        return "Other Matured PH Customer"
    elif  value['CustomerTypeAgePH'] == 'Old PH Customer' and value['maritalstatus'] == 'Other':
        return "Other Old PH Customer"
    else:
        return "Others"
fin_df2['customer_maritalgrp'] = fin_df2.apply(agegrp_df, axis=1)
fin_df2.customer_maritalgrp.unique()
fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)


###### Family Group bucket ######### Not Needed : refer next step


#
#def agegrp_df(value):
#    if value['customer_maritalgrp'] == 'Widow Matured Dependent Customer' and value['totalkids'] == 0:
#        return "Widow Matured Dependent Customer with no kid"
#    elif value['customer_maritalgrp'] == 'Widow Matured Dependent Customer' and value['totalkids'] != 0:
#        return "Widow Matured Dependent Parent"
#    elif value['customer_maritalgrp'] == 'Young Couple' and value['totalkids'] == 0:
#        return "Young Couple "
#    elif  value['customer_maritalgrp'] == 'Young Couple' and value['totalkids'] < 3 :
#        return "Young Small Family"
#    elif  value['customer_maritalgrp'] == 'Young Couple' and value['totalkids'] > 2 :
#        return "Young large Family"
#    elif  value['customer_maritalgrp'] == 'Old Single' and value['totalkids'] == 0:
#        return "Old Single"
#    elif  value['customer_maritalgrp'] == 'Old Single' and value['totalkids'] != 0:
#        return "Old Single Parent"
#    elif value['customer_maritalgrp'] == 'Old Couple' and value['totalkids'] == 0:
#        return "Old Couple"
#    elif  value['customer_maritalgrp'] == 'Old Couple' and value['totalkids'] < 3 :
#        return "Old Small Family"
#    elif  value['customer_maritalgrp'] == 'Old Couple' and value['totalkids'] > 2 :
#        return "Old large Family"
#    elif  value['customer_maritalgrp'] == 'Matured Single' and value['totalkids'] == 0:
#        return "Matured Single"
#    elif  value['customer_maritalgrp'] == 'Matured Single' and value['totalkids'] != 0:
#        return "Matured Single Parent"
#    elif value['customer_maritalgrp'] == 'Matured Couple' and value['totalkids'] == 0:
#        return "Matured Couple"
#    elif  value['customer_maritalgrp'] == 'Matured Couple' and value['totalkids'] < 3 :
#        return "Matured Small Family"
#    elif value['customer_maritalgrp'] == 'Matured Couple' and value['totalkids'] > 2:
#        return "Matured large Family"
#    else:
#        return "Others"
#
#fin_df2['familygrp1'] = fin_df2.apply(agegrp_df, axis=1)

######## Kids status in the family

def agegrp_df(value):
    if  value['totalkids'] == 0:
        return "no kids"
    elif value['totalkids'] != 0:
        return "has kids"
    else:
        return "Others"
fin_df2['kids_status'] = fin_df2.apply(agegrp_df, axis=1)
fin_df2.kids_status.unique()
fin_df2 = fin_df2.drop_duplicates(subset=None, keep='first', inplace=False)
##############################################################
def agegrp_df(value):
    if value['customer_maritalgrp'] == 'Widow Matured Dependent Customer' and value['totalkids'] == 0:
        return "Widow Matured Dependent Customer with no kid"
    elif value['customer_maritalgrp'] == 'Widow Matured Dependent Customer' and value['totalkids'] != 0:
        return "Widow Matured Dependent Parent"
    elif value['customer_maritalgrp'] == 'Young Couple' and value['totalkids'] == 0:
        return "Young Couple "
    elif  value['customer_maritalgrp'] == 'Young Couple' and value['totalkids'] < 3 :
        return "Young Small Family"
    elif  value['customer_maritalgrp'] == 'Young Couple' and value['totalkids'] > 2 :
        return "Young large Family"
    elif  value['customer_maritalgrp'] == 'Old Single' and value['totalkids'] == 0:
        return "Old Single"
    elif  value['customer_maritalgrp'] == 'Old Single' and value['totalkids'] != 0:
        return "Old Single Parent"
    elif value['customer_maritalgrp'] == 'Old Couple' and value['totalkids'] == 0:
        return "Old Couple"
    elif  value['customer_maritalgrp'] == 'Old Couple' and value['totalkids'] < 3 :
        return "Old Small Family"
    elif  value['customer_maritalgrp'] == 'Old Couple' and value['totalkids'] > 2 :
        return "Old large Family"
    elif  value['customer_maritalgrp'] == 'Matured Single' and value['totalkids'] == 0:
        return "Matured Single"
    elif  value['customer_maritalgrp'] == 'Matured Single' and value['totalkids'] != 0:
        return "Matured Single Parent"
    elif value['customer_maritalgrp'] == 'Matured Couple' and value['totalkids'] == 0:
        return "Matured Couple"
    elif  value['customer_maritalgrp'] == 'Matured Couple' and value['totalkids'] < 3 :
        return "Matured Small Family"
    elif value['customer_maritalgrp'] == 'Matured Couple' and value['totalkids'] > 2:
        return "Matured large Family"
    else:
        return "Others"

fin_df2['familygrp1'] = fin_df2.apply(agegrp_df, axis=1)
###### Family Group bucket #########
def agegrp_df(value):
    if value['familygrp1'] == 'Young Single' and (value['TodCount'] == 0 or value['YoungCount'] == 0):
        return "Young Single"
    elif value['familygrp1'] == 'Young Single Parent' and (value['TodCount'] != 0 or value['YoungCount'] != 0):
        return "Young Single Parent with Tod / Young"
    elif value['familygrp1'] == 'Young Single Parent' and (value['TeenCount'] != 0 or value['GradCount'] != 0):
        return "Young Single Parent with Teen / Grad kids"
    elif value['familygrp'] == 'Young Couple' and (value['TodCount'] == 0 or value['YoungCount'] == 0):
        return "Young Couple"
    elif  value['familygrp'] == 'Young Small Family' and (value['TodCount'] > 0 or value['YoungCount'] >0) :
        return "Young Small Family with Tod / Young"
    elif  value['familygrp'] == 'Young Small Family' and (value['TeenCount'] > 0 or value['GradCount'] >0) :
        return "Young Small Family with Teen / Grad kids"
    elif  value['familygrp'] == 'Young large Family' and (value['TodCount'] > 0 or value['YoungCount'] > 0):
        return "Young large Family with Tod / Young"
    elif value['familygrp'] == 'Young large Family' and (value['TeenCount'] > 0 or value['GradCount'] > 0):
        return "Young large Family with Teen / Grad kids"
    elif  value['familygrp'] == 'Matured Single' and (value['TodCount'] == 0 or value['YoungCount'] == 0):
        return "Matured Single"
    elif  value['familygrp'] == 'Matured Single Parent' and (value['TodCount'] > 0 or value['YoungCount'] > 0):
        return "Matured Single Parent with Tod / Young"
    elif  value['familygrp'] == 'Matured Single Parent' and (value['TeenCount'] > 0 or value['GradCount'] > 0):
        return "Matured Single Parent with Teen / Grad kids"
    elif value['familygrp'] == 'Matured Couple' and (value['TodCount'] == 0 or value['YoungCount'] == 0):
        return "Matured Couple"
    elif  value['familygrp'] == 'Matured Small Family' and (value['TodCount'] > 0 or value['YoungCount'] >0) :
        return "Matured Small Family with Tod / Young"
    elif  value['familygrp'] == 'Matured Small Family' and (value['TeenCount'] > 0 or value['GradCount'] >0) :
        return "Matured Small Family with Teen / Grad kids"
    elif  value['familygrp'] == 'Matured large Family' and (value['TodCount'] > 0 or value['YoungCount'] > 0):
        return "Matured large Family with Tod / Young"
    elif value['familygrp'] == 'Matured large Family' and (value['TeenCount'] > 0 or value['GradCount'] > 0):
        return "Matured large Family with Teen / Grad kids"
    elif  value['familygrp'] == 'Old Single' and (value['TodCount'] == 0 or value['YoungCount'] == 0):
        return "Old Single"
    elif  value['familygrp'] == 'Old Single Parent' and (value['TodCount'] > 0 or value['YoungCount'] > 0):
        return "Old Single Parent with Tod / Young"
    elif  value['familygrp'] == 'Old Single Parent' and (value['TeenCount'] > 0 or value['GradCount'] > 0):
        return "Old Single Parent with Teen / Grad kids"
    elif value['familygrp'] == 'Old Couple' and (value['TodCount'] == 0 or value['YoungCount'] == 0):
        return "Old Couple"
    elif  value['familygrp'] == 'Old Small Family' and (value['TodCount'] > 0 or value['YoungCount'] >0) :
        return "Old Small Family with Tod / Young"
    elif  value['familygrp'] == 'Old Small Family' and (value['TeenCount'] > 0 or value['GradCount'] >0) :
        return "Old Small Family with Teen / Grad kids"
    elif  value['familygrp'] == 'Old large Family' and (value['TodCount'] > 0 or value['YoungCount'] > 0):
        return "Old large Family with Tod / Young"
    elif value['familygrp'] == 'Old large Family' and (value['TeenCount'] > 0 or value['GradCount'] > 0):
        return "Old large Family with Teen / Grad kids"
    else:
        return "Others"

fin_df2['familyKidgrp1'] = fin_df2.apply(agegrp_df, axis=1)




###### HouseHold Group bucket #########
def agegrp_df(value):
    if value['familyKidgrp'] == 'Young Single' and (value['MembersActive'] == 1):
        return "Young Single household"
    elif value['familyKidgrp'] == 'Young Couple' and (value['MembersActive'] > 1 and value['MembersActive'] <3):
        return "Young Couple household"
    elif  value['familyKidgrp'] == 'Young Small Family with Tod / Young' and (value['MembersActive'] > 2 or value['MembersActive'] < 5) :
        return "Small Young household with Tod / Young"
    elif  value['familyKidgrp'] == 'Young Small Family with Tod / Young' and (value['MembersActive'] > 4 ) :
        return "Large Young household with Tod / Young"
    elif  value['familyKidgrp'] == 'Young Small Family with Teen / Grad kids' and (value['MembersActive'] > 2 or value['MembersActive'] < 5) :
        return "Small Young household with Teen / Grad kids"
    elif  value['familyKidgrp'] == 'Young Small Family with Teen / Grad kids' and (value['MembersActive'] > 4 ) :
        return "Large Young household with Teen / Grad kids"
    elif value['familyKidgrp'] == 'Matured Single' and (value['MembersActive'] == 0 ):
        return "Matured Single household"
    elif value['familyKidgrp'] == 'Matured Couple' and (value['MembersActive'] > 1 and value['MembersActive'] <3):
        return "Matured Couple household"
    elif  value['familyKidgrp'] == 'Matured Small Family with Tod / Young' and (value['MembersActive'] > 2 or value['MembersActive'] < 5) :
        return "Small Matured household with Tod / Young"
    elif  value['familyKidgrp'] == 'Matured Small Family with Tod / Young' and (value['MembersActive'] > 4 ) :
        return "Large Matured household with Tod / Young"
    elif  value['familyKidgrp'] == 'Matured Small Family with Teen / Grad kids' and (value['MembersActive'] > 2 or value['MembersActive'] < 5) :
        return "Small Matured household with Teen / Grad kids"
    elif  value['familyKidgrp'] == 'Matured Small Family with Teen / Grad kids' and (value['MembersActive'] > 4 ) :
        return "Large Matured household with Teen / Grad kids"
    elif value['familyKidgrp'] == 'Old Single' and (value['MembersActive'] == 0 ):
        return "Old Single household"
    elif value['familyKidgrp'] == 'Old Couple' and (value['MembersActive'] > 1 and value['MembersActive'] <3):
        return "Old Couple household"
    elif  value['familyKidgrp'] == 'Old Small Family with Tod / Young' and (value['MembersActive'] > 2 or value['MembersActive'] < 5) :
        return "Small Old household with Tod / Young"
    elif  value['familyKidgrp'] == 'Old Small Family with Tod / Young' and (value['MembersActive'] > 4 ) :
        return "Large Old household with Tod / Young"
    elif  value['familyKidgrp'] == 'Old Small Family with Teen / Grad kids' and (value['MembersActive'] > 2 or value['MembersActive'] < 5) :
        return "Small Old household with Teen / Grad kids"
    elif  value['familyKidgrp'] == 'Old Small Family with Teen / Grad kids' and (value['MembersActive'] > 4 ) :
        return "Large Old household with Teen / Grad kids"
    else:
        return "Others"

fin_df2['household_bucket'] = fin_df2.apply(agegrp_df, axis=1)

#Writing Results

fin_df2.to_csv(path+"LifeStage_bucket_FamilyLevel.csv", header = True, index = False)

fin_df3 = fin_df2[['hid', 'maritalgrp', 'familygrp', 'familyKidgrp',      'familygrp1', 'familyKidgrp1']]

fin_df3.to_csv(path+"LifeStage_bucket_FamilyLevel_score.csv", header = True, index = False)

# Generating Final Score

life = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/lifeStage_score.csv"
#reading hh_trav_country_score data
lifeStage_score = pd.read_csv(life, low_memory = True)
lifeStage_score.columns

# Merging hh_vhbrand_score with result1 data
life_result = fin_df2.merge(lifeStage_score, on='familygrp1', how ='left'  )
life_result = life_result.fillna(0)
life_result.columns
len(life_result)
life_result1 = life_result[['hid', 'ageph',   'customertype',  'MembersCount',
        'TodCount', 'YoungCount', 'TeenCount', 'GradCount',
       'totalkids',  'maritalstatus', 'total_premium', 'premiumbucket', 'AgeGroup',
        'familyKidgrp1', 'FinalWeightScore']]

need to test the sum

life_result1 = life_result1.groupby('hid', group_keys=False).apply(lambda x: x.loc[x.FinalWeightScore.idxmax()])
life_result1 = life_result1.drop_duplicates(subset=None, keep='first', inplace=False)
life_result1.to_csv(path+"FinalHouseHoldData_overall.csv", header = True, index = False)












result1 = result.groupby('hid', group_keys=False).apply(lambda x: x.loc[x.FinalScoreEdu.idxmax()])
len(result1)
type(result1)
result1.columns

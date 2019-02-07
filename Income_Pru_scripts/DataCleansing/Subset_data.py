# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 16:31:12 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np

# Data Cleansing

#datf = pd.read_csv(path, low_memory = True)
#datf.columns
#datf.travelcountry.unique()
#datf['travelcountry'] = datf.travelcountry.replace('"', '')
#datf.columns
#datf.travelcountry.unique()
#datf.to_csv(path+"country_clean.csv", header = True)

#Merging HH data with travelpolicy
path_data = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/HouseHold_FinalDataClean.csv"
#path1 = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/travel_clean_country.csv"

df_fl = pd.read_csv(path_data, low_memory = True)
#df.columns

# Creating Subset
df_f2 = df_fl[['hid','customerseqid_x','totalpremium','productseqid', 'productname','vehbrand', 'vehtypename', 'vehage','educationlevel', 'postalcode','addr_type_desc','travelcountry' ]]
df_f2.columns
# Groupby
df1= df1.groupby('hid', axis=0).sum()
df2 = df[['hid','addr_type_desc']]
# Removing duplicates
df2 = df2.drop_duplicates(subset=None, keep='first', inplace=False)
df2.to_csv(path+"hhdata_dwellinginfo.csv", header = True, index=False)

# Creating education subset
df_f3 = df_f2[['hid','educationlevel']]
df_f3 = df_f3.drop_duplicates(subset=None, keep='first', inplace=False)
df_f3['educationlevel'] = df_f3.educationlevel.replace('"N Level', 'N Level')
df_f3.to_csv(path_data+"hh_educationdata.csv", header = True, index = False)


# Creating vehAge subset
df_f3 = df_f2[['hid','vehage']]
df_f3 = df_f3.drop_duplicates(subset=None, keep='first', inplace=False)
df_f3.columns
len(df_f3)
df_f3.to_csv(path_data+"hh_vehAge.csv", header = True, index = False)

# Creating vehbrand subset
df_f3 = df_f2[['hid','vehbrand']]
df_f3 = df_f3.drop_duplicates(subset=None, keep='first', inplace=False)
df_f3.columns
len(df_f3)
df_f3.to_csv(path_data+"hh_vehbrand.csv", header = True, index = False)

# Creating country subset
df_f3 = df_f2[['hid','travelcountry']]
df_f3 = df_f3.drop_duplicates(subset=None, keep='first', inplace=False)
df_f3.columns
len(df_f3)
df_f3.to_csv(path_data+"hh_travelcountry.csv", header = True, index = False)

# Creating dwellingType subset
df_f3 = df_f2[['hid','addr_type_desc']]
df_f3 = df_f3.drop_duplicates(subset=None, keep='first', inplace=False)
df_f3.columns
len(df_f3)
df_f3.to_csv(path_data+"hh_addr_type_desc.csv", header = True, index = False)

# Creating postalcode subset
df_f3 = df_f2[['hid','postalcode']]
df_f3 = df_f3.drop_duplicates(subset=None, keep='first', inplace=False)
df_f3.columns
df_f3.postalcode.unique()
df_f3['postalcode'] = df_f3.postalcode.replace(' Doctorate"', 0)
df_f3.columns
df_f3.postalcode.unique()
len(df_f3)
df_f3.to_csv(path_data+"hh_postalcode.csv", header = True, index = False)

# Creating vehtypename subset
df_f3 = df_f2[['hid','vehtypename']]
df_f3 = df_f3.drop_duplicates(subset=None, keep='first', inplace=False)
df_f3.columns
len(df_f3)
df_f3.to_csv(path_data+"hh_vehtypename.csv", header = True, index = False)

# Creating vehtypename subset
df_f3 = df_f2[['hid','vehtypename']]
df_f3 = df_f3.drop_duplicates(subset=None, keep='first', inplace=False)
df_f3.columns
len(df_f3)
df_f3.to_csv(path_data+"hh_vehtypename.csv", header = True, index = False)
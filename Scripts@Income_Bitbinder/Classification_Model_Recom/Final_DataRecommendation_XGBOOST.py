# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 16:31:12 2018

@author: LatizeExpress

Final Data: Data buckets and Gboost feasible data
"""

#Library declaration
import pandas as pd
import numpy as np

##Data Sources
pathread =  "E:/NTUC/raw_data/Final/hh_result_final/FinalResults_with_Bucket/"
pathwrite =  "E:/NTUC/raw_data/clean_raw_data/Final_recom_data/"
path_product = "E:/NTUC/raw_data/clean_raw_data/Final_recom_data/unique_Product_list.csv"
path_clnData = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/HouseHold_FinalDataClean.csv"

#Reading clean data
df_cln = pd.read_csv(path_clnData, low_memory = True)
df_cln.columns # Displaying columns / headings in the data file
len(df_cln.columns)#33 columns
len(df_cln)   # 1409334 records
len(df_cln.hid.unique()) # 405480 unique household ids
#Reading Product list (final list from Aswin data)
df_prdt = pd.read_csv(path_product, low_memory = True)
df_prdt.columns  # Displaying Columns
len(df_prdt.columns) # 3 columns

# Subseting of clean data file to be used as feature set

df_cln1 = df_cln[['hid', 'customerseqid_x', 'customerstatus', 'genderph','policyseqid_x',
       'totalpremium', 'sumassured', 'productseqid', 'productname',
       'policystatuscategory', 'policytype', 'productline', 'productcategory',
       'productsubcategory', 'ismain']]

# Renaming few columns
df_cln1.columns = ['hid', 'customerseqid', 'customerstatus', 'genderph','policyseqid',
       'totalpremium', 'sumassured', 'productseqid', 'productname',
       'policystatuscategory', 'policytype', 'productline', 'productcategory',
       'productsubcategory', 'ismain']

df_cln1.productline.unique() # displaying unique business lines ['GH', 'LI', 'GI']

df_cln1 = df_cln1[df_cln1['productline'] != 'GI'] # Remooving "GI" business line

len(df_cln1) # 1204228 number of records after GI removal

len(df_cln1.hid.unique()) # 388428 number of unique household ids after GI removal

df_cln1.columns # column list
len(df_cln1.columns) #15 columns in the new subset

#df_cln1['productline'] = df_cln1['productline'].replace('GH', 'Health') # Replacing "GH" with "Health"

df_cln1['productline'] = df_cln1['productline'].replace('LI',1) #Repacing "LI" to 1
df_cln1.productline.unique()
df_cln1['productline'] = df_cln1['productline'].replace('GH',2)#Repacing "GH" to 2
df_cln1.productline.unique()
len(df_cln1) # 1204228 number of records
len(df_cln1.columns) #15 columns in the new subset
df_cln1.policystatuscategory.unique() # Policy Status = ['In force']
df_cln1.productcategory.unique()  # Product Category 'IS', 'PARTICIPATING', 'TRADITIONAL', 'ELS', 'NEW UL PRODUCT', 'UNIT LINKED', 'DPS', 'MHS'

# Merge Product data with clean data (Left Join)
df_merge = df_cln1.merge(df_prdt, on = 'productname', how = 'left')
df_merge.columns
len(df_merge.columns)  #17 columns in the new subset
df_merge.Category_list.unique() # Category list = [nan, 'Savings', 'Protection', 'Health', 'ILP', 'Annuity', 'Others']
df_merge.Category_data.unique() # Category Data = ['Health ', 'PARTICIPATING', 'TRADITIONAL', 'ELS', 'NEW UL PRODUCT', 'UNIT LINKED', 'DPS', 'MHS']

len(df_merge)#1204228 number of records

len(df_merge.hid.unique()) #388428 after removing GI products
#df_merge = df_merge[['hid', 'customerseqid', 'customerstatus', 'genderph', 'policyseqid',
#       'totalpremium', 'sumassured', 'productseqid', 'productname',
#       'policystatuscategory', 'policytype', 'productline', 'productcategory','productsubcategory', 'ismain', 'Category_list']]

df_merge.productcategory.unique()
df_merge.Category_list.unique()
df_merge.productline.unique() #['GH', 'LI']
df_merge.customerstatus.unique() # ['ACTIVE']
df_merge.policytype.unique() # ['Individual', 'INDIVIDUAL']
df_merge.Category_data.unique()
#df_merge['productline'] = df_merge['productline'].replace('GH', 'Health')
df_merge['policytype'] = df_merge['policytype'].replace('INDIVIDUAL', 'Individual') # Replacing INDIVIDUAL to Individual
df_merge.productline.unique()
df_merge.ismain.unique()
df_merge['ismain'] = df_merge['ismain'].replace('YES', 1)
df_merge['ismain'] = df_merge['ismain'].replace('NO', 2)

df_merge.genderph.unique()
df_merge['genderph'] = df_merge['genderph'].fillna(0)
df_merge['genderph'] = df_merge['genderph'].replace('Male', 1) # Coding to Gender to be used in the model
df_merge['genderph'] = df_merge['genderph'].replace('Female', 2)



len(df_merge)  # 1204228 records
df_merge.columns
path_out = 'E:/NTUC/raw_data/Final/hh_result_final/FinalResults_with_Bucket/'   # Ottput source

#df_merge.to_csv(path_out+"data_merge.csv", index = False, header = True)
#
#df_prdtcat_count = df_merge.reset_index().groupby('hid')['Category_list'].value_counts()
#df_prdtvalcount = df_merge.reset_index().groupby('hid')['productname'].value_counts()
#df_prdtcount = df_merge.reset_index().groupby('hid')[['productname']].count()
#df_prdt_Cat_count = df_merge.reset_index().groupby('hid')[['Category_list']].count()

#df_prdtcat_count = df_prdtcat_count.to_frame()
#df_prdtvalcount = df_prdtvalcount.to_frame()
#df_prdt_Cat_count = df_prdt_Cat_count.to_frame()
#df_prdtcount = df_prdtcount.to_frame()

df_segment = pd.read_csv(pathread + "MicroSegmentProfile_final.csv", low_memory = True)  # Reading Microsegment Data
df_segment.columns
df_merge.columns
df_final_data = df_merge.merge(df_segment, on = 'hid', how = 'left') # Merge Microsegment data with subset data
df_final_data.columns  # Total 52 Colummns
len(df_final_data.columns)
len(df_final_data) #1204228 columns

df_final_data.MicroSegmentProfile.unique()
df_final_data.productcategory.unique()
df_final_data.productsubcategory.unique()
df_final_data.productline.unique()
df_final_data.Category_list.unique()
df_final_data.premiumbucket.unique()
df_final_data.PremiumCategory.unique()

# Codification of the values of features to be used in the model
df_final_data['PremiumCategory'] = df_final_data['PremiumCategory'].replace('HighlyPaid Premium', 1)
df_final_data['PremiumCategory'] = df_final_data['PremiumCategory'].replace('ModeratlyPaid Premium', 2)
df_final_data['PremiumCategory'] = df_final_data['PremiumCategory'].replace('LowPaid Premium', 3)
df_final_data['PremiumCategory'] = df_final_data['PremiumCategory'].replace('0', 0)

df_final_data.EducationLevel.unique()
df_final_data['EducationLevel'] = df_final_data['EducationLevel'].replace('Professional', 1)
df_final_data['EducationLevel'] = df_final_data['EducationLevel'].replace('University', 2)
df_final_data['EducationLevel'] = df_final_data['EducationLevel'].replace('DiplomaHolder', 3)
df_final_data['EducationLevel'] = df_final_data['EducationLevel'].replace('A Level', 4)
df_final_data['EducationLevel'] = df_final_data['EducationLevel'].replace('O Level', 5)
df_final_data['EducationLevel'] = df_final_data['EducationLevel'].replace('N Level Passed', 6)
df_final_data['EducationLevel'] = df_final_data['EducationLevel'].replace('Secondary', 7)
df_final_data['EducationLevel'] = df_final_data['EducationLevel'].replace('Primary passed', 8)
df_final_data['EducationLevel'] = df_final_data['EducationLevel'].replace('0', 0)
df_final_data['EducationLevel'] = df_final_data['EducationLevel'].replace('Others', 9)



df_final_data.addr_type_desc.unique()
df_final_data['addr_type_desc'] = df_final_data['addr_type_desc'].replace('Condominium', 1)
df_final_data['addr_type_desc'] = df_final_data['addr_type_desc'].replace('HDB Block', 2)
df_final_data['addr_type_desc'] = df_final_data['addr_type_desc'].replace('Standard', 3)
df_final_data['addr_type_desc'] = df_final_data['addr_type_desc'].replace('Apartment', 4)
df_final_data['addr_type_desc'] = df_final_data['addr_type_desc'].replace('Oversea', 5)
df_final_data['addr_type_desc'] = df_final_data['addr_type_desc'].replace('Walkup', 6)
df_final_data['addr_type_desc'] = df_final_data['addr_type_desc'].replace('Other', 7)
df_final_data['addr_type_desc'] = df_final_data['addr_type_desc'].replace('0', 0)


df_final_data.District_Iiving.unique()
df_final_data['District_Iiving'] = df_final_data['District_Iiving'].replace('Inner North ', 1)
df_final_data['District_Iiving'] = df_final_data['District_Iiving'].replace('Inner city ', 2)
df_final_data['District_Iiving'] = df_final_data['District_Iiving'].replace('City & South West ', 3)
df_final_data['District_Iiving'] = df_final_data['District_Iiving'].replace('Outer North ', 4)
df_final_data['District_Iiving'] = df_final_data['District_Iiving'].replace('City fringe ', 5)
df_final_data['District_Iiving'] = df_final_data['District_Iiving'].replace('East ', 6)
df_final_data['District_Iiving'] = df_final_data['District_Iiving'].replace('East Coast', 7)
df_final_data['District_Iiving'] = df_final_data['District_Iiving'].replace('Outer City', 8)
df_final_data['District_Iiving'] = df_final_data['District_Iiving'].replace('West ', 9)
df_final_data['District_Iiving'] = df_final_data['District_Iiving'].replace('0', 0)

df_final_data.Affluence_Bucket.unique()
df_final_data['Affluence_Bucket'] = df_final_data['Affluence_Bucket'].replace('VERY HIGH', 1)
df_final_data['Affluence_Bucket'] = df_final_data['Affluence_Bucket'].replace('HIGH', 2)
df_final_data['Affluence_Bucket'] = df_final_data['Affluence_Bucket'].replace('MEDIUM', 3)
df_final_data['Affluence_Bucket'] = df_final_data['Affluence_Bucket'].replace('LOW', 4)

df_final_data.AgeGroup.unique()
df_final_data.PH_AgeGroup.unique()
df_final_data['PH_AgeGroup'] = df_final_data['PH_AgeGroup'].replace('Old Customer', 1)
df_final_data['PH_AgeGroup'] = df_final_data['PH_AgeGroup'].replace('Matured Customer', 2)
df_final_data['PH_AgeGroup'] = df_final_data['PH_AgeGroup'].replace('Young Customer', 3)
df_final_data['PH_AgeGroup'] = df_final_data['PH_AgeGroup'].replace('value NA or Insured New born baby', 4)
df_final_data['PH_AgeGroup'] = df_final_data['PH_AgeGroup'].replace('Teen child', 5)
df_final_data['PH_AgeGroup'] = df_final_data['PH_AgeGroup'].replace('Young child', 6)
df_final_data['PH_AgeGroup'] = df_final_data['PH_AgeGroup'].fillna(0)
#df_final_data = df_final_data.loc[~df_final_data['productsubcategory'].isin(['ELS'])]
#df_final_data = df_final_data.loc[~df_final_data['productsubcategory'].isin(['DPS'])]
#df_final_data = df_final_data.loc[~df_final_data['productsubcategory'].isin(['MHS'])]



# Removing 'ELS', 'DPS', 'MHS', and filling blanks with NA
df_final_data = df_final_data[df_final_data['productsubcategory'] != 'ELS']
df_final_data = df_final_data[df_final_data['productsubcategory'] != 'DPS']
df_final_data = df_final_data[df_final_data['productsubcategory'] != 'MHS']
df_final_data['Category_list'] = df_final_data['Category_list'].fillna('NA')
df_final_data['Category_list'] = df_final_data['Category_list'].fillna('NA')

# Removing all NA records
df_final_data_tmp = df_final_data[df_final_data['Category_list'] != 'NA']

#
len(df_final_data.hid.unique()) #280345 unique Household Ids
len(df_final_data_tmp.hid.unique()) #181767 unique Household Ids after deleting NA and other records
len(df_final_data_tmp)#384355 number of records after deleting NA and other records
len(df_final_data) #856681 number of records after deleting ELS, DPS and MHS
df_final_data_tmp.productline.unique()
len(df_final_data_tmp.columns)

#Writing files
df_final_data.to_csv(pathread+"final_data_xboost.csv", index = False, header = True)
df_final_data_tmp.to_csv(pathread+"final_data_temp_xboost.csv", index = False, header = True)



##########################################################################################################################
#def write_file(pd_name, filename):
#    pd_name.to_csv(pathwrite+filename+".csv", header = True, index = False)
#
#def readfile(pathread):
#    df = pd.read_csv(pathread, low_memory = True)
#    return df
#
#
## Reading FinalHouseHold Affluence Data
#fhhPD = pd.read_csv(pathread+'Household_Affluence_Result.csv', low_memory = True)
#fhhPD.columns
#
## Reading FinalHouseHold Affinity Data
#Affi_PD = pd.read_csv(pathread+'Household_Affinity_Result_with_bucket_v1.1.csv', low_memory = True)
#Affi_PD.columns
#
#
## Reading FinalHouseHold LifeStage Data
#ls_PD = pd.read_csv(pathread+'hh_lifeStage_result_score_broad.csv', low_memory = True)
#ls_PD.columns
#
#
#
## Cleaning of customerview Data
#path_data = "E:/NTUC/raw_data/Data_24092018/HH_customerview_latize_v2_240918/customerview_latize.csv"
#addPD = pd.read_csv(path_data, low_memory = True)
#addPD = addPD.fillna('NA')
#addPD.columns
## Renaming H.Id to hid
#addPD.columns = ['CustomerSeqID', 'CustomerStatus', 'GenderPH', 'MMOPH', 'AgePH', 'hid',
#       'CustomerType', 'CustomerValueLI', 'IndividualRelationTag',
#       'ReachScore10', 'CustomerReachConfi', 'MembersSpouse', 'MembersChild',
#       'MembersOthers', 'Tod', 'Young', 'Grad', 'Teen', 'Adult', 'PolicyCount',
#       'Decision_maker']
## Final Data set
#cview_data = addPD[['CustomerSeqID', 'CustomerStatus', 'GenderPH', 'MMOPH', 'AgePH', 'hid',
#       'CustomerType',  'IndividualRelationTag',
#       'ReachScore10', 'CustomerReachConfi', 'MembersSpouse', 'MembersChild',
#       'MembersOthers', 'Tod', 'Young', 'Grad', 'Teen', 'Adult', 'PolicyCount',
#       'Decision_maker']]
#
## Handlling NaN / Blank values with "NA"
#
#cview_data = cview_data.fillna('NA')
#
#cview_data.to_csv(pathwrite+"customerview_clean.csv", header = True, index= False)
#
#
#
## Cleaning of agent Data
#path_data = "E:/NTUC/raw_data/Data_24092018/edw_agent_v2_240918/agent.csv"
#addPD = pd.read_csv(path_data, low_memory = True)
## Handlling NaN / Blank values with "NA"
#addPD = addPD.fillna('NA')
#addPD.columns
#
## writing to csv
#addPD.to_csv(pathwrite+"agent_clean.csv", header = True, index= False)
#
#
#
## Cleaning of houseview Data
#path_data = "E:/NTUC/raw_data/Data_24092018/HH_houseview_latize_v2_240918/houseview_latize.csv"
#addPD = pd.read_csv(path_data, low_memory = True)
#addPD.columns
## Renaming H.Id to hid, GI.active to GI_active and others
#addPD.columns = ['hid', 'MembersCount', 'GI_active', 'LI_active', 'IS_active',
#       'MembersActive', 'holdingtag', 'HouseRelationConfidence',
#       'HouseRelationTag', 'HouseRelationCount', 'HouseMMOConfidence',
#       'HouseholdReachConfi', 'TodCount', 'YoungCount', 'TeenCount',
#       'GradCount', 'Toddler_Flag', 'Young_Flag', 'Teen_Flag', 'Grad_Flag',
#       'Spouse_Flag', 'totalkids', 'Total_Policies', 'Decision_maker']
## Final Data set, removed unnecessary columns
#hview_data = addPD[['hid', 'MembersCount', 'GI_active', 'LI_active', 'IS_active','MembersActive', 'HouseRelationConfidence',
#       'HouseRelationTag', 'HouseRelationCount', 'HouseMMOConfidence', 'HouseholdReachConfi', 'TodCount', 'YoungCount', 'TeenCount', 'GradCount', 'Toddler_Flag', 'Young_Flag', 'Teen_Flag', 'Grad_Flag', 'Spouse_Flag', 'totalkids', 'Total_Policies', 'Decision_maker']]
#
## Handlling NaN / Blank values with "NA"
#
#hview_data = hview_data.fillna('NA')
##Writing csv
#hview_data.to_csv(pathwrite+"houseview_clean.csv", header = True, index= False)
######################################################
#
#
## Cleaning of customer Data
#path_data = "E:/NTUC/raw_data/Data_24092018/edw_customer_v2_240918/customer.csv"
#addPD = pd.read_csv(path_data, low_memory = True)
#addPD.columns
## Final Data set, removed unnecessary columns
#customer_data = addPD[['customerseqid', 'customerstatus', 'dateofbirth', 'gender','nationality', 'race', 'educationlevel', 'maritalstatus', 'mmoemail','mmomail', 'mmophone', 'mmosms', 'staffflag', 'PostalCode', 'dwellingtype']]
#customer_data.columns
## Handlling NaN / Blank values with "NA"
#
#customer_data = customer_data.fillna('NA')
##Writing csv
#write_file(customer_data,'customer_clean')
###################################################
#
## Cleaning of edw_customerdemog_historydetails_v1_280918 Data
#path_data = "E:/NTUC/raw_data/Data_24092018/edw_customerdemog_historydetails_v1_280918/edw_customerdemog.csv"
#addPD = pd.read_csv(path_data, low_memory = True)
#addPD.columns
## Handlling NaN / Blank values with "NA"
#
#addPD = addPD.fillna('NA')
##Writing csv
#write_file(addPD,'customer_demography_history_clean')
###################################################
#
## Cleaning of edw_lapsedpolicies Data
#path_data = "E:/NTUC/raw_data/Data_24092018/edw_lapsedpolicies_v1_280918/edw_lapsedpolicies.csv"
#addPD = pd.read_csv(path_data, low_memory = True)
#addPD.columns
## Handlling NaN / Blank values with "NA"
#
#addPD = addPD.fillna('NA')
##Writing csv
#write_file(addPD,'lapsed_policy_clean')
###################################################
#
## Cleaning of product Data
#path_data = "E:/NTUC/raw_data/Data_24092018/edw_product_v2_240918/product.csv"
#addPD = pd.read_csv(path_data, low_memory = True)
#addPD.columns
## Handlling NaN / Blank values with "NA"
#
#addPD = addPD.fillna('NA')
##Writing csv
#write_file(addPD,'product_clean')
###################################################
#
## Cleaning of transaction Data
#path_data = "E:/NTUC/raw_data/Data_24092018/edw_transaction_v2_240918/transaction.csv"
#addPD = pd.read_csv(path_data, low_memory = True)
#addPD.columns
## data cleansing
#addPD.maindriveroccupation.unique()
#
#addPD['maindriveroccupation'] = addPD.maindriveroccupation.replace('BUSINESSMAN-OUTDOOR', 'BUSINESSMAN-OUTDOOR')
#addPD.columns
#addPD.maindriveroccupation.unique()
#
#
## Handlling NaN / Blank values with "NA"
#
#addPD = addPD.fillna('NA')
##Writing csv
#write_file(addPD,'transaction_clean')
###################################################
#
## Cleaning of edw_travelpolicy Data
#path_data = "E:/NTUC/raw_data/Data_24092018/edw_travelpolicy_v1_280918/edw_travelpolicy.csv"
#addPD = pd.read_csv(path_data, low_memory = True)
#addPD.columns
## Handlling NaN / Blank values with "NA"
#
#addPD = addPD.fillna('NA')
##Writing csv
#write_file(addPD,'travel_policy_clean')
###################################################
#
## Cleaning of relation_latize Data
#path_data = "E:/NTUC/raw_data/Data_24092018/HH_relation_latize_v2_240918/relation_latize.csv"
#addPD = pd.read_csv(path_data, low_memory = True)
#addPD.columns
##Column name Cleansing
#addPD.columns = ['customerIdnumber_1', 'Relation', 'Add_R', 'RelationConfidence',
#       'customerIdnumber_2', 'type', 'PHIS_R', 'email_R', 'Namematch', 'hid']
#
## Handlling NaN / Blank values with "NA"
#
#addPD = addPD.fillna('NA')
##Writing csv
#write_file(addPD,'house_relation_clean')
###############################################################
#
########## Joining / Merging data ##################
#
##def readfl(filename):
##    addPD = pd.read_csv(path_merge+filename+".csv", low_memory = True)
##    addPD.columns
#
## define path for reading
#path_merge = "E:/NTUC/raw_data/clean_raw_data/"
#
## Merging customerview and houseview
#cview = pd.read_csv(path_merge+'customerview_clean.csv', low_memory = True)
#cview.columns
#hview = pd.read_csv(path_merge+'houseview_clean.csv', low_memory = True)
#hview.columns
#
#mergePD = cview.merge(hview, on='hid', how ='left')
#mergePD = mergePD.fillna('NA')
#mergePD.columns
#mergePD.columns = ['CustomerSeqID', 'CustomerStatus', 'GenderPH', 'MMOPH', 'AgePH', 'hid','CustomerType', 'IndividualRelationTag', 'ReachScore10','CustomerReachConfi', 'MembersSpouse', 'MembersChild', 'MembersOthers','Tod', 'Young', 'Grad', 'Teen', 'Adult', 'PolicyCount','Decision_maker_customerview', 'MembersCount', 'GI_active', 'LI_active', 'IS_active', 'MembersActive', 'HouseRelationConfidence','HouseRelationTag', 'HouseRelationCount', 'HouseMMOConfidence','HouseholdReachConfi', 'TodCount', 'YoungCount', 'TeenCount','GradCount', 'Toddler_Flag', 'Young_Flag', 'Teen_Flag', 'Grad_Flag','Spouse_Flag', 'totalkids', 'Total_Policies', 'Decision_maker_household']
#len(mergePD)
#mergePD = mergePD.drop_duplicates(subset=None, keep='first', inplace=False)
#len(mergePD)
##writing csv file
#write_file(mergePD,'customerview_houseview_merge')
##############################################################
#
#
###Creating unique customerseqid and householdid together for further merging
#
#uniqueIds =  mergePD[['CustomerSeqID', 'hid']]
#uniqueIds.columns = ['customerseqid', 'hid']
#uniqueIds = uniqueIds.fillna('NA')
#uniqueIds = uniqueIds.drop_duplicates(subset=None, keep='first', inplace=False)
#len(uniqueIds)
#len(uniqueIds.hid.unique())
#
## writing csv file
#write_file(uniqueIds,'uniqueIds_merge')
#################################################################
#
## Merging uniqueids_merge and transaction
#cview = pd.read_csv(path_merge+'transaction_clean.csv', low_memory = True)
#cview.columns
#hview = pd.read_csv(path_merge+'uniqueIds_merge.csv', low_memory = True)
#hview.columns
#
#mergePD = hview.merge(cview, on='customerseqid', how ='left')
#mergePD = mergePD.fillna('NA')
#mergePD.columns
#len(mergePD)
#mergePD = mergePD.drop_duplicates(subset=None, keep='first', inplace=False)
#len(mergePD)
##writing csv file
#write_file(mergePD,'uniqueIds_transaction_merge')
#
#################################################################
#
## Merging uniqueids_merge and customer
#cview = pd.read_csv(path_merge+'customer_clean.csv', low_memory = True)
#cview.columns
#hview = pd.read_csv(path_merge+'uniqueIds_merge.csv', low_memory = True)
#hview.columns
#
#mergePD = hview.merge(cview, on='customerseqid', how ='left')
#mergePD = mergePD.fillna('NA')
#mergePD.columns
#len(mergePD)
#mergePD = mergePD.drop_duplicates(subset=None, keep='first', inplace=False)
#len(mergePD)
##writing csv file
#write_file(mergePD,'uniqueIds_customer_merge')
##################################################################
#
## Clean product Data
#cview = pd.read_csv(path_merge+'product_clean.csv', low_memory = True)
#cview = cview[['productseqid', 'productname', 'productline', 'productcategory',
#       'productsubcategory', 'ismain', 'governmentschemeintegrated']]
#cview.columns
#cview = cview.drop_duplicates(subset=None, keep='first', inplace=False)
#len(cview)
##writing csv file
#write_file(cview,'clean_product_tobe_used')
#################################################################
#
## Generating uniqueids+transaction and prodcutmerge
#cview = pd.read_csv(path_merge+'uniqueIds_transaction_merge.csv', low_memory = True)
#cview.columns
#cview = cview[['customerseqid', 'hid', 'policyseqid','productseqid']]
#hview = pd.read_csv(path_merge+'clean_product_tobe_used.csv', low_memory = True)
#hview.columns
#
#mergePD = cview.merge(hview, on='productseqid', how ='left')
#mergePD = mergePD.fillna('NA')
#mergePD.columns
#len(mergePD)
#mergePD = mergePD.drop_duplicates(subset=None, keep='first', inplace=False)
#len(mergePD)
##writing csv file
#write_file(mergePD,'uniqueIds_productInfo_merge')
#
##################################################################
##### merging uniqueIds and travelPolicy Data
#cview = cview[['customerseqid', 'hid', 'policyseqid']]
#hview = pd.read_csv(path_merge+'travel_policy_clean.csv', low_memory = True)
#hview.columns
#
#mergePD = cview.merge(hview, on='policyseqid', how ='left')
#mergePD = mergePD.fillna('NA')
#mergePD.columns
#len(mergePD)
#mergePD = mergePD.drop_duplicates(subset=None, keep='first', inplace=False)
#len(mergePD)
##writing csv file
#write_file(mergePD,'uniqueIds_travelInfo_merge')
###########################################################
#
##### merging uniqueIds and affluence bucket data
#cview = pd.read_csv(path_merge+'uniqueIds_merge.csv', low_memory = True)
#hview = pd.read_csv(path_merge+'hh_Affluence_final_Result.csv', low_memory = True)
#hview.columns
#
#mergePD = cview.merge(hview, on='hid', how ='left')
#mergePD = mergePD.fillna('NA')
#mergePD.columns
#len(mergePD)
#mergePD = mergePD.drop_duplicates(subset=None, keep='first', inplace=False)
#len(mergePD)
##writing csv file
#write_file(mergePD,'affluence_HH_Info_uniqueIds_merge')
#
#################################################################
#
##### merging uniqueIds and addresstype_clean data
#cview = pd.read_csv(path_merge+'uniqueIds_merge.csv', low_memory = True)
#hview = pd.read_csv(path_merge+'addresstype_clean.csv', low_memory = True)
#hview.columns
#
#mergePD = cview.merge(hview, on='customerseqid', how ='left')
#mergePD = mergePD.fillna('NA')
#mergePD.columns
#len(mergePD)
#mergePD = mergePD.drop_duplicates(subset=None, keep='first', inplace=False)
#len(mergePD)
##writing csv file
#write_file(mergePD,'uniqueIds_AddressType_merge')
#
#
#
#
#
#
#

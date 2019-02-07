# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 16:31:12 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np
pathwrite =  "E:/NTUC/raw_data/clean_raw_data/Final_recom_data/"

def write_file(pd_name, filename):
    pathwrite =  "E:/NTUC/raw_data/clean_raw_data/Final_recom_data/"
    pd_name.to_csv(pathwrite+filename+".csv", header = True, index = False)


# Cleaning of AddressType Data
path_data = "E:/NTUC/raw_data/Data_24092018/edw_addresstypedetails.csv"
addPD = pd.read_csv(path_data, low_memory = True)
addPD.columns
addPD.addr_type_desc.unique()
# data cleansing
addPD['addr_type_desc'] = addPD.addr_type_desc.replace('PO Box', 'NA')
addPD.columns
addPD.addr_type_desc.unique()
dwell = addPD[['customerseqid','addr_type_desc']]
dwell = dwell.fillna('NA')

dwell.to_csv(pathwrite+"addresstype_clean.csv", header = True, index= False)

# Cleaning of customerview Data
path_data = "E:/NTUC/raw_data/Data_24092018/HH_customerview_latize_v2_240918/customerview_latize.csv"
addPD = pd.read_csv(path_data, low_memory = True)
addPD = addPD.fillna('NA')
addPD.columns
# Renaming H.Id to hid
addPD.columns = ['CustomerSeqID', 'CustomerStatus', 'GenderPH', 'MMOPH', 'AgePH', 'hid',
       'CustomerType', 'CustomerValueLI', 'IndividualRelationTag',
       'ReachScore10', 'CustomerReachConfi', 'MembersSpouse', 'MembersChild',
       'MembersOthers', 'Tod', 'Young', 'Grad', 'Teen', 'Adult', 'PolicyCount',
       'Decision_maker']
# Final Data set
cview_data = addPD[['CustomerSeqID', 'CustomerStatus', 'GenderPH', 'MMOPH', 'AgePH', 'hid',
       'CustomerType',  'IndividualRelationTag','ReachScore10', 'CustomerReachConfi', 'MembersSpouse', 'MembersChild','MembersOthers', 'Tod', 'Young', 'Grad', 'Teen', 'Adult', 'PolicyCount', 'Decision_maker']]

# Handlling NaN / Blank values with "NA"

cview_data = cview_data.fillna('NA')
cview_data = cview_data.drop_duplicates(subset=None, keep='first', inplace=False)
cview_data.to_csv(pathwrite+"customerview_clean.csv", header = True, index= False)



# Cleaning of agent Data
path_data = "E:/NTUC/raw_data/Data_24092018/edw_agent_v2_240918/agent.csv"
addPD = pd.read_csv(path_data, low_memory = True)
# Handlling NaN / Blank values with "NA"
addPD = addPD.fillna('NA')
addPD.columns

# writing to csv
addPD.to_csv(pathwrite+"agent_clean.csv", header = True, index= False)



# Cleaning of houseview Data
path_data = "E:/NTUC/raw_data/Data_24092018/HH_houseview_latize_v2_240918/houseview_latize.csv"
addPD = pd.read_csv(path_data, low_memory = True)
addPD.columns
# Renaming H.Id to hid, GI.active to GI_active and others
addPD.columns = ['hid', 'MembersCount', 'GI_active', 'LI_active', 'IS_active',
       'MembersActive', 'holdingtag', 'HouseRelationConfidence',
       'HouseRelationTag', 'HouseRelationCount', 'HouseMMOConfidence',
       'HouseholdReachConfi', 'TodCount', 'YoungCount', 'TeenCount',
       'GradCount', 'Toddler_Flag', 'Young_Flag', 'Teen_Flag', 'Grad_Flag',
       'Spouse_Flag', 'totalkids', 'Total_Policies', 'Decision_maker']
# Final Data set, removed unnecessary columns
hview_data = addPD[['hid', 'MembersCount', 'GI_active', 'LI_active', 'IS_active','MembersActive', 'HouseRelationConfidence',
       'HouseRelationTag', 'HouseRelationCount', 'HouseMMOConfidence', 'HouseholdReachConfi', 'TodCount', 'YoungCount', 'TeenCount', 'GradCount', 'Toddler_Flag', 'Young_Flag', 'Teen_Flag', 'Grad_Flag', 'Spouse_Flag', 'totalkids', 'Total_Policies', 'Decision_maker']]

# Handlling NaN / Blank values with "NA"

hview_data = hview_data.fillna('NA')
hview_data = hview_data.drop_duplicates(subset=None, keep='first', inplace=False)
#Writing csv
hview_data.to_csv(pathwrite+"houseview_clean.csv", header = True, index= False)
#####################################################


# Cleaning of customer Data
path_data = "E:/NTUC/raw_data/Data_24092018/edw_customer_v2_240918/customer.csv"
addPD = pd.read_csv(path_data, low_memory = True)
addPD.columns
# Final Data set, removed unnecessary columns
customer_data = addPD[['customerseqid', 'customerstatus', 'dateofbirth', 'gender','nationality', 'race', 'educationlevel', 'maritalstatus', 'mmoemail','mmomail', 'mmophone', 'mmosms', 'staffflag', 'PostalCode', 'dwellingtype']]
customer_data.columns
# Handlling NaN / Blank values with "NA"

customer_data = customer_data.fillna('NA')
customer_data = customer_data.drop_duplicates(subset=None, keep='first', inplace=False)
#Writing csv
write_file(customer_data,'customer_clean')
##################################################

# Cleaning of edw_customerdemog_historydetails_v1_280918 Data
path_data = "E:/NTUC/raw_data/Data_24092018/edw_customerdemog_historydetails_v1_280918/edw_customerdemog.csv"
addPD = pd.read_csv(path_data, low_memory = True)
addPD.columns
# Handlling NaN / Blank values with "NA"

addPD = addPD.fillna('NA')
#Writing csv
write_file(addPD,'customer_demography_history_clean')
##################################################

# Cleaning of edw_lapsedpolicies Data
path_data = "E:/NTUC/raw_data/Data_24092018/edw_lapsedpolicies_v1_280918/edw_lapsedpolicies.csv"
addPD = pd.read_csv(path_data, low_memory = True)
addPD.columns
# Handlling NaN / Blank values with "NA"

addPD = addPD.fillna('NA')
#Writing csv
write_file(addPD,'lapsed_policy_clean')
##################################################

# Cleaning of product Data
path_data = "E:/NTUC/raw_data/Data_24092018/edw_product_v2_240918/product.csv"
addPD = pd.read_csv(path_data, low_memory = True)
addPD.columns
# Handlling NaN / Blank values with "NA"

addPD = addPD.fillna('NA')
#Writing csv
write_file(addPD,'product_clean')
##################################################

# Cleaning of transaction Data
path_data = "E:/NTUC/raw_data/Data_24092018/edw_transaction_v2_240918/transaction.csv"
addPD = pd.read_csv(path_data, low_memory = True)
addPD.columns
#addPD = addPD[['policyseqid', 'PolicyStartDate',
#       'PolicyEndDate']]
#addPD.to_csv(pathread+'policydate.csv', header = True, index = False)
# data cleansing
addPD.maindriveroccupation.unique()

addPD['maindriveroccupation'] = addPD.maindriveroccupation.replace('BUSINESSMAN-OUTDOOR', 'BUSINESSMAN-OUTDOOR')
addPD.columns
addPD.maindriveroccupation.unique()


# Handlling NaN / Blank values with "NA"

addPD = addPD.fillna('NA')
addPD = addPD.drop_duplicates(subset=None, keep='first', inplace=False)
#Writing csv
write_file(addPD,'transaction_clean')
##################################################

# Cleaning of edw_travelpolicy Data
path_data = "E:/NTUC/raw_data/Data_24092018/edw_travelpolicy_v1_280918/edw_travelpolicy.csv"
addPD = pd.read_csv(path_data, low_memory = True)
addPD.columns
# Handlling NaN / Blank values with "NA"

addPD = addPD.fillna('NA')
#Writing csv
write_file(addPD,'travel_policy_clean')
##################################################

# Cleaning of relation_latize Data
path_data = "E:/NTUC/raw_data/Data_24092018/HH_relation_latize_v2_240918/relation_latize.csv"
addPD = pd.read_csv(path_data, low_memory = True)
addPD.columns
#Column name Cleansing
addPD.columns = ['customerIdnumber_1', 'Relation', 'Add_R', 'RelationConfidence',
       'customerIdnumber_2', 'type', 'PHIS_R', 'email_R', 'Namematch', 'hid']

# Handlling NaN / Blank values with "NA"

addPD = addPD.fillna('NA')
#Writing csv
write_file(addPD,'house_relation_clean')
##############################################################

######### Joining / Merging data ##################

#def readfl(filename):
#    addPD = pd.read_csv(path_merge+filename+".csv", low_memory = True)
#    addPD.columns

# define path for reading
path_merge = "E:/NTUC/raw_data/clean_raw_data/Final_recom_data/"

# Merging customerview and houseview
cview = pd.read_csv(path_merge+'customerview_clean.csv', low_memory = True)
cview.columns
hview = pd.read_csv(path_merge+'houseview_clean.csv', low_memory = True)
hview.columns

mergePD = cview.merge(hview, on='hid', how ='left')
mergePD = mergePD.fillna('NA')
mergePD.columns
mergePD.columns = ['CustomerSeqID', 'CustomerStatus', 'GenderPH', 'MMOPH', 'AgePH', 'hid','CustomerType', 'IndividualRelationTag', 'ReachScore10','CustomerReachConfi', 'MembersSpouse', 'MembersChild', 'MembersOthers','Tod', 'Young', 'Grad', 'Teen', 'Adult', 'PolicyCount','Decision_maker_customerview', 'MembersCount', 'GI_active', 'LI_active', 'IS_active', 'MembersActive', 'HouseRelationConfidence','HouseRelationTag', 'HouseRelationCount', 'HouseMMOConfidence','HouseholdReachConfi', 'TodCount', 'YoungCount', 'TeenCount','GradCount', 'Toddler_Flag', 'Young_Flag', 'Teen_Flag', 'Grad_Flag','Spouse_Flag', 'totalkids', 'Total_Policies', 'Decision_maker_household']
len(mergePD)
mergePD = mergePD.drop_duplicates(subset=None, keep='first', inplace=False)
len(mergePD)
#writing csv file
write_file(mergePD,'customerview_houseview_merge')
#############################################################


##Creating unique customerseqid and householdid together for further merging

uniqueIds =  mergePD[['CustomerSeqID', 'hid']]
uniqueIds.columns = ['customerseqid', 'hid']
uniqueIds = uniqueIds.fillna('NA')
uniqueIds = uniqueIds.drop_duplicates(subset=None, keep='first', inplace=False)
len(uniqueIds)
len(uniqueIds.hid.unique())

# writing csv file
write_file(uniqueIds,'uniqueHid_CustomerIds_merge')
################################################################

# Merging uniqueids_merge and transaction
cview = pd.read_csv(path_merge+'transaction_clean.csv', low_memory = True)
cview.columns
hview = pd.read_csv(path_merge+'uniqueHid_CustomerIds_merge.csv', low_memory = True)
hview.columns

mergePD = hview.merge(cview, on='customerseqid', how ='left')
mergePD = mergePD.fillna('NA')
mergePD.columns
len(mergePD)
mergePD = mergePD.drop_duplicates(subset=None, keep='first', inplace=False)
len(mergePD)
#writing csv file
write_file(mergePD,'uniqueIds_transaction_merge')

################################################################

# Merging uniqueids_merge and customer
cview = pd.read_csv(path_merge+'customer_clean.csv', low_memory = True)
cview.columns
hview = pd.read_csv(path_merge+'uniqueHid_CustomerIds_merge.csv', low_memory = True)
hview.columns

mergePD = hview.merge(cview, on='customerseqid', how ='left')
mergePD = mergePD.fillna('NA')
mergePD.columns
len(mergePD)
mergePD = mergePD.drop_duplicates(subset=None, keep='first', inplace=False)
len(mergePD)
#writing csv file
write_file(mergePD,'uniqueIds_customer_merge')
#################################################################

# Clean product Data
cview = pd.read_csv(path_merge+'product_clean.csv', low_memory = True)
cview = cview[['productseqid', 'productname', 'productline', 'productcategory',
       'productsubcategory', 'ismain', 'governmentschemeintegrated']]
cview.columns
cview = cview.drop_duplicates(subset=None, keep='first', inplace=False)
len(cview)
#writing csv file
write_file(cview,'product_clean_tobe_used')
################################################################

# Generating uniqueids+transaction and prodcutmerge
cview = pd.read_csv(path_merge+'uniqueIds_transaction_merge.csv', low_memory = True)
cview.columns
cview = cview[['customerseqid', 'hid', 'policyseqid','productseqid']]
hview = pd.read_csv(path_merge+'product_clean_tobe_used.csv', low_memory = True)
hview.columns

mergePD = cview.merge(hview, on='productseqid', how ='left')
mergePD = mergePD.fillna('NA')
mergePD.columns
len(mergePD)
mergePD = mergePD.drop_duplicates(subset=None, keep='first', inplace=False)
len(mergePD)
#writing csv file
write_file(mergePD,'uniqueIds_productInfo_merge')

#################################################################
#### merging uniqueIds and travelPolicy Data
cview = cview[['customerseqid', 'hid', 'policyseqid']]
hview = pd.read_csv(path_merge+'travel_policy_clean.csv', low_memory = True)
hview.columns

mergePD = cview.merge(hview, on='policyseqid', how ='left')
mergePD = mergePD.fillna('NA')
mergePD.columns
len(mergePD)
mergePD = mergePD.drop_duplicates(subset=None, keep='first', inplace=False)
len(mergePD)
#writing csv file
write_file(mergePD,'uniqueIds_travelInfo_merge')
##########################################################

#### merging uniqueIds and affluence bucket data
cview = pd.read_csv(path_merge+'uniqueIds_merge.csv', low_memory = True)
hview = pd.read_csv(path_merge+'hh_Affluence_final_Result.csv', low_memory = True)
hview.columns

mergePD = cview.merge(hview, on='hid', how ='left')
mergePD = mergePD.fillna('NA')
mergePD.columns
len(mergePD)
mergePD = mergePD.drop_duplicates(subset=None, keep='first', inplace=False)
len(mergePD)
#writing csv file
write_file(mergePD,'affluence_HH_Info_uniqueIds_merge')

################################################################

#### merging uniqueIds and addresstype_clean data
cview = pd.read_csv(path_merge+'uniqueIds_merge.csv', low_memory = True)
hview = pd.read_csv(path_merge+'addresstype_clean.csv', low_memory = True)
hview.columns

mergePD = cview.merge(hview, on='customerseqid', how ='left')
mergePD = mergePD.fillna('NA')
mergePD.columns
len(mergePD)
mergePD = mergePD.drop_duplicates(subset=None, keep='first', inplace=False)
len(mergePD)
#writing csv file
write_file(mergePD,'uniqueIds_AddressType_merge')








# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 14:50:28 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np

pathwrite =  "E:/NTUC/raw_data/clean_raw_data/Final_recom_data/"
path_merge =  "E:/NTUC/raw_data/clean_raw_data/Final_recom_data/"

def write_file(pd_name, filename):
    pathwrite =  "E:/NTUC/raw_data/clean_raw_data/Final_recom_data/"
    pd_name.to_csv(pathwrite+filename+".csv", header = True, index = False)


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
mergePD.head()
mergePD.productline.unique()  # output: array(['NA', 'GH', 'LI', 'GI'], dtype=object)
mergePD.productcategory.unique()  # output:  array(['NA', 'IS', 'TRADITIONAL', 'ELS', 'PLINE', 'PARTICIPATING',
                               # 'MOTOR', 'CLINE', 'DPS', 'NEW UL PRODUCT', 'UNIT LINKED', 'MHS','MCS'], dtype=object)

mergePD.productsubcategory.unique() # output:  array(['NA', 'INCOMESHIELD MEDISAVE', 'SCHEME', 'ELS', 'FIRE',
                         # 'INCOMESHIELD ENHANCED', 'INCOMESHIELD STANDARD', 'PERSONAL ACCIDENT', 'ENDOWMENT', 'MOTOR', 'GROUP', 'TRAVEL', 'TERM', 'LIABILITY', 'BOND', 'DPS', 'WHOLE LIFE', 'PROPERTY', 'ANNUITY', 'PACKAGE', 'MISCELLANEOUS', 'MARINE', 'ENGINEERING', 'HEALTH', 'MHS', 'INDIVIDUAL', 'MCS'], dtype=object)

productDF = pd.read_csv("E:/NTUC/working/ProductClassification MetadataLatize_processed.csv", low_memory = True)
productDF.columns
productDF =productDF[['Product Code', 'productname', 'PremiumType','productcategory']]
prodmerge = mergePD.merge(productDF, on = 'productname', how = 'left' )
prodmerge.columns
len(prodmerge)
prodmerge.productcategory_x.unique()
prodmerge.productcategory_y.unique()
abc = prodmerge.productname.unique().tolist()
uniq_prod_list = pd.DataFrame(abc)
uniq_prod_list.to_csv(path_merge+"unique_Product_list.csv", header = True, index = False)


# updating product category
prodmerge = prodmerge[['customerseqid', 'hid', 'policyseqid', 'productseqid', 'productname',
       'productline', 'productsubcategory', 'ismain',
       'governmentschemeintegrated', 'Product Code', 'PremiumType']]

uniquePrdtDF = pd.read_csv(path_merge+"unique_Product_list.csv", low_memory = True)
uniquePrdtDF.columns
prodmerge = prodmerge.merge(uniquePrdtDF, on = 'productname', how = 'left' )
prodmerge.columns
prodmerge.Category_list.unique()
prodmerge.Category_data.unique()
prodmerge.productline.unique() # 'NA', 'Health', 'LI', 'GH', 'GI'
len(prodmerge)
len(prodmerge.hid.unique())
prodmerge = prodmerge[prodmerge.productline != 'GI' ]
prodmerge = prodmerge[prodmerge.productline != 'GH' ]
len(prodmerge)
len(prodmerge.policyseqid.unique())
len(prodmerge.hid.unique())
finalList = prodmerge[['hid','customerseqid', 'policyseqid', 'Product Code', 'PremiumType',
       'Category_list', 'Category_data']]
finalList.to_csv(path_merge+"final_Product_list.csv", header = True, index = False)

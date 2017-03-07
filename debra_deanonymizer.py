# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 14:28:23 2016

@author: Vidyut
"""

import numpy as np
import pandas as pd
import time
import datetime
import os

start = []
start.append(datetime.datetime.now().time())

# set the working directory
path = "D:/training/TWG_overall/data_harmonisation/JPN/twg_ag/trial/"

os.chdir(path)
fls=os.listdir(path)


# set the number of decimal places to see in DFs
pd.set_eng_float_format(accuracy=15, use_eng_prefix=True)

debCol = ['country', 'company', 'businesstype', 'client', 'clientnum', 'clientlevel2', 'clientlevel3', 'clientlevel4', 'sellingdealer', 'sellingdealerstate', 'sellingdealerpostalcode', 'customerstate', 'customerpostalcode', 'contractnum', 'contractseqnum', 'contractstatus', 'contractpurchasedate', 'contractpurchaseyear', 'contractpurchasemonth', 'contractliabbegindate', 'contractliabbeginyear', 'contractliabbeginmonth', 'contractliabenddate', 'contractliabendyear', 'contractliabendmonth', 'contractcanceldate', 'contractcancelyear', 'contractcancelmonth', 'productpurchasedate', 'productpurchaseyear', 'productpurchasemonth', 'productdeliveryorinservicedate', 'productdeliveryorinserviceyear', 'productdeliveryorinservicemonth', 'contracttermbegindate', 'contracttermbeginyear', 'contracttermbeginmonth', 'contractterm_labormonths', 'contractterm_partsmonths', 'contractterm_odo', 'contracttermmeasure_odo', 'contractterm_expiremethod', 'elimperiodmonths', 'modelcode', 'modeldesc', 'modeldesc_native', 'vehicleclass', 'modelcollection', 'modelcollection_native', 'modelsection', 'modelsection_native', 'modelclass', 'modelclass_native', 'modelyear', 'vehiclecylinders', 'vehiclefueltype', 'vinorserialnumber', 'mfrname', 'mfrname_native', 'mfrname_make', 'mfrterm_odo', 'mfrterm_labormonths', 'mfrterm_partsmonths', 'mfrterm_majorcompmonths', 'sku', 'clientsku', 'skubegindate', 'skuenddate', 'skudesc', 'skudesc_native', 'programid', 'programiddesc', 'programiddesc_native', 'pricetiermin', 'pricetiermax', 'priceratingmethod', 'newused', 'refurbflag', 'vehicleodo', 'deductibleamt', 'deductibletype', 'deductibledesc', 'reducingdeductamtfrom', 'reducingdeductamtto', 'coveragecategory', 'coveragetype', 'servicelocation', 'skucollection', 'skucollection_native', 'skusection', 'skusection_native', 'skuclass', 'skuclass_native', 'vehicleodolevel_min', 'vehicleodolevel_max', 'modelage_min', 'modelage_max', 'obligor', 'contractenteryrmo', 'productpurchaseprice', 'contractpurchaseprice', 'reservefund_written', 'adminfee_written', 'mktfee_written', 'dlrcostnotax_written', 'dlrcostwithtax_written', 'reservefund_refund', 'adminfee_refund', 'mktfee_refund', 'dlrcostnotax_refund', 'dlrcostwithtax_refund', 'reservefund_net', 'adminfee_net', 'mktfee_net', 'dlrcostnotax_net', 'dlrcostwithtax_net', 'reservefund_earned', 'adminfee_earned', 'mktfee_earned', 'premium_written', 'premium_refund', 'premium_net', 'premium_earned', 'fees_written', 'fees_refund', 'fees_net', 'fees_earned', 'cancelfee', 'contractcnt_earned', 'contractcnt_written', 'contractcnt_written_xflat', 'contractcnt_net', 'contractcnt_net_xcancels', 'claimcnt_paid', 'claimamt_paid', 'claimamtnotax_paid', 'claimcnt_pend', 'claimamt_pend', 'claimamtnotax_pend']

debTable = ['COUNTRY', 'CONTRACT_DETAIL', 'BUSINESS_TYPE', 'CLIENT', 'CLIENT', 'CLIENT', 'CLIENT', 'CLIENT', 'CLIENT', 'CLIENT', 'CLIENT', 'CUSTOMER', 'CUSTOMER', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'TERM_CODE', 'TERM_CODE', 'PRODUCT_EXPIRE_METHOD', 'PRODUCT_COVERAGE', 'CONTRACT_DETAIL', 'MODEL', 'MODEL', 'MR_CLASS', 'PRODUCT_CLASS_COLLECTION', 'PRODUCT_CLASS_COLLECTION', 'PRODUCT_CLASS_SECTION', 'PRODUCT_CLASS_SECTION', 'PRODUCT_CLASS', 'PRODUCT_CLASS', 'CONTRACT_DETAIL_MR', 'MODEL', 'FUEL_TYPE', 'CONTRACT_DETAIL', 'MFG', 'MFG', 'MFG', 'FACTORY_WARRANTY_DETAIL', 'FACTORY_WARRANTY_DETAIL', 'FACTORY_WARRANTY_DETAIL', 'FACTORY_WARRANTY_DETAIL', 'CONTRACT_DETAIL', 'SKU', 'SKU', 'SKU', 'SKU', 'SKU', 'PRODUCT', 'PRODUCT', 'PRODUCT', 'PRODUCT', 'PRODUCT', 'PRICE_RATING_METHOD', 'NEW_USED_TYPE', 'PRODUCT', 'CONTRACT_DETAIL_MR', 'DEDUCTIBLE_CODE', 'DEDUCTIBLE_TYPE', 'DEDUCTIBLE_CODE', 'DEDUCTIBLE_CODE', 'DEDUCTIBLE_CODE', 'COMPONENT', 'COVERAGE_TYPE', 'SERVICE_LOCATION', 'PRODUCT_CLASS_COLLECTION', 'PRODUCT_CLASS_COLLECTION', 'PRODUCT_CLASS_SECTION', 'PRODUCT_CLASS_SECTION', 'PRODUCT_CLASS', 'PRODUCT_CLASS', 'RATE', 'RATE', 'RATE', 'RATE', 'WRITING_COMPANY', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'CONTRACT_DETAIL', 'ACCOUNTING_TRANSACTION', 'ACCOUNTING_TRANSACTION', 'ACCOUNTING_TRANSACTION', 'ACCOUNTING_TRANSACTION', 'ACCOUNTING_TRANSACTION', 'ACCOUNTING_TRANSACTION', 'ACCOUNTING_TRANSACTION', 'CDE_EXTRACT', 'ACCOUNTING_TRANSACTION', 'ACCOUNTING_TRANSACTION', 'CDE_EXTRACT', 'CDE_EXTRACT', 'CDE_EXTRACT', 'ACCOUNTING_TRANSACTION', 'ACCOUNTING_TRANSACTION', 'CDE_EXTRACT', 'CDE_EXTRACT', 'CDE_EXTRACT', 'CDE_EXTRACT', 'CDE_EXTRACT', 'CDE_EXTRACT', 'CDE_EXTRACT', 'CDE_EXTRACT', 'CDE_EXTRACT', 'CDE_EXTRACT', 'CDE_EXTRACT', 'ACCOUNTING_TRANSACTION', 'check', 'check', 'check', 'check', 'check', 'check', 'check', 'check', 'check', 'check', 'check']

len(np.unique(debTable))

reference = [xi+"_pii.csv" for xi in np.unique(debTable)]
debTableReference = []

for dt in range(len(debTable)):
    for dr in reference:
        if (debTable[dt].lower().strip()==dr[:-8].lower().strip()):
            print dt
            debTableReference.append(dr)

for fil in fls:
    name = fil[-9:-4] 
    if name=="_anon":
        finPd = pd.DataFrame()    
        anonPd = pd.read_csv(fil, header=0, low_memory=False)
        fil_name = fil[:-9]
        
        check = fil_name+"_pii"
        for x in fls:
            if check in x:
                piiPd = pd.read_csv(x, header=0, low_memory=False)
                finPd = anonPd.copy()
                for op in finPd.columns:
                    if 'checksum' in op:
                        csLocation = op
                        break;
                finPd = pd.merge(left=finPd, right=piiPd, on=csLocation, how="left", indicator=True)
                finPd.to_csv(fil_name+"_final.csv",sep=',', index=False)
        #po=[]
        #for i in finPd.columns:
        #    po.append(i.lower())
        #    eo=[]
        #    for i in po:
        #        for x in debCol:
        #            if i in x:
        #                eo.append(i)
        #                break;
        #print eo


for mi in range(len(debCol)):
    chk=0
    for iy in anonPd.columns:
        if debCol[mi] in iy.lower().strip():
            chk=1
            break
    if chk==1:
        print debCol[mi], mi
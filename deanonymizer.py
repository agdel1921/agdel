# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 09:50:52 2016

@author: Vidyut
"""

import pandas as pd
import time
import datetime
import os

start = []
start.append(datetime.datetime.now().time())

# set the working directory
path = "D:/training/randomProg/cryptoAnon/"

os.chdir(path)
fls=os.listdir(path)


# set the number of decimal places to see in DFs
pd.set_eng_float_format(accuracy=15, use_eng_prefix=True)

debCol = ['country', 'company', 'businesstype', 'client', 'clientnum', 'clientlevel2', 'clientlevel3', 'clientlevel4', 'sellingdealer', 'sellingdealerstate', 'sellingdealerpostalcode', 'customerstate', 'customerpostalcode', 'contractnum', 'contractseqnum', 'contractstatus', 'contractpurchasedate', 'contractpurchaseyear', 'contractpurchasemonth', 'contractliabbegindate', 'contractliabbeginyear', 'contractliabbeginmonth', 'contractliabenddate', 'contractliabendyear', 'contractliabendmonth', 'contractcanceldate', 'contractcancelyear', 'contractcancelmonth', 'productpurchasedate', 'productpurchaseyear', 'productpurchasemonth', 'productdeliveryorinservicedate', 'productdeliveryorinserviceyear', 'productdeliveryorinservicemonth', 'contracttermbegindate', 'contracttermbeginyear', 'contracttermbeginmonth', 'contractterm_labormonths', 'contractterm_partsmonths', 'contractterm_odo', 'contracttermmeasure_odo', 'contractterm_expiremethod', 'elimperiodmonths', 'modelcode', 'modeldesc', 'modeldesc_native', 'vehicleclass', 'modelcollection', 'modelcollection_native', 'modelsection', 'modelsection_native', 'modelclass', 'modelclass_native', 'modelyear', 'vehiclecylinders', 'vehiclefueltype', 'vinorserialnumber', 'mfrname', 'mfrname_native', 'mfrname_make', 'mfrterm_odo', 'mfrterm_labormonths', 'mfrterm_partsmonths', 'mfrterm_majorcompmonths', 'sku', 'clientsku', 'skubegindate', 'skuenddate', 'skudesc', 'skudesc_native', 'programid', 'programiddesc', 'programiddesc_native', 'pricetiermin', 'pricetiermax', 'priceratingmethod', 'newused', 'refurbflag', 'vehicleodo', 'deductibleamt', 'deductibletype', 'deductibledesc', 'reducingdeductamtfrom', 'reducingdeductamtto', 'coveragecategory', 'coveragetype', 'servicelocation', 'skucollection', 'skucollection_native', 'skusection', 'skusection_native', 'skuclass', 'skuclass_native', 'vehicleodolevel_min', 'vehicleodolevel_max', 'modelage_min', 'modelage_max', 'obligor', 'contractenteryrmo', 'productpurchaseprice', 'contractpurchaseprice', 'reservefund_written', 'adminfee_written', 'mktfee_written', 'dlrcostnotax_written', 'dlrcostwithtax_written', 'reservefund_refund', 'adminfee_refund', 'mktfee_refund', 'dlrcostnotax_refund', 'dlrcostwithtax_refund', 'reservefund_net', 'adminfee_net', 'mktfee_net', 'dlrcostnotax_net', 'dlrcostwithtax_net', 'reservefund_earned', 'adminfee_earned', 'mktfee_earned', 'premium_written', 'premium_refund', 'premium_net', 'premium_earned', 'fees_written', 'fees_refund', 'fees_net', 'fees_earned', 'cancelfee', 'contractcnt_earned', 'contractcnt_written', 'contractcnt_written_xflat', 'contractcnt_net', 'contractcnt_net_xcancels', 'claimcnt_paid', 'claimamt_paid', 'claimamtnotax_paid', 'claimcnt_pend', 'claimamt_pend', 'claimamtnotax_pend']


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
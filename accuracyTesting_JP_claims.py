# -*- coding: utf-8 -*-
"""
Created on Tue May 02 14:40:20 2017

@author: vsdaking
"""

import os
import pandas as pd
import numpy as np
import math
import random
import copy

### Testing specifically for KOR


## Test for Claims DS

path_in1 = "/home/latize/Desktop/TWG/Jap_3_dump/"
path_in2 = "/home/latize/Desktop/TWG/Jap_final_formatted_data/" 
path_op = "/home/latize/Downloads/JPN/claims/" 
path_schema = "/home/latize/Downloads/JPN/" 


fls_in1 = os.listdir(path_in1)
fls_in2 = os.listdir(path_in2)
fls_op = os.listdir(path_op)
fls_schema = os.listdir(path_schema)

print "Read final CSV"
#finalDf1 = pd.read_csv(path_op+'JPN_contracts_comma_to_space.csv', header=0, low_memory=False, nrows=200000)
#finalDf1 = pd.concat(pd.read_csv(path_op+"JPN_contracts_comma_to_space.csv", header = 0, low_memory=True, nrows=2000000))
finalDf1 = pd.concat(pd.read_csv(path_op+"jpn_claims_cleansed.csv", header = 0, low_memory=False, chunksize = 16*1024))
print "Finished reading final CSV"

fin_df_cols = list(finalDf1.columns)
if len(fin_df_cols)<3:
    fin_df_cols = fin_df_cols[0].split(',')


fin_df_cols2 = []

for z1 in fin_df_cols:
    if '.' in z1:
        fin_df_cols2.append(z1[z1.index('.')+1:])
    else:
         fin_df_cols2.append(z1)

finalDf1.columns = fin_df_cols2

print "Read Schema"
schema = pd.read_csv(path_schema+"twg_jpn_entire_metadata.csv", header=0, low_memory=True)    
print "Finished reading Schema"

inpFileLst = ['RO_EVENT.csv', 'CLIENT.csv', 'RO_HEADER.csv', 'RO_STATUS.csv', 'SERVICE_PERFORMED.csv', 'CONTRACT_DETAIL_FIN.csv',  '4_COMPONENT.csv',  '17_MODEL.csv',  '14_MFG.csv',  '21_PRODUCT_CLASS_COLLECTION.csv',  '22_PRODUCT_CLASS_SECTION.csv',  '23_PRODUCT_COVERAGE.csv', 'PRODUCT.csv', 'SKU.csv', '26_SERVICE_LOCATION.csv',  '29_WRITING_COMPANY.csv',  '8_COVERAGE_TYPE.csv',  '20_PRICE_RATING_METHOD.csv' ]

inp1 = inpFileLst[random.sample(xrange(len(inpFileLst)),1)[0]]

print "Read File 1: "+inp1

print "Finding columns for input file"
pth =""
if inp1 in fls_in1:
    pth = path_in1
else:
    pth = path_in2


inputFile1 = pd.read_csv(pth+inp1, header=None, low_memory = True)

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
		


if "_" in inp1[:2]:
	if RepresentsInt(inp1[0]):
		name = inp1[inp1.index('_')+1:-4]
	else:
		name = inp1[:-4]
else:
    name = inp1[:-4]

schema = schema.loc[schema['Table_names' ]== name]

inputFile1.columns = list(schema.Column_names)[:len(inputFile1.columns)]
inputFile_pks = [list(schema.Column_names)[m] for m in range(len(schema)) if list(schema.Primary_Key)[m]==1]

print "Finished reading inputFile 1",inp1
print "Also found", len(inputFile_pks), "primary keys - "
print inputFile_pks


print "#### Finished reading files"


print "#### Now updating and matching the column names "

duplicateCols = ['add_time', 'add_user', 'chg_time', 'chg_user', 'company_code', 'eng_desc', 'nat_desc', 'status', 'code', 'actg_dist_id', 'begin_date', 'end_date', 'id', 'pcc_code', 'chd_nbr', 'pcs_code', 'mfg_code', 'nbr', 'pmd_code', 'ins_code', 'igt_code', 'rns_code', 'rgt_code', 'seq', 'pce_code', 'mdl_code', 'tvl_term_type', 'tvl_term_len', 'srp', 'prod_id', 'cli_nbr', 'eng_name', 'type', 'serial_nbr', 'svl_code', 'lbr_term_type', 'lbr_term_len', 'can_date', 'adm_only', 'sku_code', 'wrt_code', 'pay_code', 'cmp_code', 'sell_client_amt', 'sell_client_amt_type', 'out_client_amt', 'out_client_amt_type', 'ded_id', 'new_used_type', 'cdt_seq', 'actg_cat_code', 'actg_sub_cat_code', 'faw_id', 'invoice_client_nbr', 'tax_id', 'line1', 'line2', 'line3', 'city_town', 'st_prov_terr', 'postal_code', 'cntry_code', 'phone', 'fax', 'mobil', 'pager', 'email', 'url', 'psset_id', 'psvendor_id', 'pslocation', 'vat_registration_id', 'prior_seq', 'liab_begin_date', 'liab_end_date', 'prod_pur_date', 'warr_pur_date', 'prod_del_date', 'sales_1', 'sales_2', 'cvt_type', 'prt_term_type', 'prt_term_len', 'mcp_term_type', 'mcp_term_len', 'lbr_begin_date', 'lbr_end_date', 'parts_begin_date', 'parts_end_date', 'mcp_begin_date', 'mcp_end_date', 'tvl_begin_date', 'tvl_end_date', 'prod_pur_amt', 'prem_amt', 'crn_code', 'eom_proc_date', 'prt_code', 'adm_code', 'cus_cont_nbr', 'cus_cont_seq_nbr', 'corp_cont_nbr', 'actg_per_mon', 'actg_per_year', 'actg_version', 'wrt_pur_prc', 'comm_usage', 'trans_chg', 'replace_cost', 'max_clm_amt_yr', 'max_clm_amt_chh', 'max_clm_amt_vis', 'max_clm_nbr_yr', 'max_clm_nbr_chh', 'upr_id', 'remitted_amt', 'force_code', 'comments', 'ivr_cus_cont_nbr', 'fullfill_date', 'flr_code', 'cdr_id', 'cpl_code', 'css_id', 'rat_id', 'pcv_id', 'trm_id', 'prs_id', 'bus_code', 'is_for_new_product', 'mmw_seq_nbr', 'for_id', 'max_vis_nbr_chh', 'max_clm_amt_repair', 'delivery_date', 'risk_owned_by_twg', 'covered_amount', 'wildcard', 'ros_code', 'odometer', 'adj_code', 'writing_company_type', 'amount', 'billable', 'ratable', 'collectible', 'user_enterable', 'commissions_payable', 'vendor_payable', 'gl_interface', 'fixed', 'nat_name', 'fctry_wty_type', 'term_mo', 'term_dist', 'deduct_amt', 'deduct_pct', 'coverage_min', 'coverage_max', 'rental_id', 'towing_id', 'own_code', 'transfer_id', 'coverage_plan_code', 'fuel_type', 'con_nbr', 'not_nbr', 'part_term_type', 'part_term_len']

inputCols = copy.copy(list(inputFile1.columns))

inpCols = []
	
for z2 in inputCols:
    z2 = z2.lower()
    if z2 in duplicateCols:
        #colll = "wrt_"+z2+"_mod"
        colll = list(schema.abbr)[0].lower()+z2+"_mod"
        if colll in fin_df_cols2:
            inpCols.append(colll)
        else:
            print z2, "and",colll,"both not in final df cols"
    else:
        inpCols.append(z2)
		

inputFile1.columns = inpCols	

print "Update Final Df column names due to multiple fields from same inp col"


# below tasks are now automated


# take a sample DS of 5%
# first, let us determine the random rows / indices to consider
print "Obtain random sample of inputFile1"

if len(inputFile1)<10000:
    print len(inputFile1), "rows selected"
    sampleFinalDataSetIndx = random.sample(xrange(len(finalDf1)), int(len(inputFile1)))
else:
    if len(inputFile1)/20.0<100000:
        print len(inputFile1)/20.0, "rows selected"
        sampleFinalDataSetIndx = random.sample(xrange(len(finalDf1)), int(len(inputFile1)/20.0))
    else:
        print len(inputFile1)/40.0, "rows selected"
        sampleFinalDataSetIndx = random.sample(xrange(len(finalDf1)), int(len(inputFile1)/40.0))



sampleFinalDf = finalDf1.loc[sampleFinalDataSetIndx]
print len(sampleFinalDf), "were the rows in the final DF used for comparision"
print "Generated random final data set"

pks = []
iCols = copy.copy(inpCols)
for z3 in inputFile_pks:
    for z4 in iCols:
        if z3.lower() in z4:
            pks.append(z4)
            iCols.remove(z4)
            break

print pks, "are the final PKs present in the input file"

for z4 in pks:
	ct=0
	if z4.lower().strip() not in fin_df_cols2:
		print z4, "is not in Final DF"
		ct=1
	if z4.lower().strip() not in inpCols:
		print z4, "is not in Final DF"
		ct=1
	if ct==0:
		print z4, "is everywhere"


correspondingInpDf2 = pd.merge(inputFile1, sampleFinalDf, how='inner', on = pks)
len(correspondingInpDf2)
matching_cols = [n1+"_x" for n1 in inputFile1.columns if n1 in sampleFinalDf.columns and n1 not in pks]
matching_cols.extend([n1 for n1 in inputFile1.columns if n1 in sampleFinalDf.columns and n1 in pks])
correspondingInpDf1 = correspondingInpDf2[matching_cols]
print "Generated corresponding input data set with ", len(matching_cols), "cols selected"



def findColsToCheck(finDfCols, inpDfCols, pKeys):
    #pKeys.append('ContractNum')
    finCols = [u for u in inpDfCols[random.sample(xrange(len(inpDfCols)), 5)] if u in finDfCols ]
    finCols = [u2 for u2 in finCols if u2 not in pKeys]
    #if 'ContractNum' in finCols:
    #	finCols.remove('ContractNum')
    fCols = copy.deepcopy(finCols)
    finCols = None
    return fCols

InpColLst = []
for n1 in correspondingInpDf1.columns:
	if '_x' in n1:
		InpColLst.append(n1[:-2])
	else:
		InpColLst.append(n1)

print "Updating the correspondingInpDf1 columns"
correspondingInpDf1.columns = InpColLst

print "find the cols to do comparison on"
chkCols = []
while len(chkCols)<3:
    chkCols = findColsToCheck(sampleFinalDf.columns, correspondingInpDf1.columns, pks)

print chkCols, "are the final cols to compare on"

accuracy = [[0 for n2 in range(len(correspondingInpDf1))] for n2 in range(len(chkCols))]

print "make copies of the input DFs)"
InpDf1 = copy.deepcopy(correspondingInpDf1)
sampleFinalDf2 = copy.deepcopy(sampleFinalDf)

print "sort the copies"
InpDf1.sort_values(pks, ascending=False, inplace=True)
sampleFinalDf2.sort_values(pks, ascending=False, inplace=True)


print "begin comparison of final sample cols"
for s in range(len(chkCols)):
    finalCol = list(sampleFinalDf2[chkCols[s]])
    inpCol = list(InpDf1[chkCols[s]])
    sum1=0
    if (len(finalCol)<len(inpCol)):
        colLen = len(finalCol)
    else:
	colLen = len(inpCol)
    for s2 in range(colLen):
        if inpCol[s2]!=finalCol[s2]:
            sum1=sum1+1
            accuracy[s][s2]=1
    print sum1, s

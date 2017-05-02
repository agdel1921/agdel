# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 15:47:04 2017

@author: vsdaking
"""


import os
import pandas as pd
import numpy as np
import math
import copy
import sys
import codecs

sys.setrecursionlimit(20000)

# define the path where the files are located
path = "D:/training/TWG_overall/data_harmonisation/KR/Claim_Data/"
path_op = "D:/training/TWG_overall/data_harmonisation/final_output_KR/"
#path2 = "/home/latize/Downloads/KR/claims/"

# set the working directory to the above defined path
os.chdir(path)

# read in all the files present at the said path
fls = os.listdir(path)


print "Started reading ANCLHP"
anclhpCols = ['CHCMPY', 'CHCLNT', 'CHYEAR', 'CHSERL', 'CHCTYP', 'CHSTSB', 'CHRSFG', 'CHRONO', 'CHACLN', 'CHPWAN', 'CHGCOD', 'CHGFLG', 'CHSALE', 'CHLINE', 'CHCPON', 'CHAGMN', 'CHVMID', 'CHVLNE', 'CHVBDY', 'CHVTRM', 'CHVRST', 'CHVENG', 'CHVCKD', 'CHVMDY', 'CHVPLN', 'CHVSEQ', 'CHENCP', 'CHEGNO', 'CHTMNO', 'CHDLDT', 'CHSLDT', 'CHCRPD', 'CHFSDT', 'CHLSDT', 'CHAJDT', 'CHRQDT', 'CHSNDT', 'CHRCDT', 'CHPDDT', 'CHCODM', 'CHPRPD', 'CHPODM', 'CHPRON', 'CHCPRT', 'CHNCOD', 'CHCCOD', 'CHERRC', 'CHOPCD', 'CHMLBR', 'CHSPMT', 'CHSLMT', 'CHSSMT', 'CHDDCT', 'CHAPMT', 'CHALMT', 'CHASMT', 'CHTOTL', 'CHVPLT', 'CHVUSE', 'CHVEND', 'CHLOT1', 'CHLOT2', 'CHFTDT', 'CHLTDT', 'CHUSID', 'CHLTAC']
anclhp = pd.read_csv(path+'Claim Header_ANCLHP.CSV', header=None, low_memory = True)
anclhp.columns = anclhpCols
print "Ended reading ANCLHP"

print "Started reading ANCLPP"
anclppCols = ['CHCMPY', 'CHCLNT', 'CHYEAR', 'CHSERL', 'CPLINE', 'CPPART', 'CPSPTQ', 'CPSPTP', 'CPSPTA', 'CPAPTQ', 'CPAPTP', 'CPAPTA', 'CPMKUP']
anclpp = pd.read_csv(path+'Claim Part_ANCLPP.CSV', header=None, low_memory = True)
anclpp.columns = anclppCols
print "Ended reading ANCLPP"

print "Started merging both data sets"
result = pd.merge(anclhp, anclpp, on = ['CHCLNT', 'CHCMPY','CHSERL','CHYEAR'])
print "Finished merging both data sets"

kr_claimCols = ['Country', 'Company', 'BusinessType', 'ContractNum', 'ContractSeqNum', 'ClaimNum', 'ClaimStatus', 'ClaimBreakdownDate', 'ClaimEventNum', 'ClaimEventStatus', 'ClientClaimNum', 'ClaimEventEnteredDate', 'RepairReceivedDate', 'RepairDate', 'PaymentOrderedDate', 'PaidDate', 'ServicePerformed', 'ServicePerformed_Native', 'ServiceLocation', 'ReplaceFlag', 'ClaimOdo', 'LaborRate', 'LaborHours', 'PartsAmt', 'MajorAmt', 'LaborAmt', 'TravelAmt', 'DeliveryAmt', 'TaxAmt', 'ClaimAmt_Gross', 'DeductibleAmt', 'ClaimAmt_Net', 'CustomerAmtAdj', 'OtherAmtAdj', 'ClaimAmt_AdjNet', 'PartCode_1', 'PartName_1', 'PartAmt_1', 'PartQty_1', 'PartCode_2', 'PartName_2', 'PartAmt_2', 'PartQty_2', 'PartCode_3', 'PartName_3', 'PartAmt_3', 'PartQty_3', 'PartCode_4', 'PartName_4', 'PartAmt_4', 'PartQty_4', 'PartCode_5', 'PartName_5', 'PartAmt_5', 'PartQty_5', 'PartCode_6', 'PartName_6', 'PartAmt_6', 'PartQty_6', 'PartCode_7', 'PartName_7', 'PartAmt_7', 'PartQty_7', 'PartCode_8', 'PartName_8', 'PartAmt_8', 'PartQty_8', 'PartCode_9', 'PartName_9', 'PartAmt_9', 'PartQty_9', 'PartCode_10', 'PartName_10', 'PartAmt_10', 'PartQty_10', 'AdjustmentCode', 'OverrideReason', 'RejectReason', 'AERecordNum']


kr_claimPd = []

chk1 = 9
for z in range(len(result)):
    if type(result.CHAGMN[z])==float:
        if math.isnan(result.CHAGMN[z]):
            kr_claimPd.append(['KOR', result.CHCMPY[z], 'MR', 0, 0, result.CHCMPY[z]+ " "+ result.CHCLNT[z]+ " "+str(result.CHYEAR[z])+ " "+str(result.CHSERL[z]), result.CHSTSB[z], 0, 0, 0, 0, 0, result.CHLSDT[z], result.CHCRPD[z], result.CHRQDT[z], result.CHPDDT[z], 0, 0, 0, 0, result.CHCODM[z], 0, 0, result.CHAPMT[z], 0, result.CHALMT[z], 0, 0, 0, result.CHTOTL[z], result. CHDDCT[z], 0, 0, 0, 0, result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CHSTSB[z], 0, result.CHERRC[z], z])
            chk1=0
        else:
            kr_claimPd.append(['KOR', result.CHCMPY[z], 'MR', result.CHAGMN[z], result.CHAGMN[z], result.CHCMPY[z]+ " "+ result.CHCLNT[z]+ " "+str(result.CHYEAR[z])+ " "+str(result.CHSERL[z]), result.CHSTSB[z], 0, 0, 0, 0, 0, result.CHLSDT[z], result.CHCRPD[z], result.CHRQDT[z], result.CHPDDT[z], 0, 0, 0, 0, result.CHCODM[z], 0, 0, result.CHAPMT[z], 0, result.CHALMT[z], 0, 0, 0, result.CHTOTL[z], result. CHDDCT[z], 0, 0, 0, 0, result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CHSTSB[z], 0, result.CHERRC[z], z])
            chk1 = 1
    else:
        kr_claimPd.append(['KOR', result.CHCMPY[z], 'MR', result.CHAGMN[z][0: 11], result.CHAGMN[z][11:13], result.CHCMPY[z]+ " "+ result.CHCLNT[z]+ " "+str(result.CHYEAR[z])+ " "+str(result.CHSERL[z]), result.CHSTSB[z], 0, 0, 0, 0, 0, result.CHLSDT[z], result.CHCRPD[z], result.CHRQDT[z], result.CHPDDT[z], 0, 0, 0, 0, result.CHCODM[z], 0, 0, result.CHAPMT[z], 0, result.CHALMT[z], 0, 0, 0, result.CHTOTL[z], result. CHDDCT[z], 0, 0, 0, 0, result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CPPART[z], 0, result.CPAPTA[z], result.CPAPTQ[z], result.CHSTSB[z], 0, result.CHERRC[z], z])
        chk1=2
    if chk1<1:
        print z, "nan"
    elif chk1<2:
        print z, "float"
    else:
        print z

kr_claimPd2 = pd.DataFrame(kr_claimPd, columns = kr_claimCols)

        
kr_claimPd2.to_csv(path_op+"kr_claims.csv", header=True, index=False)

# determine the rows in contracts files
path_contr = "D:/training/TWG_overall/data_harmonisation/final_output_KR/contracts/"

fls = os.listdir(path_contr)

for i2 in fls:
    m2 = pd.read_csv(path_contr+i2, header=0, low_memory=True)
    print i2, len(m2)
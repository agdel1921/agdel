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

path_in = "D:/training/TWG_overall/data_harmonisation/KR/Claim_Data/" 
path_op = "D:/training/TWG_overall/data_harmonisation/final_output_KR/claims/" 
path_schema = "D:/training/TWG_overall/data_harmonisation/KR/final_files_to_use_170407/" 


fls1 = os.listdir(path_in)
fls2 = os.listdir(path_op)

print "Read final CSV"
finalDf = pd.read_csv(path_op+'merged_not_mapped_claims_KOR.csv', header=0, low_memory=False, nrows = 2500000)

print "Read Schema"
schema = pd.read_csv(path_schema+"170407_finalSchema.csv", header=0, low_memory=False)    

print "Read File 1"
anclhpCols = list(schema.loc[schema['Table_Name'] == 'ANCLHP'].Field_Code)


anclhp = pd.read_csv(path_in+'Claim Header_ANCLHP.CSV', header=None, low_memory = False)
anclhp.columns = list(schema.loc[schema['Table_Name'] == 'ANCLHP'].Field_Code)

print "Read File 2"
anclpp = pd.read_csv(path_in+'Claim Part_ANCLPP.CSV', header=None, low_memory=False)
anclpp.columns = list(schema.loc[schema['Table_Name'] == 'ANCLPP'].Field_Code)
# update ANCLPP cols to reflect the ANCLHP FKs
anclppNewCols = []

for i3 in anclpp.columns:
    if i3 in ['CPCLNT', 'CPCMPY','CPSERL','CPYEAR']:
        anclppNewCols.append(i3[0]+'H'+i3[2:])
    else:
        anclppNewCols.append(i3)

anclpp.columns = anclppNewCols

print "Finished reading files"

# ANCLHP and ANCLPP were merged on ['CHCLNT', 'CHCMPY','CHSERL','CHYEAR']


# below tasks are now automated


# take a sample DS of 2.5%
# first, let us determine the random rows / indices to consider
sampleFinalDataSetIndx = random.sample(xrange(len(finalDf)), int(len(finalDf)/20))

sampleFinalDf = finalDf.loc[sampleFinalDataSetIndx]
print "Generated random final data set"


correspondingInpDf2 = pd.merge(anclpp, sampleFinalDf, how='inner', on=['CHCLNT', 'CHCMPY','CHSERL','CHYEAR'])
correspondingInpDf1 = correspondingInpDf2[anclpp.columns]
print "Generated corresponding input data set"



def findColsToCheck(finDfCols, inpDfCols, pKeys):
    finCols = [u for u in inpDfCols[random.sample(xrange(len(inpDfCols)), 5)] if u in finDfCols ]
    finCols = [u2 for u2 in finCols if u2 not in pKeys]
    fCols = copy.deepcopy(finCols)
    finCols = None
    return fCols

chkCols = []
while len(chkCols)<3:
    chkCols = findColsToCheck(sampleFinalDf.columns, anclpp.columns, ['CHCLNT', 'CHCMPY','CHSERL','CHYEAR'])

accuracy = [[0 for n2 in range(len(correspondingInpDf1))] for n in range(len(chkCols))]


InpDf1 = copy.deepcopy(correspondingInpDf1)
sampleFinalDf2 = copy.deepcopy(sampleFinalDf)

InpDf1.sort_values(['CHCLNT', 'CHCMPY','CHSERL','CHYEAR'], ascending=False, inplace=True)
sampleFinalDf2.sort_values(['CHCLNT', 'CHCMPY','CHSERL','CHYEAR'], ascending=False, inplace=True)


for s in range(len(chkCols)):
    finalCol = list(sampleFinalDf2[chkCols[s]])
    inpCol = list(InpDf1[chkCols[s]+'_x'])
    sum1=0
    for s2 in range(len(inpCol)):
        if inpCol[s2]!=finalCol[s2]:
            sum1=sum1+1
            accuracy[s][s2]=1
    print sum1, s
    
    
    
# ANCLHP
correspondingInpDf2 = pd.merge(anclhp, sampleFinalDf, how='inner', on=['CHCLNT', 'CHCMPY','CHSERL','CHYEAR'])
correspondingInpDf1 = correspondingInpDf2[anclhp.columns]
print "Generated corresponding input data set"



def findColsToCheck(finDfCols, inpDfCols, pKeys):
    finCols = [u for u in inpDfCols[random.sample(xrange(len(inpDfCols)), 5)] if u in finDfCols ]
    finCols = [u2 for u2 in finCols if u2 not in pKeys]
    fCols = copy.deepcopy(finCols)
    finCols = None
    return fCols

chkCols = []
while len(chkCols)<3:
    chkCols = findColsToCheck(sampleFinalDf.columns, anclhp.columns, ['CHCLNT', 'CHCMPY','CHSERL','CHYEAR'])

accuracy = [[0 for n2 in range(len(correspondingInpDf1))] for n in range(len(chkCols))]


InpDf1 = copy.deepcopy(correspondingInpDf1)
sampleFinalDf2 = copy.deepcopy(sampleFinalDf)

InpDf1.sort_values(['CHCLNT', 'CHCMPY','CHSERL','CHYEAR'], ascending=False, inplace=True)
sampleFinalDf2.sort_values(['CHCLNT', 'CHCMPY','CHSERL','CHYEAR'], ascending=False, inplace=True)


for s in range(len(chkCols)):
    finalCol = list(sampleFinalDf2[chkCols[s]])
    inpCol = list(InpDf1[chkCols[s]+'_x'])
    sum1=0
    for s2 in range(len(inpCol)):
        if inpCol[s2]!=finalCol[s2]:
            sum1=sum1+1
            accuracy[s][s2]=1
    print sum1, s

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 17:17:08 2017

@author: Latize
"""

import pandas as pd
import numpy as np
import os
import time
import copy
import matplotlib.pyplot as plt
import math
import collections
import gc


#path1 = 'D:/training/Prudential/data/data/'
#path2 = 'D:/training/Prudential/data/vd_test/'
path1_brkUp = 'C:/data/170810/data/'
path2_brkUp = 'C:/data/170810/test_170810/'
path_metadata_brkUp = 'C:/data/170810/metadata/'
path_prog = 'C:/data/170810/origins/'
os.chdir(path1_brkUp)

listPath = []
listPath.append(path1_brkUp)
listPath.append(path2_brkUp)
listPath.append(path_metadata_brkUp)

for pth in listPath:
    if not os.path.exists(pth):
        os.makedirs(pth)
        print ("Created path "+pth)
    else:
        print (pth +" already exists")


amgPd = pd.DataFrame()
#premiumFileName = 'ag_input_170724.csv'
premiumFileName = os.listdir(path1_brkUp)[0]

start_amg = time.time()
# read in the Component-level Premium file
for chunk in pd.read_csv(path1_brkUp+premiumFileName, chunksize = 100000, low_memory=False):
    amgPd = pd.concat([amgPd,chunk])
end_amg = time.time()
print (amgPd.shape)

amgPd = amgPd[['cownnum', 'chdrnum','cnttype','crtable']]

userNumber = list(amgPd.cownnum)
cntr = collections.Counter(userNumber)
vals = cntr.values()
kys = cntr.keys()

print "There are "+str(len(np.unique(np.array(amgPd.cownnum))))+" unique customers with transactions in 2017"

# read in the Customer Profile file
start_cust = time.time()
custPd = pd.DataFrame()
for chunk in pd.read_csv(path_metadata_brkUp+'min_custProfile_17.csv', chunksize = 100000, low_memory=False):
    custPd = pd.concat([custPd,chunk])
end_cust = time.time()
print custPd.shape

# determine users with only more than 1 Inforce policy
custConsider = custPd.loc[custPd['noifp']>1]
custNoConsider = custPd.loc[custPd['noifp']<2]
print amgPd.shape
ignoreUser = [kys[k2] for k2 in range(len(vals)) if vals[k2]<2 and kys[k2] not in custConsider.clntnum]
amgPd = amgPd[~amgPd['cownnum'].isin(ignoreUser)]

print amgPd.shape



mergedAmg = pd.merge(amgPd, custPd, how='left', left_on='cownnum', right_on='clntnum')

mergedIFP = [k for k in np.unique(mergedAmg.noifp) if not math.isnan(k)]

for rng in mergedIFP:
    print "\n For",rng
    custTmp = mergedAmg.loc[mergedAmg['noifp']==rng]
    print custTmp.age.describe()
    if not os.path.exists(path2_brkUp+str(int(rng))+"/"):
        os.makedirs(path2_brkUp+str(int(rng))+"/")
        custTmp.columns = mergedAmg.columns
        custTmp.to_csv(path2_brkUp+str(int(rng))+"/custProfile_"+str(rng)+".csv", header=True, index=False)
        print str(custTmp.shape)
    custTmp=None


whitelist = ['gc', 'whitelist','path_prog']

for name in locals().keys():
    if not name.startswith('_') and name not in whitelist:
        del locals()[name]

execfile(path_prog+'2_generate_crosstab_Pru_basic_data_170719_pipelined.py')
execfile(path_prog+'3_h1b1_2_ag_170718.py')

print "fin! :)"
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 16:31:59 2017

@author: Latize
"""

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import os
import time
import copy
import matplotlib.pyplot as plt
import collections


#path = 'D:/training/Prudential/'
#path0 = 'D:/training/Prudential/data/'
#path1_crosstab = 'D:/training/Prudential/data/data/'
#path2_crosstab = 'D:/training/Prudential/data/vd_test/'
path1_crosstab = 'C:/data/data/'
path1_crosstab = 'C:/data/170810/test_170810/'
path2_crosstab = 'C:/data/vd_test/test16/'
path2_crosstab = 'C:/data/170810/vd_test/test_1/'
path_metadata_crosstab = 'C:/data/170810/metadata/'
path_prog = 'C:/data/170810/origins/'

os.chdir(path1_crosstab)

listPath = []
listPath.append(path1_crosstab)
listPath.append(path2_crosstab)
listPath.append(path_metadata_crosstab)

for pth in listPath:
    if not os.path.exists(pth):
        os.makedirs(pth)
        print "Created path "+pth
    else:
        print pth +" already exists"

os.chdir(path1_crosstab)

dirs = [x[0] for x in os.walk(path1_crosstab)]
dirs = dirs[1:]
print dirs

for path_n in dirs:
    os.chdir(path_n)
    print path_n
    fls = [fl for fl in os.listdir(path_n) if fl[:12]=="custProfile_"]
    if len(fls)>0:
        print fls, len(fls[0])
        start_amg = time.time()
        amgPd = pd.DataFrame()
        #premiumFileName = 'premium_combo.csv'
        premiumFileName = fls[0]

        # read in the Component-level Premium file
        for chunk in pd.read_csv(path_n+"/"+premiumFileName, chunksize = 100000, low_memory=False):
            amgPd = pd.concat([amgPd,chunk])
        end_amg = time.time()
        print amgPd.shape

        custNum = list(amgPd.cownnum)

        print np.unique(np.array(amgPd.noifp))

        #amgPd['fullProdName'] = amgPd['cnttype']+' '+amgPd['crtable']

        amgPd = amgPd[['cownnum','cnttype']]

        user_u = list(sorted(amgPd.cownnum.unique()))
        item_u = list(sorted(amgPd.cnttype.unique()))

        row = amgPd.cownnum.astype('category', categories=user_u).cat.codes
        col = amgPd.cnttype.astype('category', categories=item_u).cat.codes

        data = np.array([1 for k in range(len(amgPd))])

        sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_u), len(item_u)))

        df = pd.SparseDataFrame([ pd.SparseSeries(sparse_matrix[i].toarray().ravel(), fill_value=0) for i in np.arange(sparse_matrix.shape[0]) ],
                               index=user_u, columns=item_u, default_fill_value=0)
        finCols = ['cownnum']
        len(finCols)
        finCols.extend(df.columns)
        len(finCols)

        dfMtrx = np.empty(shape = (df.shape[0]+1,df.shape[1]+1), dtype=np.ndarray)
        dfMtrx[:1,:][0] = finCols
        dfMtrx[1:,0] = user_u
        dfMtrx[1:,1:] = df.values
        print dfMtrx.shape
        np.savetxt(path2_crosstab+'test17h1b1_'+premiumFileName[:-4]+"_17_fin.csv", dfMtrx, delimiter=",",fmt='%s')

whitelist = ['gc', 'whitelist','path_prog']

for name in locals().keys():
    if not name.startswith('_') and name not in whitelist:
        del locals()[name]

execfile(path_prog+'3_h1b1_2_ag_170718.py')


import gc
gc.collect()
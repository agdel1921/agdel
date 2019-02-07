# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 16:17:09 2017

@author: ashutosh.gaur
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 02 10:54:32 2017

@author: ashutosh.gaur
"""

import pandas as pd
import os
import time 

path1 = 'C:/data/170810/vd_test/test_2/'
path2 = 'C:/data/170810/vd_test/test_1/testdata_20170817/'
os.chdir(path1)

start_amg = time.time()
amgPd = pd.DataFrame()
#premiumFileName = 'premium_combo.csv'
premiumFileName = 'test17h1b1_custProfile_4.0_17_fin.csv'

ct=0
# read in the input file
for chunk in pd.read_csv(path1+premiumFileName, chunksize = 15000, low_memory=False):
    pos1 = premiumFileName.find(".csv")
    fileName = premiumFileName[:pos1]
    
#    if not os.path.exists(path2+fileName+"/"):
#        path3 = path2+fileName+"/"
#        os.makedirs(path3)
#    path3 = path2+fileName+"/"
    destName = path2+premiumFileName[:pos1]+"_"+str(ct)+".csv"
    chunk.to_csv(destName, header=True, index= False)
    print str(ct), chunk.shape
    ct = ct +1
end_amg = time.time()
print amgPd.shape
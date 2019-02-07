# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 12:06:19 2017

@author: ashutosh.gaur
"""

import pandas as pd
import numpy as np
from datetime import datetime
import time 
import os
import gc


path1 = 'C:/data/data/'
path3 = 'C:/data/input_data_og/'
pathOp = 'C:/data/170810/data/'
path_prog = 'C:/data/170810/origins/'

os.chdir(path1)

listPath = []
listPath.append(path1)
listPath.append(path3)
listPath.append(pathOp)

for pth in listPath:
    if not os.path.exists(pth):
        os.makedirs(pth)
        print "Created path "+pth
    else:
        print pth +" already exists"
    
amgPd = pd.DataFrame()
#premiumFileName = 'premium_combo.csv'
premiumFileName = 'Premium17.csv'
#premiumFileName = 'ag_input_170724.csv'



# read in the Component-level Premium file
start_amg = time.time()
for chunk in pd.read_csv(path1+premiumFileName, chunksize = 100000, low_memory=False):
    amgPd = pd.concat([amgPd,chunk])
end_amg = time.time()
print amgPd.shape

products_soldPd = pd.read_csv(path3+'currently_sold_products_mid_term_add.csv', header=0)    
cntPresent = list(products_soldPd.cnttype)

# lower case the columns in amgPd, for further usage
amgPd.columns = [k.lower() for k in amgPd.columns]

# select only those rows with contracts currently being sold
amgPd = amgPd[amgPd['cnttype'].isin(cntPresent)]

# export the data set to pathOp
amgPd.to_csv(pathOp+'current_'+premiumFileName[:-4]+'_'+str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))+'.csv', header=True, index=False)



amgPd = None
chunk = None
cntPresent = None
end_amg = None
start_amg = None
listPath = None
products_soldPd = None

execfile(path_prog+'1_breakUp_custProfile_pipelined.py')
execfile(path_prog+'2_generate_crosstab_Pru_basic_data_170719_pipelined.py')
execfile(path_prog+'3_h1b1_2_ag_170718.py')


import gc
gc.collect()
###### End of current module

print "fin! :)"



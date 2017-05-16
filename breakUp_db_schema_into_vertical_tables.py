# -*- coding: utf-8 -*-
"""
Created on Tue May 16 11:38:19 2017

@author: Latize
"""

import os
import pandas as pd
import sys  
reload(sys)  
#sys.setdefaultencoding('utf-8')


path = "D:/training/TWG_overall/data_harmonisation/JPN_HW/zipped/output/final_metadata_files/"
os.chdir(path)
fls = os.listdir(path)

print fls

for s in fls:
    if s[-4:]=="xlsx":
        pd1 = pd.read_excel(s, header=0)
        print s, len(pd1)
        tbl_name = list(pd1.TABLE_NAME)
        field_name = list(pd1.FIELD_NAME)
        pos = list(pd1.ORDINAL_POSITION)
        indx = [i for i in range(len(list(pos))) if list(pos)[i]==1]
        print indx
        print len(indx)
        pd2 = pd.DataFrame()
        for s2 in range(len(indx)):
            if s2==len(indx)-1:
                tmpPd = pd.DataFrame([str(y) for y in field_name[indx[s2]:len(pos)]])
            else:
                try:
                    tmpPd = pd.DataFrame([str(y) for y in field_name[indx[s2]:indx[s2+1]]])
                except UnicodeEncodeError:
                    tmpPd = pd.DataFrame([y.encode('ascii') for y in field_name[indx[s2]:indx[s2+1]]])
            pd2 = pd.concat([pd2, tmpPd], ignore_index=True, axis=1)
        colNames = [str(tbl_name[x]) for x in indx[:pd2.shape[1]]]
        pd2.columns = colNames    
        pd2.to_csv(path+s[:-4]+"csv", headers= True, index=False)

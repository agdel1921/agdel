# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 15:55:01 2017

@author: vsdaking
"""


# import required libraries
import pandas as pd
import os
import numpy as np

# set the working directory
path = "D:/training/pd_ag/"
os.chdir(path)
fls1=os.listdir(path)

def classifyDataType(dType,pos):
    if dType in ['int','bigint','smallint']:
        return "xsd:integer"
    elif dType in ['varchar','text','mediumtext','char']:
        return "xsd:string"
    elif dType in ['datetime','date']:
        return "xsd:dateTime" 
    elif dType in ['decimal']:
       return "xsd:float"
    else:
        print "Unknown data type encountered at position ",pos
        return "xsd:string"
   
# run the program for all CSV files in the path
for a2 in fls1:
    if a2[-3:]=='csv':
        # read in the CSV file and store it in a DF (data frame) called m
        csvPd = pd.read_csv(a2, header=0)
        dest1 = path+"chk/"+a2[:-4]+".xlsx"
        print dest1

        # find loaded DF col names
        csvPd.columns
        
        # extract specific cols that we need from schema
        usablePd = csvPd.ix[:,['TABLE_SCHEMA', 'TABLE_NAME','COLUMN_NAME','ORDINAL_POSITION','IS_NULLABLE','DATA_TYPE','COLUMN_KEY']]
        
        # create the output structure - DF & 2D Mtrx
        #opPd = pd.DataFrame(columns = ['CLASS', 'SubClassOf', 'PROPERTIES', 'PERMISSIBLE VALUES','REMARKS'])
        #opMtrx = [['CLASS', 'SubClassOf', 'PROPERTIES', 'PERMISSIBLE VALUES','REMARKS']]
        opMtrx = []
        class_name = list(usablePd['TABLE_NAME'])
        class_name = [k21.strip() for k21 in class_name]
        class_props = list(usablePd['COLUMN_NAME'])
        class_props = [k22[:1].lstrip().title()+k22[1:].rstrip() for k22 in class_props]
        class_superClass = list(usablePd['TABLE_SCHEMA'])
        class_ordinal = list(usablePd['ORDINAL_POSITION'])
        prop_dataType = list(usablePd['DATA_TYPE'])
        prop_KeyType = list(usablePd['COLUMN_KEY'])
                
        distnct_classNames = np.unique(class_name)
        
        
        for k in distnct_classNames:
            db = ""
            for y in range(len(class_name)):
                if class_name[y]==k:
                    colName = class_props[y]
                    dataType = prop_dataType[y]
                    keyType = prop_KeyType[y]
                    if class_ordinal[y]==1:
                        db = class_superClass[y]
                        opMtrx.append([k, db, "", "", ""])
                    # in case colName is neither a Primary Key (PRI) or a Foreign Key (MUL)
                    if keyType =="MUL":
                        ind = [ty for ty in range(len(class_name)) if  class_name[ty] != class_name[y]]
                        #print numpy.unique([class_name[ki] for ki in range(len(class_name)) if ki in ind])  
                        for op in ind:
                            if class_props[op]==class_props[y]:
                               if prop_KeyType[op]=="PRI":
                                    # uncomment below condition to ensure the PK and FK data types match as well
                                    # if dataType ==prop_dataType[op]:
                                    print class_props[y], "in",class_name[y], "points to ",class_name[op]
                                    opMtrx.append(["","",colName,"latize:"+class_name[op]+" "+classifyDataType(dataType,y),""])
                    else:
                        opMtrx.append(["","",colName,classifyDataType(dataType,y),""])
            opMtrx.append(["","","","",""])
        
        opPd = pd.DataFrame(opMtrx, columns = ['CLASS', 'SubClassOf', 'PROPERTIES', 'PERMISSIBLE VALUES','REMARKS'])
        #opPd.to_csv("D:/training/pd_ag/chk/trial.csv", header=True, index=False)
        opPd.to_excel(dest1, header=True, index=False)
        print dest1
 
        """
for ut in range(len(prop_KeyType)):
    if prop_KeyType[ut]=="PRI":
        print class_props[ut],"is a Primary Key"
    elif prop_KeyType[ut]=="MUL":
        print class_props[ut],"is a Foreign Key"
        #print class_name[ut]
        ind = [ty for ty in range(len(class_name)) if  class_name[ty] != class_name[ut]]
        #print numpy.unique([class_name[ki] for ki in range(len(class_name)) if ki in ind])  
        for op in ind:
            if class_props[op]==class_props[ut]:
                if prop_KeyType[op]=="PRI":
                    print class_props[ut], "in",class_name[ut], "points to ",class_name[op]
    else:
        continue
print ind
"""
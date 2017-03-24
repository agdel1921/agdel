# -*- coding: utf-8 -*-
"""
Created on Tue Mar 07 10:18:35 2017

@author: Ashu & vsdaking
"""

# this program aims to connect MySQL to python and extract each DB's schema & corresponding Data Dictionary

import pandas as pd
import os
import numpy as np

hostname = 'localhost'
username = 'root'
password = 'vidyut@latize'
database = 'sakila'

# Simple routine to run a query on a database and print the results:

print "Using pymysql…"
import pymysql
myConnection = pymysql.connect( host=hostname, user=username, passwd=password)
with myConnection.cursor() as cursor:
    # The SQL command to be extract all metadata for all contents in the given 'database'
    sql = "SELECT * from information_schema.columns WHERE table_schema = '" + database +"';"
    
    # The SQL command to extract all PKs and FKs in the given database
    sql11= "SELECT * FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA='" + database +"' or REFERENCED_TABLE_SCHEMA = '"+database+"';"    
    
    # store the result of the SQL commands into 2 Pandas DF
    dbMetadataOvrall = pd.read_sql(sql,myConnection)
    dbMetadataKeys = pd.read_sql(sql11,myConnection)

# herein, we now have to resolve the PKs & FKs present in the tables for each DB
pks = ["DB_Name","Table_Name",[]]
fks = ["DB_Name","Table_Name",[]]

keysOgSchema = list(dbMetadataKeys.TABLE_SCHEMA)
keysOgTbl = list(dbMetadataKeys.TABLE_NAME)
keysOgCol = list(dbMetadataKeys.COLUMN_NAME)
keysConstraintName = list(dbMetadataKeys.CONSTRAINT_NAME)
keysRefSchema = [str(s) for s in list(dbMetadataKeys.REFERENCED_TABLE_SCHEMA)]
keysRefTbl = [str(s) for s in list(dbMetadataKeys.REFERENCED_TABLE_NAME)]
keysRefCol = [str(s) for s in list(dbMetadataKeys.REFERENCED_COLUMN_NAME)]

                  
finalDfTbl = list(dbMetadataOvrall.TABLE_NAME)
finalDfCol = list(dbMetadataOvrall.COLUMN_NAME)
finalDfSchema = list(dbMetadataOvrall.TABLE_SCHEMA)
finalDfDType = list(dbMetadataOvrall.DATA_TYPE)



for k1 in range(len(keysOgTbl)):
    tbl_from = keysOgTbl[k1]
    tbl_col = keysOgCol[k1]
    tbl_constrName = keysConstraintName[k1]
    if keysConstraintName[k1] == "PRIMARY":
        for k2 in range(len(finalDfTbl)):
            if finalDfSchema[k2]==keysOgSchema[k1]:
                if finalDfTbl[k2] == keysOgTbl[k1]:
                    if finalDfCol[k2] == keysOgCol[k1]:
                        #print finalDfSchema[k2], finalDfTbl[k2], finalDfCol[k2]
                        #print keysOgSchema[k1], keysOgTbl[k1], keysOgCol[k1]
                        dbMetadataOvrall.set_value(dbMetadataOvrall.index[k2-1], 'COLUMN_KEY', 'PRI')
                        break;
    elif 'fk_' in keysConstraintName[k1]:
        if keysRefSchema[k1]!='None' and keysRefTbl[k1]!='None' and keysRefCol[k1]!='None':
            for k3 in range(len(finalDfTbl)):
                if finalDfSchema[k3]==keysOgSchema[k1]:
                    if finalDfTbl[k3] == keysOgTbl[k1]:
                        if finalDfCol[k3] == keysOgCol[k1]:
                            # below commented out if condition checks if the data types match for the PK & FK - plz complete this later
                            # if finalDfDType[k3] == 
                            print finalDfSchema[k3], finalDfTbl[k3], finalDfCol[k3], k3
                            print keysRefSchema[k1], keysRefTbl[k1], keysRefCol[k1], k1, keysOgSchema[k1], keysOgTbl[k1], keysOgCol[k1], k1
                            dbMetadataOvrall.set_value(dbMetadataOvrall.index[k3], 'COLUMN_KEY', 'FOR')
                            break;
        

    
dest1= "D:/training/pd_ag/"+database+".csv"
#dest1= "F:/latize/auto_ontology/"+database+".csv"
dbMetadataOvrall.to_csv(dest1, header=True, index=False)
dest2 = "F:/latize/auto_ontology/"+database+"_keys.csv"
dbMetadataKeys.to_csv(dest2, header=True, index=False)

# determine the tables for which we want to extract data from the DB
t_name = list(np.unique(dbMetadataOvrall.TABLE_NAME))

# determine the DB name to which the tables belong
db_name = list(np.unique(dbMetadataOvrall.TABLE_SCHEMA))

db = db_name[0]
for tn in t_name:
    # The SQL command to extract data from the table
    myConnection = pymysql.connect( host=hostname, user=username, passwd=password)
    sql = "use "+ db +";"
    curs = myConnection.cursor()
    curs.execute(sql)
    sql2 = "SELECT * from " + tn +";"
    # store the result of the SQL command into a Pandas DF
    d5 = pd.read_sql(sql2,myConnection)
    db_TblName = db+"__"+tn
    #dest2= "F:/latize/auto_ontology/data/"+db_TblName+".csv"
    dest2= "D:/training/pd_ag/data/"+db_TblName+".csv"
    d5.to_csv(dest2, header=True, index=False)

myConnection.close()

execfile("D:/CodeLah!/latize/rdb2owl.py")
execfile("D:/CodeLah!/latize/trial.py")
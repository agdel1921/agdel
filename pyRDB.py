# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 10:44:58 2017

@author: Ashu & vsdaking
"""

# this program aims to connect MySQL to python and extract each DB's schema & corresponding Data Dictionary

import pandas as pd
import os
import numpy as np

hostname = 'localhost'
username = 'root'
password = 'vidyut@latize'
database = 'wfs'

# Simple routine to run a query on a database and print the results:

print "Using pymysql…"
import pymysql
myConnection = pymysql.connect( host=hostname, user=username, passwd=password)
with myConnection.cursor() as cursor:
    # The SQL command to be executed
    #sql = "SELECT * from information_schema.columns WHERE table_schema = '" + database +"';"
    sql = "SELECT * from information_schema.columns WHERE table_schema = '" + database +"';"
    
    sql11= "SELECT TABLE_SCHEMA,TABLE_NAME,COLUMN_NAME,REFERENCED_TABLE_SCHEMA,REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA IS NOT NULL;" 
   
    # store the result of the SQL command into a Pandas DF
    
    m51 = pd.read_sql(sql1,myConnection)
    M512 = pd.read_sql(sql11,myConnection)

    
    
    # store the result of the SQL command into a Pandas DF
    m5 = pd.read_sql(sql,myConnection)
dest1= "D:/training/pd_ag/"+database+".csv"
m5.to_csv(dest1, headers=True, index=False)

# determine the tables for which we want to extract data from the DB
t_name = list(np.unique(m5.TABLE_NAME))

# determine the DB name to which the tables belong
db_name = list(np.unique(m5.TABLE_SCHEMA))

db = db_name[0]
for tn in t_name:
    # The SQL command to extract data from the table
    myConnection = pymysql.connect( host=hostname, user=username, passwd=password)
    sql = "use "+ db +";"
    curs = myConnection.cursor()
    curs.execute(sql)
    sql2 = "SELECT * from " + tn +";"
    # store the result of the SQL command into a Pandas DF
    #d5 = pd.read_sql(sql2,myConnection)
    dest2= "D:/training/pd_ag/data/"+tn+".csv"
    #d5.to_csv(dest2, headers=True, index=False)

myConnection.close()

execfile("D:/CodeLah!/latize/rdb2owl.py")
execfile("D:/CodeLah!/latize/trial.py")
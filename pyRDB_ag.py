# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 10:44:58 2017

@author: Ashu & vsdaking
"""

# this program aims to connect MySQL to python and extract each DB's schema & corresponding Data Dictionary

import pandas as pd
import os
import pymysql

# Passing Mysql Connection credentials
hostname = 'localhost'
username = 'root'
password = 'latize'
database = 'test1'

# Connecting python console to mysql and executing query

myConnection = pymysql.connect( host=hostname, user=username, passwd=password)

 # The SQL command to extract schema from the given "database"
with myConnection.cursor() as cursor:
    sql = "SELECT * from information_schema.columns WHERE table_schema = '" + database +"';"
#    sql1 = "SELECT * from information_schema.table_constraints WHERE table_schema = '" + database +"';"    
    sql11= "SELECT TABLE_SCHEMA,TABLE_NAME,COLUMN_NAME,REFERENCED_TABLE_SCHEMA,REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA IS NOT NULL;" 
   
    # store the result of the SQL command into a Pandas DF
    
    m5 = pd.read_sql(sql,myConnection)
#    m51 = pd.read_sql(sql1,myConnection)
    M512 = pd.read_sql(sql11,myConnection)


myConnection.close()  # closing the connection / Disconnecting Mysql server

# Creating CSV file to store the schema
dest1= "D:/Latize/Ontology/RDB2OWL_VER1.2/"+database+".csv"
#dest2= "D:/Latize/Ontology/RDB2OWL_VER1.2/"+database+"_const.csv"
dest3= "D:/Latize/Ontology/RDB2OWL_VER1.2/"+database+"_foreign.csv"
# Writing Schema in csv format
m5.to_csv(dest1, headers=True, index=False)
#m51.to_csv(dest2, headers=True, index=False)
#M512.to_csv(dest3, headers=True, index=False)
  
# executing / transfering control to another python scripts to explore and transform
# Database schema to owl / turtle format

# Exploring the database schema
execfile("D:/Latize/Ontology/RDB2OWL_VER1.2/rdb2owl.py")

# Transforming the elements into turtle / owl format 
execfile("D:/Latize/Ontology/RDB2OWL_VER1.2/trial_ver1.2.py")
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 14:18:35 2018

@author: LatizeExpress
"""

"""
This file is to prepare some generic code for NTUC data validation and manipulation
This file is generated by Ivy Yi on 20180817
"""

__author__ = 'Latize'
import os
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np
os.environ['SPARK_HOME']=r"C:\opt\spark\spark-2.3.1-bin-hadoop2\spark-2.3.1-bin-hadoop2.7"
sys.path.append(r"C:\opt\spark\spark-2.3.1-bin-hadoop2\spark-2.3.1-bin-hadoop2.7\python")
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql.types import IntegerType
from pyspark.sql.types import FloatType
from functools import reduce
from pyspark.sql.functions import substring
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.linalg import Vectors
from pyspark.ml.stat import Correlation
from pyspark.ml.stat import ChiSquareTest
from pyspark.sql.functions import col
from pyspark.mllib.stat import Statistics
import datetime
from pyspark.sql.types import *
from pyspark.sql.functions import udf
from pyspark.sql import functions as F
conf = SparkConf().setMaster("local").setAppName("NTUC")
sc = SparkContext(conf = conf)
sqlContext=SQLContext(sc)

def read_file(path):
    df = sqlContext.read.csv(path,header=True)
    return (df)

def clean_header(data,oldColumns,newColumns):
    df = reduce(lambda data, idx: data.withColumnRenamed(oldColumns[idx], newColumns[idx]), range(len(oldColumns)), data)
    return(df)

def change_to_int(data,col):
    for conv_col in col:
        data = data.withColumn(conv_col, data[conv_col].cast(IntegerType()))
    return(data)

def change_to_float(data,col):
    for conv_col in col:
        data = data.withColumn(conv_col, data[conv_col].cast(FloatType()))
    return(data)

def change_to_month(data,col):
    for conv_col in col:
        data = data.withColumn(conv_col, data[conv_col].substr(1, 7))
    return(data)

def data_exploration(data,data_name):
    categorical_data=pd.DataFrame()
    descriptive_data=pd.DataFrame()

    categorical_output_loc = r"E:/NTUC/Processed/Categorical_output_/" + data_name + ".csv"
    descriptive_output_loc = r"E:/NTUC/Processed/desc_output_/" + data_name + ".csv"
    for column in data.schema.names:
        graph_name=r"E:/NTUC/Processed/Graph_chart_/" + data_name + "_" + column + ".png"
        flag=data.schema[column].dataType
        categorical_update=data.groupby(column).count().toPandas()
        categorical_update=categorical_update.sort_values(by="count",ascending=False).reset_index(drop=True)
        categorical_data=pd.concat([categorical_data, categorical_update], axis=1, sort=False)
        if isinstance(flag,IntegerType) or isinstance(flag,FloatType):
            descriptive_update=data.describe(column).toPandas()
            descriptive_data = pd.concat([descriptive_data, descriptive_update], axis=1, sort=False)
            categorical_update_graph = categorical_update
            categorical_update_graph.set_index(column, inplace=True)
            plot = categorical_update_graph.plot.bar()
            fig = plot.get_figure()
            fig.savefig(graph_name)
    categorical_data.to_csv(categorical_output_loc, header=True, index=False)
    descriptive_data.to_csv(descriptive_output_loc, header=True, index=False)
    return()

def unique_counts(sampledata):
    path = r"E:/NTUC/Processed/UniqueOutput_/" + "unique" + ".csv"
    for i in sampledata.columns:
        sample = sampledata.toPandas()
        count = sample[i].nunique()
        print(i,": ", count)
        return()


def contentAnalysis(sampleData):
    sample12 = sampleData.toPandas()
    abc = sample12.corr(method='pearson')
    print(abc)
    path = r"E:/NTUC/Processed/correlation/"+"correlation" + ".csv"
    abc.to_csv(path,header=True, index=False)
    return()
#path
path = "E:/NTUC/raw_data/LifeStage_AffinityData/LifeStage.csv"
path1 ="E:/NTUC/raw_data/LifeStage_AffinityData/Affinity.csv"
path2 ="E:/NTUC/raw_data/LifeStage_AffinityData/Affiliation.csv"
path3 = "E:/NTUC/raw_data/LifeStage_AffinityData/groupby_sum.csv"
path4 = "E:/NTUC/raw_data/LifeStage_AffinityData/groupby_sum1.csv"
path5 = "E:/NTUC/raw_data/LifeStage_AffinityData/groupby_count.csv"




#Reading File
df = pd.read_csv(path, low_memory = True)
df.columns
len(df)

df1 = pd.read_csv(path1, low_memory = True)
df1.columns
len(df1)


df2 = pd.read_csv(path2, low_memory = True)
df2.columns
len(df2)

df3 = pd.read_csv(path3, low_memory = True)
df3.columns
len(df3)

df4 = pd.read_csv(path4, low_memory = True)
df4.columns
len(df4)

df5 = pd.read_csv(path5, low_memory = True)
df5.columns
len(df5)


#Group by
#Groupby count
df2.groupby(['customerseqid', 'customerstatus']).count()
df2.groupby(['customerseqid', 'policytype']).count()


group_Status = df2.groupby(['customerseqid', 'customerstatus'])
group_policytype = df2.groupby(['customerseqid', 'policytype'])
group = df2.groupby('customerseqid')
group.columns

niqId = df5['customerseqid'].unique()


# aggregation of groupby

test = group.aggregate(np.sum)
group.sum().reset_index().to_csv(path2+'grouped.csv', index = False)
group.count().reset_index().to_csv(path2+'grouped_count.csv', index = False)

niqId.count().reset_index().to_csv(path2+'uniqueCustomerID.csv',

test1 =df2.groupby('customerseqid').count()
len(test1)
test1.columns
df.groupby('customerseqid').count()

customergroup = df.groupby('customerseqid')


path_out = "E:/NTUC/raw_data/Final/results_affluence/"

#result.head(5)
len(result)
result.to_csv(path_out+'Affluence_final_weight.csv', header =True, index = False)


#Data Exploration
prod_test=read_file(path2)

data_exploration(prod_test,"Affiliation_Summary")












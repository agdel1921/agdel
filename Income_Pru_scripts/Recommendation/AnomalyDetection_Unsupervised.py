# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 10:10:30 2018

@author: LatizeExpress
"""

#Anomaly detection using unsupervised methods
import numpy as np
INPUT = "hdfs://localhost/data/kdd"

def parse_line(line):
    bits = line.split(",")
    return np.array([float(e) for e in bits[4:12]])

df = sc.textFile(INPUT).map(parse_line)

# Identifying Outliers
stats = df.map(lambda e: e[0]).stats()
mean, stdev = stats.mean(), stats.stdev()
outliers = df.filter(lambda e: not (mean - 2 * stdev > e[0] > mean + 2 * stdev))
outliers.collect()


#Clustering
from pyspark.mllib.clustering import KMeans
clusters = KMeans.train(df, 5, maxIterations=10,
    runs=1, initializationMode="random")

cluster_sizes = df.map(lambda e: clusters.predict(e)).countByValue()


def get_distance(clusters):
    def get_distance_map(record):
        cluster = clusters.predict(record)
        centroid = clusters.centers[cluster]
        dist = np.linalg.norm(record - centroid)
        return (dist, record)
    return get_distance_map

data_distance = df.map(get_distance(clusters))
hist = data_distance.keys().histogram(10)


def unisample(df, fraction=1.0):
    columns = df.first()
    new_df = None
    for i in range(0, len(columns)):
        column = df.sample(withReplacement=True, fraction=fraction)
            .map(lambda row: row[i])
            .zipWithIndex()
            .map(lambda e: (e[1], [e[0]]))
        if new_df is None:
            new_df = column
        else:
            new_df = new_df.join(column)
            new_df = new_df.map(lambda e: (e[0], e[1][0] + e[1][1]))
    return new_df.map(lambda e: e[1])



def supervised2unsupervised(model):
    def run(df, *args, **kwargs):
        unisampled_df = unisample(df)
        unisampled_df = unisample(df)
        labeled_data = df.map(lambda e: LabeledPoint(1, e))
            .union(unisampled_df.map(lambda e: LabeledPoint(0, e)))
        return model(labeled_data, *args, **kwargs)
    return run



from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import RandomForest

unsupervised_forest = supervised2unsupervised(RandomForest.trainClassifier)
rf_model = unsupervised_forest(df, numClasses=2, categoricalFeaturesInfo={},
                  numTrees=10, featureSubsetStrategy="auto",
                  impurity='gini', maxDepth=15, maxBins=50)





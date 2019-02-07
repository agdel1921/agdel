# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 10:41:30 2018

@author: LatizeExpress
"""
./bin/spark-shell --packages \
   "org.apache.lucene:lucene-analyzers-common:5.1.0"
val line="Flick. A tiny, almost invisible movement, " +
  "and the house was still."
val tokens=Stemmer.tokenize(line)
# tokens: Seq[String] = ArrayBuffer(flick, tini, almost,
#   invis, movement, hous, still)

import org.apache.spark.mllib.feature.HashingTF
val tf = new HashingTF(10)

val hashed = tf.transform(tokens)


import org.apache.spark.mllib.feature.IDF
val idfModel = new IDF(minDocFreq = 3).fit(trainDocs)
val idfs = idfModel.transform(hashed)

val data = mockData.union(watchData)
val splits = data.randomSplit(Array(0.7, 0.3))
val trainDocs = splits(0).map{ x=>x.features}
val idfModel = new IDF(minDocFreq = 3).fit(trainDocs)
val train = splits(0).map{
  point=>LabeledPoint(point.label,idfModel.transform(point.features))
}
val test = splits(1).map{
  point=>LabeledPoint(point.label,idfModel.transform(point.features))
}
train.cache()


import org.apache.spark.mllib.classification.{NaiveBayes,
  NaiveBayesModel}
val nbmodel = NaiveBayes.train(train, lambda = 1.0)
val bayesTrain = train.map(p => (nbmodel.predict(p.features), p.label))
val bayesTest = test.map(p => (nbmodel.predict(p.features), p.label))
println("Mean Naive Bayes performance")
(bayesTrain.filter(x => x._1 == x._2).count() /
  bayesTrain.count().toDouble,
  bayesTest.filter(x => x._1 == x._2).count() /
  bayesTest.count().toDouble)



import org.apache.spark.mllib.tree.RandomForest
import org.apache.spark.mllib.tree.model.RandomForestModel
import org.apache.spark.mllib.tree.GradientBoostedTrees
import org.apache.spark.mllib.tree.configuration.BoostingStrategy
import org.apache.spark.mllib.tree.model.GradientBoostedTreesModel

// RANDOM FOREST REGRESSION
val categoricalFeaturesInfo = Map[Int, Int]()
val numClasses = 2
val featureSubsetStrategy = "auto"
val impurity = "variance"
val maxDepth = 10
val maxBins = 32
val numTrees = 50
val modelRF = RandomForest.trainRegressor(train,
  categoricalFeaturesInfo, numTrees, featureSubsetStrategy,
  impurity, maxDepth, maxBins)

// GRADIENT BOOSTED TREES REGRESSION
val boostingStrategy = BoostingStrategy.defaultParams("Regression")
boostingStrategy.numIterations = 50
boostingStrategy.treeStrategy.maxDepth = 5
boostingStrategy.treeStrategy.categoricalFeaturesInfo = Map[Int, Int]()
val modelGB = GradientBoostedTrees.train(train, boostingStrategy)


//// Random forest model metrics on training data
val trainScores = train.map { point =>
  val prediction = modelRF.predict(point.features)
  (prediction, point.label)

//// Random forest model metrics on training data
val trainScores = train.map { point =>
  val prediction = modelRF.predict(point.features)
  (prediction, point.label)
}
val metricsTrain = new BinaryClassificationMetrics(trainScores,100)
val trainroc= metricsTrain.roc()
trainroc.saveAsTextFile("/ROC/rftrain")
metricsTrain.areaUnderROC()



//// Random forest model metrics on test data
val testScores = test.map { point =>
  val prediction = modelRF.predict(point.features)
  (prediction, point.label)
}
val metricsTest = new BinaryClassificationMetrics(testScores,100)
val testroc= metricsTest.roc()
testroc.saveAsTextFile("/ROC/rftest")
metricsTest.areaUnderROC()






# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 10:32:13 2018

@author: LatizeExpress
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





































// SQLContext entry point for working with structured data
val sqlContext = new org.apache.spark.sql.SQLContext(sc)

// This is used to implicitly convert an RDD to a DataFrame.
import sqlContext.implicits._
// Import Spark SQL data types
import org.apache.spark.sql._
// Import mllib recommendation data types
import org.apache.spark.mllib.recommendation.{ALS,
  MatrixFactorizationModel, Rating}


/ input format MovieID::Title::Genres
case class Movie(movieId: Int, title: String, genres: Seq[String])

// input format is UserID::Gender::Age::Occupation::Zip-code
case class User(userId: Int, gender: String, age: Int,
  occupation: Int, zip: String)

/ function to parse input into Movie class
def parseMovie(str: String): Movie = {
      val fields = str.split("::")
      assert(fields.size == 3)
      Movie(fields(0).toInt, fields(1), Seq(fields(2)))
 }

// function to parse input into User class
def parseUser(str: String): User = {
      val fields = str.split("::")
      assert(fields.size == 5)
      User(fields(0).toInt, fields(1).toString, fields(2).toInt,
        fields(3).toInt, fields(4).toString)
 }


// load the data into a RDD
val ratingText = sc.textFile("/home/jovyan/work/datasets/spark-ebook/ratings.dat")

// Return the first element in this RDD
ratingText.first()



/ function to parse input UserID::MovieID::Rating
// Into org.apache.spark.mllib.recommendation.Rating class
def parseRating(str: String): Rating= {
      val fields = str.split("::")
      Rating(fields(0).toInt, fields(1).toInt, fields(2).toDouble)
}

// create an RDD of Ratings objects
val ratingsRDD = ratingText.map(parseRating).cache()

println("Total number of ratings: " + ratingsRDD.count())

println("Total number of movies rated: " +
  ratingsRDD.map(_.product).distinct().count())

println("Total number of users who rated movies: " +
  ratingsRDD.map(_.user).distinct().count())




/ load the data into DataFrames
val usersDF = sc.textFile("/home/jovyan/work/datasets/spark-ebook/users.dat").
  map(parseUser).toDF()
val moviesDF = sc.textFile("/home/jovyan/work/datasets/spark-ebook/movies.dat").
  map(parseMovie).toDF()

// create a DataFrame from the ratingsRDD
val ratingsDF = ratingsRDD.toDF()

// register the DataFrames as a temp table
ratingsDF.registerTempTable("ratings")
moviesDF.registerTempTable("movies")
usersDF.registerTempTable("users")


sersDF.printSchema()

moviesDF.printSchema()

ratingsDF.printSchema()


/ Get the max, min ratings along with the count of users who have
// rated a movie.
val results = sqlContext.sql(
  """select movies.title, movierates.maxr, movierates.minr, movierates.cntu
    from(SELECT ratings.product, max(ratings.rating) as maxr,
    min(ratings.rating) as minr,count(distinct user) as cntu
    FROM ratings group by ratings.product ) movierates
    join movies on movierates.product=movies.movieId
    order by movierates.cntu desc""")

// DataFrame show() displays the top 20 rows in  tabular form
results.show()


 Show the top 10 most-active users and how many times they rated
// a movie
val mostActiveUsersSchemaRDD = sqlContext.sql(
  """SELECT ratings.user, count(*) as ct from ratings
  group by ratings.user order by ct desc limit 10""")

println(mostActiveUsersSchemaRDD.collect().mkString("\n"))

// Find the movies that user 4169 rated higher than 4
val results = sqlContext.sql("""SELECT ratings.user, ratings.product,
  ratings.rating, movies.title FROM ratings JOIN movies
  ON movies.movieId=ratings.product
  where ratings.user=4169 and ratings.rating > 4""")

results.show
##ALS
/ Randomly split ratings RDD into training
// data RDD (80%) and test data RDD (20%)
val splits = ratingsRDD.randomSplit(Array(0.8, 0.2), 0L)

val trainingRatingsRDD = splits(0).cache()
val testRatingsRDD = splits(1).cache()

val numTraining = trainingRatingsRDD.count()
val numTest = testRatingsRDD.count()
println(s"Training: $numTraining, test: $numTest.")

// build a ALS user product matrix model with rank=20, iterations=10
val model = (new ALS().setRank(20).setIterations(10)
  .run(trainingRatingsRDD))


# Predictions

/ Get the top 4 movie predictions for user 4169
val topRecsForUser = model.recommendProducts(4169, 5)

// get movie titles to show with recommendations
val movieTitles=moviesDF.map(array => (array(0), array(1))).
  collectAsMap()

// print out top recommendations for user 4169 with titles
topRecsForUser.map(rating => (movieTitles(
  rating.product), rating.rating)).foreach(println)


##Model Evaluation
/ get user product pair from testRatings
val testUserProductRDD = testRatingsRDD.map {
  case Rating(user, product, rating) => (user, product)
}

// get predicted ratings to compare to test ratings
val predictionsForTestRDD  = model.predict(testUserProductRDD)

predictionsForTestRDD.take(10).mkString("\n")


/ prepare predictions for comparison
val predictionsKeyedByUserProductRDD = predictionsForTestRDD.map{
  case Rating(user, product, rating) => ((user, product), rating)
}

// prepare test for comparison
val testKeyedByUserProductRDD = testRatingsRDD.map{
  case Rating(user, product, rating) => ((user, product), rating)
}

//Join the test with predictions
val testAndPredictionsJoinedRDD = testKeyedByUserProductRDD.
  join(predictionsKeyedByUserProductRDD)

// print the (user, product),( test rating, predicted rating)
testAndPredictionsJoinedRDD.take(3).mkString("\n")



val falsePositives = (
  testAndPredictionsJoinedRDD.filter{
    case ((user, product), (ratingT, ratingP)) => (ratingT <= 1 && ratingP >=4)
  })
falsePositives.take(2)
falsePositives.count()




// Evaluate the model using Mean Absolute Error (MAE) between test
// and predictions
val meanAbsoluteError = testAndPredictionsJoinedRDD.map {
  case ((user, product), (testRating, predRating)) =>
    val err = (testRating - predRating)
    Math.abs(err)
}.mean()
println(meanAbsoluteError)




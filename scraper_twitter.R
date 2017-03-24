# import the twitteR library for use
if(!require(twitteR)) {
  install.packages("twitteR"); require(twitteR)}
if(!require(wordcloud)) {
  install.packages("wordcloud"); require(wordcloud)}
if(!require(igraph)) {
  install.packages("igraph"); require(igraph)}
if(!require(tm)) {
  install.packages("tm"); require(tm)}
if(!require(ROAuth)) {
  install.packages("ROAuth"); require(ROAuth)}
if(!require(curl)) {
  install.packages("curl"); require(curl)}


# set the authentication keys of 4 different apps for usage
ckey <- c("TDdDg7XUOccCaFS9NvEg6ADr1","W2OCkMO2ybGFVU4s7BgXFk0MO","YlyNuGXxkCIwTbTENShCVyAV4","IhUFgQqUSJi668S81ifMQx3Mw")
csecret <- c("cFF44BcWwJm37Tqit2ATj1nJl2CaMm4Tah1OscpHov3nMDoDiQ","Hm5dGOZNCQ3SliwMiSMZTRo35k7ZFfQoGmvjpVkpUseuTGEjeJ","bj5dbh3RpsHohAxMuVN3zkjfNGrtZUbJlwYueWwqOeDfHaijCj","zepyErdr92kiCO68O4uT68JUHcVoACOi7FCakqh4inkGJj1pmo")
atoken <- c("16280903-SHcxm2NHJy1CpFYa1muJ7tdulN99Dlhql45Nj5LpY","16280903-EgpG7X9XQbmcajILrMAK7Tf6FOmqHEnNc8sCvZDbf","	16280903-hNz3jkAo2PePYt42gF0MaJLurEd6VWV744X0N52DO", "16280903-RvkGJ55mNd25DQiEplnd8a2OzIqroW4BoF63S7NZY")
asecret <- c("ehoStGnleKxgLl6tKxrwUjgWTTJ3rKp5PWhCHmKF2NTTf","GWrIwseUzVQwxJx2L1VfkF4gBs9hNu6Bq1UbtjBSvmhSG","pCt3HJLZ0ia3dlGQqAfmkY6erKIFaxtvpeH6CXwy5e5SG","oqWZg5sdVQkkFITq8VmQ2o7uTo599duFehU6tJ3uWKCtZ")

consumerKey <- ckey[1]
consumerSecret <- csecret[1]
access_token <- atoken[1]
access_token_secret <- asecret[1]
  

searchTwitter("sers Singapore", n=3000)


# import the twitteR library for use
if(!require(twitteR)) {
  install.packages("twitteR"); require(twitteR)}
if(!require(stringr)) {
  install.packages("stringr"); require(stringr)}

# set the authentication keys of 4 different apps for usage
ckey <- c("W2OCkMO2ybGFVU4s7BgXFk0MO","YlyNuGXxkCIwTbTENShCVyAV4","TDdDg7XUOccCaFS9NvEg6ADr1","IhUFgQqUSJi668S81ifMQx3Mw")
csecret <- c("Hm5dGOZNCQ3SliwMiSMZTRo35k7ZFfQoGmvjpVkpUseuTGEjeJ","bj5dbh3RpsHohAxMuVN3zkjfNGrtZUbJlwYueWwqOeDfHaijCj","cFF44BcWwJm37Tqit2ATj1nJl2CaMm4Tah1OscpHov3nMDoDiQ","zepyErdr92kiCO68O4uT68JUHcVoACOi7FCakqh4inkGJj1pmo")
atoken <- c("16280903-EgpG7X9XQbmcajILrMAK7Tf6FOmqHEnNc8sCvZDbf","16280903-hNz3jkAo2PePYt42gF0MaJLurEd6VWV744X0N52DO","16280903-SHcxm2NHJy1CpFYa1muJ7tdulN99Dlhql45Nj5LpY","16280903-RvkGJ55mNd25DQiEplnd8a2OzIqroW4BoF63S7NZY")
asecret <- c("GWrIwseUzVQwxJx2L1VfkF4gBs9hNu6Bq1UbtjBSvmhSG","pCt3HJLZ0ia3dlGQqAfmkY6erKIFaxtvpeH6CXwy5e5SG","ehoStGnleKxgLl6tKxrwUjgWTTJ3rKp5PWhCHmKF2NTTf","oqWZg5sdVQkkFITq8VmQ2o7uTo599duFehU6tJ3uWKCtZ")

# choose any of the apps ofr usage - range the indice from 1 to 4
consumerKey <- ckey[2]
consumerSecret <- csecret[2]
access_token <- atoken[2]
access_token_secret <- asecret[2]

# establish the authentication handshake
setup_twitter_oauth(consumerKey,consumerSecret,access_token,access_token_secret)

# obtain the metadata associated with the "Airbnb_SG" twitter handle
# convert it to a DF and save it in excel
#user <- getUser("Airbnb_SG")
uName = "HootsuiteAPAC"
output_path_base = paste("D:\\training\\Use_Cases\\Discovery\\vd_trial",uName,sep="\\")
user <- getUser(uName)
lo <- user$toDataFrame()
#write.csv(flo,"D:\\training\\Use_Cases\\Discovery\\vd_trial\\eskimon_metadata.csv")
write.csv(lo,paste(output_path_base,"_metadata.csv",sep=""))

# obtain the metadata associated with Airbnb_SG followers
# convert it to a DF and save it in excel
follow <- user$getFollowers()
flo <- twListToDF(follow)
#write.csv(flo,"D:\\training\\Use_Cases\\Discovery\\vd_trial\\eskimon_followers.csv")
write.csv(flo,paste(output_path_base,"_followers.csv",sep=""))

# obtain the timeline posts associated with the Airbnb_SG handle
# convert it to a DF and save it in excel
timel <- userTimeline(user,n=3200,includeRts = TRUE)
tlo <- twListToDF(timel)
#write.csv(lo,"D:\\training\\Use_Cases\\Discovery\\vd_trial\\eskimon_post_timeline.csv")
write.csv(tlo,paste(output_path_base,"_post_timeline.csv",sep=""))

read_file <- read.csv("C:\\Users\\Vidyut Singhania\\Downloads\\New_Business_Cases\\twitter_research\\AirbnbTwitterUsers.csv")

colnames((read_file))

speakr <- as.list(read_file[,"Voice.Name"])

speakr_split <- split(speakr, ceiling(seq_along(speakr)/100))
speakr_split <- speakr_split[,drop=T]
r <- 0
for (i in speakr_split){
  r <- r+1 
  lp <- getUser(i,includeNA = FALSE)
  ldf <- lp$toDataFrame()
  pth <- "C:\\Users\\Vidyut Singhania\\Downloads\\New_Business_Cases\\twitter_research\\Twitter\\"
  ext <- ".csv"
  pth <- paste(pth,r,ext,sep="")
  write.csv(ldf,pth)
}
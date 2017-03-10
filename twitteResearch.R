if(!require(installr)) {
  install.packages("installr"); require(installr)} #load / install+load installr

#updateR()

if(!require(devtools)) {
  install.packages(c("devtools", "rjson", "bit64", "httr")); require(devtools)}

if(!require(twitteR)) {
  install.packages("twitteR"); require(twitteR)}

if(!require(plyr)) {
  install.packages("plyr"); require(plyr)}

if(!require(tm)) {
  install.packages("tm"); require(tm)}

if(!require(base64enc)) {
  install.packages("base64enc"); require(base64enc)}

if(!require("wordcloud")) {
  install.packages(c("wordcloud","tm"),repos="http://cran.r-project.org"); require("wordcloud")}

if(!require(httpuv)) {
  install.packages("httpuv"); require(httpuv)}

#Setting up the OAuth Key
api_key <- "vtHQe8yMDnFG1r1R1wN05sX1M"

api_secret <- "Wu7Fzau36IXCYQ0Ot6NmJfeKCrcI5kdRLOREc83yAUHslBXdOy"

atoken <- " 16280903-96YlRjV7ZQUiMXatzcclDzjjMt8hx38484WLlAALP"

atoken_secret <- "McGVxwJ9C6OD318Og6nbXp77HOITjbrojg6JwMKR1n0Xl"

setup_twitter_oauth(api_key,api_secret,access_token=atoken)

vd <- userTimeline("vsdaking",n=2000)

vidyut <- getUser("vsdaking")

str(vidyut)

str(vd)

df <- do.call("rbind", lapply(vd, as.data.frame))

write.table(df,"C:\\Users\\Vidyut Singhania\\Downloads\\New Business Cases\\Data Sets\\trial.xls")



if(!require(RSQLite)) {
  install.packages("RSQLite"); require(RSQLite)} #load / install+load installr


conTw <- dbConnect(SQLite())
dbGetInfo(conTw)
dbWriteTable(conTw, "timeline", df)
dbListTables(conTw)
dbReadTable(conTw,"timeline")
dbListFields(conTw,"timeline")
dbDisconnect(conTw)

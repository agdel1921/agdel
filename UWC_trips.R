# load the openxlsx for reading and writing xlsx files
if(!require(openxlsx)) {
  install.packages("openxlsx"); require(openxlsx)}
# load the data.table package to be able to use the fread command - fast read of csv
if(!require(data.table)) {
  install.packages("data.table"); require(data.table)}
# load the plyr package to be able to use the 'count' function
if(!require(plyr)) {
  install.packages("plyr"); require(plyr)}

# clears my enrionment
rm(list=ls())

# read the input csv file using the fread command instead of the read.table fn 
trip <- fread("D:\\vd\\vd_data\\trips.csv")

# determine the unique URIs / Email Addresses - each denotes a unique student
l <- unique(trip$EmailAddress)

# create an empty DF whilst declaring its structure
attenDetail = data.frame(matrix(vector(), 0, 8,dimnames=list(c(),c("Student Email","Dest 1", "Dest 2","Dest 3","General Companions","TripNature","TripCategory","totalTrips"))),stringsAsFactors = F)

###### core of program begins #######

# each iteration (i) of the for loop indicates a unique Student / Email Address 
for (i in l){
  # create a new row at the bottom of DF for entering new content - use placeholders of " " & 0 
  attenDetail[dim(attenDetail)[1]+1,]=matrix(c(i," "," "," ",0," "," ",0))
  
  # create a new DF comprising only rows pertaining to the specific Student in question (subset the OG DF by matching the Email Address)
  odin <- trip[which(trip$EmailAddress==i),]
  
  # 'count' determine the frequency of the vars (denoted by Destination below) 
  destFreq <- count(odin,'Destination')
  
  # order the newly created freq DF in descending order of the freq(uency)
  dfq <- destFreq[with(destFreq,order(-freq)),]
  natureFreq <- count(odin,'TripNature')
  nfq <- natureFreq[order(-natureFreq$freq),]
  natureFreq <- count(odin,'TripCategory')
  cfq <- natureFreq[order(-natureFreq$freq),]
  
  # store the content in the placeholders of the attenDetail DF - remember to use as.character / as.numeric, else problematic
  attenDetail[dim(attenDetail)[1],2]=as.character(dfq[1][[1]][1])
  attenDetail[dim(attenDetail)[1],3]=as.character(dfq[1][[1]][2])
  attenDetail[dim(attenDetail)[1],4]=as.character(dfq[1][[1]][3])
  attenDetail[dim(attenDetail)[1],5]=as.numeric(mean(odin$NoOfParticipants))
  attenDetail[dim(attenDetail)[1],6]=as.character(nfq[1][[1]][1])
  attenDetail[dim(attenDetail)[1],7]=as.character(cfq[1][[1]][1])
  attenDetail[dim(attenDetail)[1],8]=as.numeric(dim(odin)[1])
}
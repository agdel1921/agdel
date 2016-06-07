# load the openxlsx for reading and writing xlsx files
if(!require(openxlsx)) {
  install.packages("openxlsx"); require(openxlsx)}
# load the plyr package to be able to use the 'count' function
if(!require(plyr)) {
  install.packages("plyr"); require(plyr)}
if(!require(xlsx)) {
  install.packages("xlsx"); require(xlsx)}
if(!require(rJava)) {
  install.packages("rJava"); require(rJava)}

# clears my enrionment
rm(list=ls())

# read in the xlsx data file
#acaData <- read.xlsx("D:\\Data Sets\\UWC\\Attendance, Activity & Trips.xlsx",sheetIndex = 1)
# read in the csv data file
acaData <- fread("D:\\vd\\vd_data\\Attendance1_vd.csv",sep=",",header = TRUE)

# get a brief summary of acaData
str(acaData)
# eliminate the var StudentId
acaData$StudentId <- NULL
# supposed to round of all decimals places to 2 - emphasis on 'supposed to'! 
options(digits=2)

# determine the unique URIs / Email Addresses - each denotes a unique student
o <- unique(acaData$EmailAddress)

# create 2 empty DFs whilst declaring their structure
# attenDetail comprises the detailed info about the attendance in courses a student has taken
# attenTotal comprises the summarized info about each student
attenTotal <- data.frame(matrix(vector(),0,9,dimnames=list(c(),c("Student Email","Year","Course Most Present", "Classes Attended","Course Most Absent","Classes Missed","Course Most Late","Classes Late","Overall Attendance"))),stringsAsFactors = F)
attenDetail = data.frame(matrix(vector(), 0, 6,dimnames=list(c(),c("Student Email","Course Name", "Absent","Late","Present","Percent Present"))),stringsAsFactors = F)

###### core of program begins #######

# each iteration (i) of the for loop indicates a unique Student / Email Address 
for(i in o){
  
  # create a new DF comprising only rows pertaining to the specific Student in question 
  # (subset the OG DF by matching the Email Address)
  nor<-acaData[which(acaData$EmailAddress==i),]
  
  # determine the unique Classes taken by the student in question
  s<-unique(nor$ClassCode)
  
  # declare the variables for storing Present, Late & Absent values
  abs=late=pres=finAbs=finLate=finPres=0
  
  # create a new row at the bottom of summary DF for entering new content - use placeholders of " " & 0 
  attenTotal[dim(attenTotal)[1]+1,] =matrix(c(i," "," ",0," ",0," ",0,0))
  #print s
  for (k in s){
    print(paste("For class ",k,"the attendance of ",i," is :"))
    
    # create a new DF comprising only rows pertaining to the distinct courses taken by the Student in question 
    # (subset the subsetted DF by matching the class code)
    thor<-nor[which(nor$ClassCode==k),]
    
    # 'count' determine the frequency of the vars (denoted by Attendance below)
    # there may be different types of frequency tables - on the basis of Attendance types [Present, Late & Absent]
    m <- count(thor,'Attendance')
    print(m)
    
    # enter the Academic Year for the record
    attenTotal[dim(attenTotal)[1],2]=as.character(thor$AcademicYear[1])
    
    len <- dim(m)[1]
    # in case Present, Absent & Late all exist for the particular course
    if(len==3){
      # these conditions check if the existing stored values for pres, late or abs are smallers than those for the curent course
      if(m[2][[1]][3]>pres){
        pres=m[2][[1]][3]
        attenTotal[dim(attenTotal)[1],3]=k
        attenTotal[dim(attenTotal)[1],4]=pres
      }
      if(m[2][[1]][2]>late){
        late=m[2][[1]][2]
        attenTotal[dim(attenTotal)[1],7]=k
        attenTotal[dim(attenTotal)[1],8]=late
      }
      if(m[2][[1]][1]>abs){
        abs=m[2][[1]][1]
        attenTotal[dim(attenTotal)[1],5]=k
        attenTotal[dim(attenTotal)[1],6]=abs
      }
      attenDetail[dim(attenDetail)[1]+1,] =matrix(c(i,k,m[2][[1]][1],m[2][[1]][2],m[2][[1]][3],m[2][[1]][3]/as.double(m[2][[1]][1]+m[2][[1]][3]+m[2][[1]][2])))
    }
    else if(len==2){
      # in case only 2 of the 3 attendance types exist for the particular course
      if(m[1][[1]][1]=="Absent"){
        if(m[1][[1]][2]=="Present"){
          if(m[2][[1]][2]>pres){
            pres=m[2][[1]][2]
            attenTotal[dim(attenTotal)[1],3]=k
            attenTotal[dim(attenTotal)[1],4]=pres
          }
          if(m[2][[1]][1]>abs){
            abs=m[2][[1]][1]
            attenTotal[dim(attenTotal)[1],5]=k
            attenTotal[dim(attenTotal)[1],6]=abs
          }
          attenDetail[dim(attenDetail)[1]+1,] =matrix(c(i,k,m[2][[1]][1],0,m[2][[1]][2],m[2][[1]][2]/as.double(m[2][[1]][1]+m[2][[1]][2])))
        }
        else{
          if(m[2][[1]][2]>late){
            late=m[2][[1]][2]
            attenTotal[dim(attenTotal)[1],7]=k
            attenTotal[dim(attenTotal)[1],8]=late
          }
          if(m[2][[1]][1]>abs){
            abs=m[2][[1]][1]
            attenTotal[dim(attenTotal)[1],5]=k
            attenTotal[dim(attenTotal)[1],6]=abs
          }
          attenDetail[dim(attenDetail)[1]+1,] =matrix(c(i,k,m[2][[1]][1],m[2][[1]][2],0,0))
        }
      }
      else if(m[1][[1]][1]=="Late"){
        if(m[2][[1]][2]>pres){
          pres=m[2][[1]][2]
          attenTotal[dim(attenTotal)[1],3]=k
          attenTotal[dim(attenTotal)[1],4]=pres
        }
        if(m[2][[1]][1]>late){
          late=m[2][[1]][1]
          attenTotal[dim(attenTotal)[1],7]=k
          attenTotal[dim(attenTotal)[1],8]=late
        }
        attenDetail[dim(attenDetail)[1]+1,] =matrix(c(i,k,0,m[2][[1]][1],m[2][[1]][2],m[2][[1]][2]/as.double(m[2][[1]][1]+m[2][[1]][2])))        
      }      
    }
    else{
      # in case only 1 of the 3 attendance types exist for the particular course
      if(m[1][[1]][1]=="Absent"){
        if(m[2][[1]][1]>abs){
          abs=m[2][[1]][1]
          attenTotal[dim(attenTotal)[1],5]=k
          attenTotal[dim(attenTotal)[1],6]=abs
        }
        attenDetail[dim(attenDetail)[1]+1,] =matrix(c(i,k,m[2][[1]][1],0,0,0))
      }
      else if(m[1][[1]][1]=="Late"){
        if(m[2][[1]][1]>late){
          late=m[2][[1]][1]
          attenTotal[dim(attenTotal)[1],7]=k
          attenTotal[dim(attenTotal)[1],8]=late
        }
        attenDetail[dim(attenDetail)[1]+1,] =matrix(c(i,k,0,m[2][[1]][1],0,0))
      }
      else{
        if(m[2][[1]][1]>pres){
          pres=m[2][[1]][1]
          attenTotal[dim(attenTotal)[1],3]=k
          attenTotal[dim(attenTotal)[1],4]=pres
        }
        attenDetail[dim(attenDetail)[1]+1,] =matrix(c(i,k,0,0,m[2][[1]][1],1))
      }
    }
    # update the total Present, Absent & Late scores for the student
    finPres = finPres+as.numeric(attenDetail[dim(attenDetail)[1],5])
    finAbs = finAbs+as.numeric(attenDetail[dim(attenDetail)[1],3])
    finLate = finLate+as.numeric(attenDetail[dim(attenDetail)[1],4])
  }
  attenTotal[dim(attenTotal)[1],9]=finPres/as.double(finPres+finLate+finAbs)
}

attenDetail$Absent <- as.numeric(attenDetail$Absent)
attenDetail$Late <- as.numeric(attenDetail$Late)
attenDetail$Present <- as.numeric(attenDetail$Present)
attenDetail$Percent.Present <- as.numeric(attenDetail$Percent.Present)

attenTotal$Classes.Attended <- as.numeric(attenTotal$Classes.Attended)
attenTotal$Classes.Missed <- as.numeric(attenTotal$Classes.Missed)
attenTotal$Classes.Late <- as.numeric(attenTotal$Classes.Late)
attenTotal$Overall.Attendance <- as.numeric(attenTotal$Overall.Attendance)

write.xlsx(attenTotal,"D:\\vd\\vd_data\\individualAttendanceSummary1.xlsx", sheetName = "2011-13", row.names = FALSE)
write.xlsx(attenDetail,"D:\\vd\\vd_data\\individualDetailedAttendance1.xlsx", sheetName = "2011-13",row.names = FALSE)

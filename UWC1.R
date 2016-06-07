if(!require(openxlsx)) {
  install.packages("openxlsx"); require(openxlsx)}
if(!require(plyr)) {
  install.packages("plyr"); require(plyr)}
if(!require(xlsx)) {
  install.packages("xlsx"); require(xlsx)}
if(!require(rJava)) {
  install.packages("rJava"); require(rJava)}

rm(list=ls())
acaData <- read.xlsx("D:\\Data Sets\\UWC\\Attendance, Activity & Trips.xlsx",sheetIndex = 1)
acaData <- fread("D:\\vd\\vd_data\\Attendance1_vd.csv",sep=",",header = TRUE)

str(acaData)
acaData$StudentId <- NULL
options(digits=2)

o <- unique(acaData$EmailAddress)

attenTotal <- data.frame(matrix(vector(),0,9,dimnames=list(c(),c("Student Email","Year","Course Most Present", "Classes Attended","Course Most Absent","Classes Missed","Course Most Late","Classes Late","Overall Attendance"))),stringsAsFactors = F)
attenDetail = data.frame(matrix(vector(), 0, 6,dimnames=list(c(),c("Student Email","Course Name", "Absent","Late","Present","Percent Present"))),stringsAsFactors = F)

for(i in o){
  nor<-acaData[which(acaData$EmailAddress==i),]
  s<-unique(nor$ClassCode)
  abs=late=pres=0
  finAbs=finLate=finPres=0
  attenTotal[dim(attenTotal)[1]+1,] =matrix(c(i," "," ",0," ",0," ",0,0))
  #print s
  for (k in s){
    print(paste("For class ",k,"the attendance of ",i," is :"))
    thor<-nor[which(nor$ClassCode==k),]
    m <- count(thor,'Attendance')
    print(m)
    attenTotal[dim(attenTotal)[1],2]=as.character(thor$AcademicYear[1])
    len <- dim(m)[1]
    if(len==3){
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

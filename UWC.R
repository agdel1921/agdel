if(!require(openxlsx)) {
  install.packages("openxlsx"); require(openxlsx)}
if(!require(ggplot2)) {
  install.packages("ggplot2"); require(ggplot2)}
if(!require(Hmisc)) {
  install.packages("Hmisc"); require(Hmisc)}
if(!require(corrplot)) {
  install.packages("corrplot"); require(corrplot)}
 
# load the 4 different sheets in the Academic Data Workbook
# each sheet represents a different time period
acaData <- read.xlsx("D:\\Data Sets\\UWC\\AcademicData_vdNum.xlsx", sheet = 4)
acaData2 <- read.xlsx("D:\\Data Sets\\UWC\\AcademicData_vdNum.xlsx", sheet = 8)
acaData3 <- read.xlsx("D:\\Data Sets\\UWC\\AcademicData_vdNum.xlsx", sheet = 9)
acaData4 <- read.xlsx("D:\\Data Sets\\UWC\\AcademicData_vdNum.xlsx", sheet = 10)

# load the Student Basic Bio Info
bio <- read.xlsx("D:\\Data Sets\\UWC\\Student Baisc Bio Info.xlsx")

# load the Subject Teaching Info
teachData <- read.xlsx("D:\\Data Sets\\UWC\\Subject Teaching Group Info.xlsx")

# load the Student Survey 
survey <- read.xlsx("D:\\Data Sets\\UWC\\Student Survey.xlsx")

rcorr(as.matrix(acaData))

m1 <- as.data.frame(acaData)

t1 <- subset(m1, m1$ModuleId!="TOK")

pairs(~acaData$Campus.Code+acaData$`Ass1:.Att.Grades`,data=acaData, main="Simple Scatter Plot")

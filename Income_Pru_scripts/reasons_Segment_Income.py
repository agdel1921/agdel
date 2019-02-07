# -*- coding: utf-8 -*-
"""
Created on Sun Dec 23 21:56:19 2018

@author: LatizeExpress
"""
import pandas as pd
import numpy as np

pathread =  "E:/NTUC/raw_data/Final/hh_result_final/FinalResults_with_Bucket/"
pathwrite1 =  "E:/NTUC/raw_data/Results/Data_2016/"
pathwrite2 =  "E:/NTUC/raw_data/Results/Recommendation/"
#path_income = "E:/NTUC/raw_data/HOUSE_HOLD_FINAL/hh_Affluence_final_weight_bUCKETS/hh_Affluence_final_weight_bUCKETS/"

#data = pd.read_csv(pathwrite+'training_recom1_final.csv', low_memory = True)
#data.columns
#data.head()
segDf = pd.read_csv(pathread + 'MicroSegmentProfile_final.csv', low_memory = True)

#resultDF = pd.read_csv(pathread + 'result_reason_final.csv', low_memory = True)

segDf.columns

#resultDF.columns

#segDf['reasons'] = segDf['PremiumCategory'].map(str) + ', Active Members: ' + segDf['membersactive'].map(str) + ', AgeGroup: ' + segDf['AgeGroup'].map(str)+ ', totalkids: ' + segDf['totalkids'].map(str) + ', maritalstatus: ' + segDf['LifeStageBucket'].map(str)+ ', LifeStage: ' + segDf['maritalstatus'].map(str)

#resultDF['reasons'] = segDf['reasons']

segDf['reason1'] = 'Premium Category:' + segDf['PremiumCategory'].map(str)
segDf['reason2'] = 'Education Level:' + segDf['EducationLevel'].map(str)
segDf['reason3'] = 'LifeStage:' + segDf['LifeStageBucket'].map(str)
segDf['reason4'] = 'Affluence Status:' + segDf['Affluence_Bucket'].map(str)
segDf['reason5'] = 'Dwelling Type:' + segDf['DwellingTypeCategory'].map(str)

segDf.to_csv(pathread + 'result_reason.csv', header = True, index = False)
segDf1 = segDf[['hid','MicroSegmentProfile','reason1', 'reason2', 'reason3','reason4', 'reason5']]


#### Attaching reasons to the final summary file

#resultDF_sum = pd.read_csv(pathwrite2 + 'unique_accuracy_181221_nohealth_testing.csv', low_memory = True)
resultDF_sum = pd.read_csv(pathread + 'Final_1000_All.csv', low_memory = True)
segDf1.columns

resultDF_sum.columns
#
#segDf['reasons'] = segDf['PremiumCategory'].map(str) + ', Active Members: ' + segDf['membersactive'].map(str) + ', AgeGroup: ' + segDf['AgeGroup'].map(str)+ ', totalkids: ' + segDf['totalkids'].map(str) + ', maritalstatus: ' + segDf['LifeStageBucket'].map(str)+ ', LifeStage: ' + segDf['maritalstatus'].map(str)

#resultDF_sum['reasons'] = segDf['reasons']
#resultDF_sum['reason1'] = 'Premium Category:' + segDf['PremiumCategory'].map(str)
#resultDF_sum['reason2'] = segDf['AgeGroup'].map(str)
#resultDF_sum['reason3'] = segDf['LifeStageBucket'].map(str)
#resultDF_sum['reason4'] = 'Status:' + segDf['Affluence_Bucket'].map(str)
#resultDF_sum['reason5'] = 'totalkids:' + segDf['totalkids'].map(str)
#resultDF_sum['Segment'] = segDf['MicroSegmentProfile'].map(str)

resultDF_sum = resultDF_sum.merge(segDf1, on = 'hid', how = 'left')
prop_income = pd.read_csv(pathwrite1+'proposed_income.csv', low_memory = True)
resultDF_sum = resultDF_sum.merge(prop_income, on = 'hid', how = 'left')
#resultDF_sum = resultDF_sum.drop(resultDF_sum['Proposed_Annual_Income'], axis = 1)
#resultDF_sum1 = resultDF_sum.merge(data, on = 'hid', how = 'left')
resultDF_sum.columns
resultDF_sum.to_csv(pathread + 'CF_Final_Result_To_Income_all.csv', header = True, index = False)
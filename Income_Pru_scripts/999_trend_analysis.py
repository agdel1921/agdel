# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 12:38:34 2017

@author: ashutosh.gaur and vsdaking
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import seaborn as sns
import datetime

pathInp_ptv = "C:/data/170809_ptv/ptv_only_og_data/"
pathOp_ptv = "C:/data/170809_ptv/output_ptv/"

os.chdir(pathInp_ptv)

def c_period(df):
    df['Cohort_Period'] = np.arange(len(df)) + 1
    print df['Cohort_Period']
    return df

def c_analysis():
    for fls_ptv in os.listdir(pathInp_ptv):
        if fls_ptv[fls_ptv.find("_20")+1:fls_ptv.find(".csv")]>"2011":
            if fls_ptv.find("_20") != -1:
                print fls_ptv
                inpDf = pd.read_csv(pathInp_ptv+fls_ptv, header = 0)
                
                ### Determine the user's period column based on Update Period
                inpDf['UpdatePeriod'] = inpDf.statdate.apply(lambda x: str(x)[:4]+"-"+str(x)[4:6])
                inpDf.head()
                
                ## attempt to remove all Policies which have not been modified beyond their inception date
                ## bad idea - removing it does not give us an idea of how many total policies were created in that given month
                ## stupid attempt by vd
                ## leaving this here for Future Data person to understand/ :)
                # inpDf = inpDf[inpDf['statdate'] != inpDf['occdate']]
                
                inpDf_updatesOnly = inpDf[inpDf['statdate'] != inpDf['occdate']]
                
                print "Original shape is",inpDf.shape
                print "Updates only shape is",inpDf_updatesOnly.shape
                
                ### Determine the user's Cohort / Group (based on occdate / date of policy inception)
                #inpDf.set_index('cownnum', inplace=True)
                inpDf['Cohort_Grp'] = inpDf.groupby(level = 0)['occdate'].min().apply(lambda  x: str(x)[:4]+"-"+str(x)[4:6])
                inpDf_updatesOnly['Cohort_Grp'] = inpDf_updatesOnly.groupby(level = 0)['occdate'].min().apply(lambda  x: str(x)[:4]+"-"+str(x)[4:6])
                
                ### Roll up the data by Cohort Group and Update Period
                grouped = inpDf.groupby(['Cohort_Grp','UpdatePeriod'])
                grouped_updatesOnly = inpDf_updatesOnly.groupby(['Cohort_Grp','UpdatePeriod'])
                
                # count the unique users, orders and total premium per Group + Period
                cohorts = grouped.agg({'cownnum':pd.Series.nunique,
                                       'chdrnum':pd.Series.nunique,
                                       'apicov':np.sum})
                
                cohorts_updatesOnly =  grouped_updatesOnly.agg({'cownnum':pd.Series.nunique,
                                       'chdrnum':pd.Series.nunique,
                                       'apicov':np.sum})
                
                # make the column names more meaningful
                cohorts.rename(columns = {'cownnum':'Total Users', 'chdrnum':'Total Orders'}, inplace=True)
                cohorts.head()
                cohorts_updatesOnly.rename(columns = {'cownnum':'Total Users', 'chdrnum':'Total Orders'}, inplace=True)
                cohorts_updatesOnly.head()
                
                #cohorts = cohorts.groupby(level = 0).apply(cohort_period)
                cohorts.head()
                
                ### Tests to ensure we have a correct implemention till now
                x = inpDf[(inpDf.Cohort_Grp == '2010-01') & (inpDf.UpdatePeriod == '2010-01')]
                y = cohorts.ix[('2010-01','2010-01')]
                assert(x['cownnum'].nunique() == y['Total Users'])
                assert(x['apicov'].sum() == y['apicov'])
                assert(x['chdrnum'].nunique() == y['Total Orders'])
                
                ### User Retention by Cohort Group
                
                # reindex the DataFrame
                cohorts.head(20)
                cohorts.reset_index(inplace=True)
                cohorts.set_index(['Cohort_Grp','UpdatePeriod'], inplace=True)
                cohorts_updatesOnly.head(20)
                cohorts_updatesOnly.reset_index(inplace=True)
                cohorts_updatesOnly.set_index(['Cohort_Grp','UpdatePeriod'], inplace=True)
                
                # create a Series holding the total size of Cohort Grp
                cohort_grp_size = cohorts['Total Users'].groupby(level = 0).first()
                cohort_grp_size.head()
                
                # create a Series holding the total size of Cohort Grp
                cohort_grp_size2 = cohorts['Total Users'].groupby(level = 0).sum()
                cohort_grp_size2.head()
                
                # below line simply helps better understand the impact of the command below that in turn
                cohorts['Total Users'].head()
                # unstacked cohorts : dividing the Total Users updated apicovs by cohort_grp_size
                cohorts['Total Users'].unstack(0).head()
                
                ## commented out the lines below for this was the original code - hereby assume that the first month's value is the total number of purchases made
                ## this assumption is wrong as there may not be updates to every policy in the month they are created
                #user_retention = cohorts['Total Users'].unstack(0).divide(cohort_grp_size, axis = 1)
                #user_retention.head(10)
                
                user_retention = cohorts['Total Users'].unstack(0).divide(cohort_grp_size2, axis = 1)
                user_retention.head(10)
                
                user_retention_updatesOnly = cohorts_updatesOnly['Total Users'].unstack(0).divide(cohort_grp_size2, axis = 1)
                user_retention_updatesOnly.head(10)
                """
                user_retention.plot(figsize = (60,10))
                plt.title('Cohorts: Policy Updates')
                #plt.xticks(1,60,5)
                plt.xlim(1,60)
                plt.ylabel('% of Cohort Updates')
                """
                
                user_retention_updatesOnly.plot(figsize = (60,10))
                plt.title('Update Cohorts Only : Policy Updates')
                #plt.xticks(1,60,5)
                plt.xlim(1,60)
                plt.ylabel('% of Cohort Updates')
                plt.savefig(pathOp_ptv+"user_update_chart__"+fls_ptv[:-4]+"_"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".png")
                
                
                """
                sns.set(style='white')
                plt.figure(figsize = (60,60))
                plt.title('Cohorts: Policy Updates')
                user_retention.to_csv("user_retention.csv", header = True, index = True)
                sns.heatmap(user_retention.T, annot = True, fmt = '.0%', linewidths = .5)
                """
                
                sns.set(style='white')
                plt.figure(figsize = (60,60))
                plt.title('Updates Cohorts: Policy Updates')
                user_retention_updatesOnly.to_csv("user_retention_updates.csv", header = True, index = True)
                sns.heatmap(user_retention_updatesOnly.T, annot = True, fmt = '.0%', linewidths = .5)
                plt.savefig(pathOp_ptv+"user_update_cohort_plot__"+fls_ptv[:-4]+"_"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".png")

if __name__ == "__main__":
    c_analysis()
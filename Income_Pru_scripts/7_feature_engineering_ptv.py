# -*- coding: utf-8 -*-
"""
Created on Thu Sep 07 17:48:52 2017

@author: ashutosh.gaur and vd
"""

import os
import pandas as pd
import numpy as np

pathInp_ptv = "C:/PTV/Data_Phase2/initial_data/tmp/"

os.chdir(pathInp_ptv)

def readData():
    pd2 =  pd.read_csv(pathInp_ptv+"ptvbase_w_seller.csv", header = 0)
    #pd2 =  pd.read_csv(pathInp_ptv+"ptv_w_sel_cust_2017.csv", header = 0)
    return pd2

def processFeatures(pd2):
    # convert pd to np for speed and memory
    pdVals = pd2.values
    ogAgnt_status = []
    servAgnt_status = []
    # determine the column nos of Original (OG) Agent & Servicing Agent [Agent Codes & Departure Dates]
    ogAgnt_pos = [k1 for k1 in range(len(pd2.columns)) if pd2.columns[k1]=="original_comm_agent"][0]
    ogAgnt_deptDatePos = [k2 for k2 in range(len(pd2.columns)) if pd2.columns[k2]=="ori_agent_dtetrm"][0]
    servAgnt_pos = [k3 for k3 in range(len(pd2.columns)) if pd2.columns[k3]=="agntnum"][0]
    servAgnt_deptDatePos = [k4 for k4 in range(len(pd2.columns)) if pd2.columns[k4]=="servicing_agent_dtetrm"][0]
    
    statCode_pos = [k5 for k5 in range(len(pd2.columns)) if pd2.columns[k5]=="statcode"][0]
    
    # extract the specific fields for speed
    ogAgnt_codes = pdVals[:,ogAgnt_pos]
    ogAgnt_deptDate = pdVals[:,ogAgnt_deptDatePos]
    servAgnt_codes = pdVals[:,servAgnt_pos]
    servAgnt_deptDate = pdVals[:,servAgnt_deptDatePos]
    
    pol_currentStatusCode = pdVals[:,statCode_pos]
    
    for k3 in range(pd2.shape[0]):
        if ogAgnt_codes[k3] == servAgnt_codes[k3]:
            if ogAgnt_deptDate[k3]==99999999:
                if pol_currentStatusCode[k3]=="IF":
                    ogAgnt_status.append("With Prudential & ongoing association")
                    servAgnt_status.append("With Prudential & ongoing association")
                else:
                    ogAgnt_status.append("With Prudential & associated till lapse")
                    servAgnt_status.append("With Prudential & associated till lapse")
            else:
                if pol_currentStatusCode[k3]=="IF":
                    ogAgnt_status.append("Departed, but still associated? Recheck!")
                    servAgnt_status.append("Departed, but still associated? Recheck!")
                else:
                    ogAgnt_status.append("Departed, but associated till lapse")
                    servAgnt_status.append("Departed, but associated till lapse")
        else:
            if pol_currentStatusCode[k3]=="IF":
                if servAgnt_deptDate[k3]==99999999:
                    servAgnt_status.append("With Prudential & ongoing association")
                else:
                    servAgnt_status.append("Departed, but still associated? Recheck!")
                if ogAgnt_deptDate[k3]==99999999:
                    ogAgnt_status.append("With Prudential but not associated anymore")
                else:
                    ogAgnt_status.append("Departed but not associated at end")
            else:
                if servAgnt_deptDate[k3]==99999999:
                    servAgnt_status.append("With Prudential & associated till lapse")
                else:
                    servAgnt_status.append("Departed, but associated till lapse")
                if ogAgnt_deptDate[k3]==99999999:
                    ogAgnt_status.append("With Prudential but not associated till lapse")
                else:
                    ogAgnt_status.append("Departed but not associated till lapse")
    
    ## END OF DETERMINING AGENT'S ASSOCIATION WITH POLICY ##
    
    # CREATE TWO LISTS - EACH CONSISTING OF ONLY 'ORIGINAL AGENT' AND 'SERVICING AGENT' ONLY #
    ogAgnt_lst = ['Original Agent' for k7 in range(pd2.shape[0])]
    servAgnt_lst = ['Servicing Agent' for k8 in range(pd2.shape[0])]
    
    # DETERMINE IF AGENT WAS PTO AGENT OR NOT#
    pto_agent = []
    pto_pos = [k7 for k7 in range(len(pd2.columns)) if pd2.columns[k7]=="PTO_policy"][0]
    ptoAgentCode_pos = [k8 for k8 in range(len(pd2.columns)) if pd2.columns[k8]=="PTO_agent"][0]
    pto_indicator = pdVals[:,pto_pos]
    ptoAgentNum = pdVals[:,ptoAgentCode_pos]
    for k9 in range(pd2.shape[0]):
        if pto_indicator[k9]=='Y':
            pto_agent.append('PTO')
            if ptoAgentNum[k9] == ogAgnt_codes[k9]:
                ogAgnt_lst[k9] = 'PTO + Original Agent'
            if ptoAgentNum[k9] == servAgnt_codes[k9]:
                servAgnt_lst[k9] = 'PTO + Servicing Agent'
        else:
            pto_agent.append('Other')
    # END #
    
    
    
    ## merging field back into matrix ##
    featuresPd = pd.DataFrame({'Original_agent_status':ogAgnt_status,'Servicing_agent_status':servAgnt_status, 'PTO_Agent':pto_agent, 'Original_agent_type':ogAgnt_lst, 'Servicing_agent_type':servAgnt_lst})
    newPd = pd.concat([pd2, featuresPd], axis=1)
    newPd.to_csv(pathInp_ptv+ "updated_ptv2.csv", header=True, index=False)

if __name__ == "__main__":
    inpPd = readData()
    processFeatures(inpPd)
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 11:32:30 2017

@author: ashutosh.gaur and vsdaking
"""

import os
import pandas as pd
import numpy as np

pathInp_prem20xx = "C:/PTV/Data_Phase2/"
pathOp_ptv = "C:/data/170809_ptv/ptv_only_og_data/"

os.chdir(pathInp_prem20xx)

def extractPtv_from2010():
    for fls in os.listdir(pathInp_prem20xx):
        if fls[-4:]==".csv":
            if fls[:fls.find(".csv")-2]=="premium20":
                # above check can also be fls[:-6]. chose the above option for ease of future understanding. :)
                inpPd = pd.read_csv(pathInp_prem20xx+fls, header = 0)
                if "cnttype" not in inpPd.columns:
                    if fls=="premium2010.csv":
                        ptvPd = inpPd[inpPd["prdtgrp"].isin(['PruTerm'])]
                    elif fls =="premium2011.csv":
                        ptvPd = inpPd[inpPd["prdtgrp"].isin(['PruTerm Vantage', 'PruTerm'])]
                else:
                    ptvPd = inpPd[inpPd["cnttype"].isin(['LT4','LU4'])]
                ptvPd = ptvPd[ptvPd["occdate"]>20091231]
                destName = "ptv_"+fls[fls.find("20"):]
                ptvPd.to_csv(pathOp_ptv+destName, header=True, index=False)

if __name__ == "__main__":
    extractPtv_from2010()
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 15:36:01 2017

@author: ashutosh.gaur
"""

### AIM : remove the various blank lines in the conceptual model & quickly

import os
import numpy as np
import pandas as pd

pathInp = "C:/ontology/Conceptual_Model/"

for fls in os.listdir(pathInp):
    conceptPd = pd.read_csv(pathInp + fls, header = 0)
    print conceptPd.shape
    conceptPd.to_csv(pathInp + fls[:-4]+"_v2.csv", header = True, index = False)
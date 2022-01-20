#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 16:45:07 2017

@author: deemsj
"""

########################
#rpy2
import rpy2
from rpy2.robjects.packages import importr
from rpy2.robjects import FloatVector

base = importr('base')
utils = importr('utils')
stats = importr('stats')
segmented = importr('segmented')

utils.chooseCRANmirror(ind=1) # select the first mirror in the list

# install segmented
utils.install_packages('segmented')

#remember to run the loglags lines in vario_utils.py
loglags_r = FloatVector(loglags)
logmeans_r = FloatVector(logmeans)
rpy2.robjects.globalenv["loglags_r"] = loglags_r
rpy2.robjects.globalenv["logmeans_r"] = logmeans_r

lm_vario_init = stats.lm("logmeans_r ~ loglags_r")
print(stats.anova(lm_vario_init))

# omitting the intercept
lm_vario_init = stats.lm("logmeans_r ~ loglags_r - 1")
print(base.summary(lm_vario_init))

print(lm_vario_init.rx2('coefficients'))

rsegmented = rpy2.robjects.r['segmented']
lm_seg_vario = rsegmented(lm_vario_init,20)

#build initial linear regression
    
#call segmented
    
#report coefficients and statistics

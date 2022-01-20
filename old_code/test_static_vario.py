#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 08:21:48 2017

@author: deemsj

Dependencies:
    piecewise:
        https://www.datadoghq.com/blog/engineering/piecewise-regression/
        https://github.com/DataDog/piecewise
"""
#import pickle
import numpy as np
import pandas as pd

from piecewise.regressor import piecewise
from piecewise.plotter import plot_data_with_regression

#plotters
import seaborn as sns
sns.set()


def test_static_vario(var, circle, lag_s=3, lag_f=94, min_stop_frac=0.03):
    filename = '/Users/deemsj/Documents/tuol_vario/regional_variograms_v8/snowoff/' + var + '.pickle'
    print(filename)
    with open(filename, 'rb') as f:
        test_static_vario = pd.read_pickle(f)

#    if np.any(np.isnan(test_static_vario['vario_dfs'][i].gamma[lag_s:lag_f])):
#        nanlist = [i for i,x in enumerate(np.isnan(test_static_vario['vario_dfs'][i].gamma[lag_s:lag_f])) if x==True]
#        nancount = sum(np.isnan(test_static_vario['vario_dfs'][i].gamma[lag_s:lag_f]))
#        print(str(nancount) + ' nans in variogram at lag number(s)' + str(nanlist))
#        #print(test_vario['mean'][circle][6:94])

    #find the circle value in the circle_ids list; return index value
#    for i, j in enumerate(test_sd_vario['circle_ids']):
#        if j == circle:
#            break
    i = test_static_vario['circle_ids'].index(circle)
    loglags = np.log10(test_static_vario['vario_dfs'][i].dist[lag_s:lag_f])
    logmeans = np.log10(test_static_vario['vario_dfs'][i].gamma[lag_s:lag_f])
    print(var)

    model = piecewise(loglags,logmeans,min_stop_frac)
#    srD = 3 - model.segments[0].coeffs[1] / 2
#    #calc scale break distance in meters
#    SBdist = 10 ** ((model.segments[1].coeffs[0] - model.segments[0].coeffs[0]) / (model.segments[0].coeffs[1] - model.segments[1].coeffs[1]))
#    #calc long range fractal dimension
#    lrD = 3 - model.segments[1].coeffs[1] / 2
#    print(srD, SBdist, lrD)

    plot_data_with_regression(loglags,logmeans,min_stop_frac)
    return model

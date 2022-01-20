#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 08:21:48 2017

@author: deemsj
"""
#import pickle
import numpy as np
import pandas as pd

from piecewise.regressor import piecewise
from piecewise.plotter import plot_data_with_regression

#plotters
import seaborn as sns
sns.set()


def test_sd_vario(version, date, circle, lag_s=6, lag_f=94, min_stop_frac=0.03):
    filename = '/Users/deemsj/Documents/tuol_vario/regional_variograms_v' + str(version) + '/snow_depth/' + str(date) + '_snow_depth.pickle'
    with open(filename, 'rb') as f:
        test_sd_vario = pd.read_pickle(f)

#test for nans - seems to not be necessary with new variogram routine
#    if np.any(np.isnan(test_sd_vario['vario_dfs'][circle].gamma[lag_s:lag_f])):
#        nancount = sum(np.isnan(test_sd_vario['vario_dfs'][circle].gamma[lag_s:lag_f]))
#        print(str(nancount) + ' nans in variogram')
    try:
        i = test_sd_vario['circle_ids'].index(circle)
    except:
        print('Circle number has no snow on this date')

    loglags = np.log10(test_sd_vario['vario_dfs'][i].dist[lag_s:lag_f])
    logmeans = np.log10(test_sd_vario['vario_dfs'][i].gamma[lag_s:lag_f])

    model = piecewise(loglags,logmeans,min_stop_frac)
    srD = 3 - model.segments[0].coeffs[1] / 2
    #calc scale break distance in meters
    SBdist = 10 ** ((model.segments[1].coeffs[0] - model.segments[0].coeffs[0]) / (model.segments[0].coeffs[1] - model.segments[1].coeffs[1]))
    #calc long range fractal dimension
    lrD = 3 - model.segments[1].coeffs[1] / 2
    print(srD, SBdist, lrD)
    plot_data_with_regression(loglags,logmeans,min_stop_frac)

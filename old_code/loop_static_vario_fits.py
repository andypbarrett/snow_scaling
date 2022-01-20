#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 19:24:33 2017

@author: deemsj

wrapper scripting:
- loop through all static physiographic variables
- for each static variable, loop through all circles
- call variogram piecewise fitting routine
- build/append structure for D, SB values per sample circle
"""
#import pickle
import csv
import numpy as np
import pandas as pd
from piecewise.regressor import piecewise

rootpathname = '/Users/deemsj/Documents/tuol_vario/regional_variograms_v8/snowoff/'
varlist = open(rootpathname + 'varlist.txt').read().splitlines()
lagwindow = [2, 84]
print_summary = True

for var in varlist:  #loop over all static variables
    picklename = var + '.pickle'
    with open(rootpathname + picklename, 'rb') as f:
        static_vario = pd.read_pickle(f)
    #open output file for this flight
    outfile = open(rootpathname + var + '_static_vario_fit.txt', 'w')
    writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
    #write column headers
    writer.writerow(('circle_id', var + '_srD', var + '_SBdist', var + '_lrD'))
    #loop over all circles
    for i, circle_id in enumerate(static_vario['circle_ids']):
        try:
            #check for nans
            if np.any(np.isnan(static_vario['vario_dfs'][i].gamma[lagwindow[0]:lagwindow[1]])):
                print('nan in variogram at circle ' + str(i) + ' in ' + var)
                continue
            elif circle_id==1555:  #1555 is 100% reservoir
                continue

            #log the variogram lags; trimming the first few and last few bins
            loglags = np.log10(static_vario['vario_dfs'][i].dist[lagwindow[0]:lagwindow[1]])
            #log the variogram means in the current circle
            logmeans = np.log10(static_vario['vario_dfs'][i].gamma[lagwindow[0]:lagwindow[1]])
            #fit the linear models and breakpoints
            model = piecewise(loglags, logmeans)
            #calc short range fractal dimension
            srD = 3 - model.segments[0].coeffs[1] / 2
            if len(model.segments) > 1:
                #calc scale break distance in meters
                SBdist = 10 ** ((model.segments[1].coeffs[0] - model.segments[0].coeffs[0]) / (model.segments[0].coeffs[1] - model.segments[1].coeffs[1]))
                #calc long range fractal dimension
                lrD = 3 - model.segments[1].coeffs[1] / 2
                #append values to output file
                writer.writerow((circle_id, srD, SBdist, lrD))
            else:
                writer.writerow((circle_id, srD))
            """
            note - probably faster to build a dict with all values, then dump to
            a file after this loop, to avioid file I/O on every loop step...
            """
        except ValueError:
            print(var, i, circle_id)
    outfile.close()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 19:24:33 2017

@author: deemsj

wrapper scripting:
- loop through all ASO tuolumne dates
- loop through all circles with snow on each date
- call variogram piecewise fitting routine
- build/append structure for D, SB values per sample circle
"""
#import pickle
import csv
import numpy as np
import pandas as pd
from piecewise.regressor import piecewise

#loop through all variogram pickles, open, parse/read, close
#load the pickles
rootpathname = '/Users/deemsj/Documents/tuol_vario/regional_variograms_v8/'
datelist = open(rootpathname + 'datelist.txt').read().splitlines()

#start, end lag bins defining analysis window
lagwindow = [2,84]

for date in datelist:  #loop over all flights
    picklename = 'snow_depth/' + date + '_snow_depth.pickle'
    with open(rootpathname + picklename, 'rb') as f:
        sd_vario = pd.read_pickle(f)
    #open output file for this flight
    outfile = open(rootpathname + 'snow_depth/' + date + 'sd_vario_fit.txt', 'wb')
    writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC, lineterminator=os.linesep)
    #write column headers
    writer.writerow(('circle_id', date + 'srD', date + 'SBdist', date + 'lrD'))
    #loop over all circles in flight
    for i, circle_id in enumerate(sd_vario['circle_ids']):
        try:
            #log the variogram lags; trimming to lag window
            loglags = np.log10(sd_vario['vario_dfs'][i].dist[lagwindow[0]:lagwindow[1]])
            #check for nans
            if np.any(np.isnan(sd_vario['vario_dfs'][i].gamma[lagwindow[0]:lagwindow[1]])):
                print('nan in variogram at circle ' + str(i) + ' on ' + str(date))
                continue
            elif circle_id==1555:  #1555 is 100% reservoir
                continue
            #log the variogram means in the current circle
            logmeans = np.log10(sd_vario['vario_dfs'][i].gamma[lagwindow[0]:lagwindow[1]])
            #fit the linear models and breakpoints
            model = piecewise(loglags, logmeans)
            #calc short range fractal dimension
            srD = 3 - model.segments[0].coeffs[1] / 2
            #calc scale break distance in meters
            SBdist = 10 ** ((model.segments[1].coeffs[0] - model.segments[0].coeffs[0]) / (model.segments[0].coeffs[1] - model.segments[1].coeffs[1]))
            #calc long range fractal dimension
            lrD = 3 - model.segments[1].coeffs[1] / 2
            #append values to output file
            writer.writerow((circle_id, srD, SBdist, lrD))
            """
            note - probably faster to build a dict with all values, then dump to
            a file after this loop, to avioid file I/O on every loop step...
            """
        except (ValueError, IndexError):
            print(date, i, circle_id)
    outfile.close()

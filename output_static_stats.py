#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 09:09:23 2017

@author: deemsj
"""

import pickle
import csv

rootpathname = '/Users/deemsj/Documents/tuol_vario/regional_variograms/snowoff/'
varlist = open(rootpathname + 'varlist.txt').read().splitlines()

for var in varlist:
    picklename = var + '.pickle'
    with open(rootpathname + picklename, 'rb') as f:
        static_vario = pickle.load(f)

    outfile = open(rootpathname + var + '_stats.txt', 'w')
    writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
    #write column headers
    writer.writerow(('circle_id', 'mean', 'sd'))
    #loop over all circles
    for i, circle_id in enumerate(static_vario['circle_ids']):
        mean = static_vario['summary_stats']['mean'][i]
        sd = static_vario['summary_stats']['sd'][i]
        writer.writerow((circle_id, mean, sd))

    outfile.close()



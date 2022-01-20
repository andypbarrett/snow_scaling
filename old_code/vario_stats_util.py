#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 13:09:51 2017

@author: deemsj
"""
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# %%
#filter_sd_vario_stats

rootpathname = '/Users/deemsj/Documents/tuol_vario/regional_variograms_v8/'
#inpath = rootpathname + 'snow_depth/reg_var_sd_v8/static_stats_vario_fits_v8.txt'
#outpath = rootpathname + 'snow_depth/reg_var_sd_v8/static_stats_vario_fits_v8_filtered.txt'
inpath = rootpathname + 'snow_depth/reg_var_sd_v8/sd_vario_fits_v8.txt'
outpath = rootpathname + 'snow_depth/reg_var_sd_v8/sd_vario_fits_v8_filtered.txt'

sd_vario_stats = pd.read_csv(inpath, index_col=0, parse_dates=True)

srDcols = [i for i in sd_vario_stats.columns if 'srD' in i]
srD = sd_vario_stats.filter(like='srD', axis=1)
srD[(srD > 3.0) | (srD < 2.0)] = -9999
sd_vario_stats[srDcols] = srD

lrDcols = [i for i in sd_vario_stats.columns if 'lrD' in i]
lrD = sd_vario_stats.filter(like='lrD', axis=1)
lrD[(lrD > 3.0) | (lrD < 2.0)] = -9999
sd_vario_stats[lrDcols] = srD

SBdistcols = [i for i in sd_vario_stats.columns if 'SBdist' in i]
SBdist = sd_vario_stats.filter(like='SBdist', axis=1)
SBdist[(SBdist > 100.0) | (SBdist < 2.0)] = -9999
sd_vario_stats[SBdistcols] = srD

sd_vario_stats.to_csv(outpath, quoting=csv.QUOTE_NONNUMERIC)

# %%

# filter values, NaNs
rootpathname = '/Users/deemsj/Documents/tuol_vario/regional_variograms_v8/'
#inpath = rootpathname + 'snow_depth/reg_var_sd_v8/static_stats_vario_fits_v8.txt'
#outpath = rootpathname + 'snow_depth/reg_var_sd_v8/static_stats_vario_fits_v8_filtered_nan.txt'
inpath = rootpathname + 'snow_depth/reg_var_sd_v8/sd_vario_fits_v8.txt'
outpath = rootpathname + 'snow_depth/reg_var_sd_v8/sd_vario_fits_v8_filtered_nan.txt'

sd_vario_stats = pd.read_csv(inpath, index_col=0, parse_dates=True)

srDcols = [i for i in sd_vario_stats.columns if 'srD' in i]
srD = sd_vario_stats.filter(like='srD', axis=1)
srD[(srD > 3.0) | (srD < 2.0)] = float('nan')
sd_vario_stats[srDcols] = srD

lrDcols = [i for i in sd_vario_stats.columns if 'lrD' in i]
lrD = sd_vario_stats.filter(like='lrD', axis=1)
lrD[(lrD > 3.0) | (lrD < 2.0)] = float('nan')
sd_vario_stats[lrDcols] = lrD

SBdistcols = [i for i in sd_vario_stats.columns if 'SBdist' in i]
SBdist = sd_vario_stats.filter(like='SBdist', axis=1)
SBdist[(SBdist > 100.0) | (SBdist < 2.0)] = float('nan')
sd_vario_stats[SBdistcols] = SBdist

mcols = [i for i in sd_vario_stats.columns if '_m' in i]
m = sd_vario_stats.filter(like='_m', axis=1)
m[m == -9999] = float('nan')
sd_vario_stats[mcols] = m

sdcols = [i for i in sd_vario_stats.columns if '_sd' in i]
sd = sd_vario_stats.filter(like='_sd', axis=1)
sd[sd == -9999] = float('nan')
sd_vario_stats[sdcols] = sd

sd_vario_stats.to_csv(outpath, quoting=csv.QUOTE_NONNUMERIC)


# %%
#plot_sd_vario_stats

rootpathname = '/Users/deemsj/Documents/tuol_vario/regional_variograms_v8/'
sdinpath = rootpathname + 'snow_depth/reg_var_sd_v8/static_stats_vario_fits_v8_filtered_nan.txt'
statinpath = rootpathname + 'snowoff/static_stats_vario_fits_v8_filtered_nan.txt'
figoutpath = '/Users/deemsj/Documents/tuol_vario/plots/'

sd_vario_stats = pd.read_csv(sdinpath, index_col=0, parse_dates=True)
srDcols = [i for i in sd_vario_stats.columns if 'srD' in i]
SBdistcols = [i for i in sd_vario_stats.columns if 'SBdist' in i]
lrDcols = [i for i in sd_vario_stats.columns if 'lrD' in i]
mcols = [i for i in sd_vario_stats.columns if 'cd_m' in i]
sdcols = [i for i in sd_vario_stats.columns if 'cd_sd' in i]


#plot_vars = ['dem_m','dem_sd','northness_m','tcurv_m','tpi_m','tpi_sd','vh_m','vh_sd']+SBdistcols[0:5]
#plot_vars = ['dem_m']+SBdistcols[0:5]
#plot_vars = ['vh_sd']+srDcols[0:5]


#sns.pairplot(sd_vario_stats, vars=plot_vars, dropna=True)

#plot srD vs SBdist for each date
for i, flight in enumerate(srDcols):
    fig1 = sd_vario_stats.plot.scatter(x=srDcols[i], y=SBdistcols[i])
    fig2 = fig1.get_figure()
    fig2.savefig(str(flight) +'_srDvsSBdist')
    plt.close(fig2)

#plot each static var vs SBdist for each date
for i, flight in enumerate(SBdistcols):
    for j, mvar in enumerate(mcols):
#        fig1 = sd_vario_stats.plot.scatter(x=mcols[j], y=SBdistcols[i])
        fig1 = sns.lmplot(x=mcols[j], y=SBdistcols[i], data=sd_vario_stats, robust=True)
#        fig1a = fig1.get_figure()
        fig1.savefig(figoutpath + str(flight) + '_' + mvar + '_vsSBdist')
#        plt.close(fig1a)
    for k, sdvar in enumerate(sdcols):
#        fig2 = sd_vario_stats.plot.scatter(x=sdcols[k], y=SBdistcols[i])
        fig2 = sns.lmplot(x=sdcols[k], y=SBdistcols[i], data=sd_vario_stats, robust=True)
#        fig2a = fig2.get_figure()
        fig2.savefig(figoutpath + str(flight) + '_' + sdvar + '_vsSBdist')
#        plt.close(fig2a)

g = sns.jointplot(x1, x2, kind="kde", size=7, space=0)
testfig = sns.jointplot(sd_vario_stats['cd_m'],sd_vario_stats['20170401srD'],kind="kde", size=7, space=0)

#plot each static var vs srD for each date
for i, flight in enumerate(srDcols):
    for j, mvar in enumerate(mcols):
#        fig1 = sd_vario_stats.plot.scatter(x=mcols[j], y=srDcols[i])
        fig1 = sns.lmplot(x=mcols[j], y=srDcols[i], data=sd_vario_stats, robust=True)
#        fig1a = fig1.get_figure()
        fig1.savefig(figoutpath + str(flight) + '_' + mvar + '_vssrD')
#        plt.close(fig1a)
    for k, sdvar in enumerate(sdcols):
#        fig2 = sd_vario_stats.plot.scatter(x=sdcols[k], y=srDcols[i])
        fig2 = sns.lmplot(x=sdcols[k], y=srDcols[i], data=sd_vario_stats, robust=True)
#        fig2a = fig2.get_figure()
        fig2.savefig(figoutpath + str(flight) + '_' + sdvar + '_vssrD')
#        plt.close(fig2a)

plt.close('all')
#%%

#plot static vario fits vs sd vario fits
rootpath = '/Users/deemsj/Documents/tuol_vario/regional_variograms_v8/snow_depth/reg_var_sd_v8/'
infile = rootpath + 'static_vario_fits_sd_vario_fits_v8_filtered_nan.txt'

figoutpath = '/Users/deemsj/Documents/tuol_vario/plots/'

all_vario_stats = pd.read_csv(infile, index_col=0, parse_dates=True)

kendallcorr = all_vario_stats.corr(method='kendall')
kendallcorr.to_csv(rootpath + 'static_variofits_vs_sd_variofits_KendallTau.txt', quoting=csv.QUOTE_NONNUMERIC)

srDcols = [i for i in all_vario_stats.columns if 'srD' in i]
SBdistcols = [i for i in all_vario_stats.columns if 'SBdist' in i]
lrDcols = [i for i in all_vario_stats.columns if 'lrD' in i]

#plot each static  SBdist vs SBdist for each date

for i, flight in enumerate(SBdistcols):
    for j, mvar in enumerate(mcols):
        fig1 = all_vario_stats.plot.scatter(x=mcols[j], y=SBdistcols[i])
        fig1a = fig1.get_figure()
        fig1a.savefig(figoutpath + str(flight) + '_' + mvar + '_vsSBdist')
        plt.close(fig1a)
    for k, sdvar in enumerate(sdcols):
        fig2 = all_vario_stats.plot.scatter(x=sdcols[k], y=SBdistcols[i])
        fig2a = fig2.get_figure()
        fig2a.savefig(figoutpath + str(flight) + '_' + sdvar + '_vsSBdist')
        plt.close(fig2a)

#plot each static var srD vs srD for each date
for i, flight in enumerate(srDcols):
    for j, mvar in enumerate(mcols):
        fig1 = all_vario_stats.plot.scatter(x=mcols[j], y=srDcols[i])
        fig1a = fig1.get_figure()
        fig1a.savefig(figoutpath + str(flight) + '_' + mvar + '_vssrD')
        plt.close(fig1a)
    for k, sdvar in enumerate(sdcols):
        fig2 = all_vario_stats.plot.scatter(x=sdcols[k], y=srDcols[i])
        fig2a = fig2.get_figure()
        fig2a.savefig(figoutpath + str(flight) + '_' + sdvar + '_vssrD')
        plt.close(fig2a)



#%%
#plot time series boxplots of srD by year
rootpathname = '/Users/deemsj/Documents/tuol_vario/regional_variograms_v8/'
inpath = rootpathname + 'snow_depth/reg_var_sd_v8/static_stats_vario_fits_v8_filtered_nan.txt'
figoutpath = '/Users/deemsj/Documents/tuol_vario/plots/'

sd_vario_stats = pd.read_csv(inpath, index_col=0, parse_dates=True)
srDcols = [i for i in sd_vario_stats.columns if 'srD' in i]
SBdistcols = [i for i in sd_vario_stats.columns if 'SBdist' in i]
lrDcols = [i for i in sd_vario_stats.columns if 'lrD' in i]
mcols = [i for i in sd_vario_stats.columns if '_m' in i]
sdcols = [i for i in sd_vario_stats.columns if '_sd' in i]

#plot time series boxplots of srD by year
ax1 = sd_vario_stats[srDcols].plot(kind='box', rot=90, figsize=(6,3))
fig1=ax1.get_figure()
fig1.set_size_inches(6,3)
fig1.savefig('test_boxplot_srD.eps', dpi=300)

ax2 = sd_vario_stats[SBdistcols].plot(kind='box', rot=90, figsize=(6,3))
fig2=ax2.get_figure()
fig2.set_size_inches(6,3)
fig2.savefig('test_boxplot_SBdist.eps', dpi=300)

#%%
#filter_static_vario fit_stats

rootpathname = '/Users/deemsj/Documents/tuol_vario/regional_variograms_v8/snowoff/'
infile = rootpathname + 'static_vario_fits_v8.txt'
outfile = rootpathname + 'static_vario_fits_v8_filtered.txt'

static_vario_stats = pd.read_csv(infile, index_col=0, parse_dates=True)

srDcols = [i for i in static_vario_stats.columns if 'srD' in i]
srD = static_vario_stats.filter(like='srD', axis=1)
srD[(srD > 3.0) | (srD < 2.0)] = -9999
static_vario_stats[srDcols] = srD

lrDcols = [i for i in static_vario_stats.columns if 'lrD' in i]
lrD = static_vario_stats.filter(like='lrD', axis=1)
lrD[(lrD > 3.0) | (lrD < 2.0)] = -9999
static_vario_stats[lrDcols] = lrD

SBdistcols = [i for i in static_vario_stats.columns if 'SBdist' in i]
SBdist = static_vario_stats.filter(like='SBdist', axis=1)
SBdist[(SBdist > 700.0) | (SBdist < 2.0)] = -9999
static_vario_stats[SBdistcols] = SBdist

static_vario_stats.to_csv(outfile, quoting=csv.QUOTE_NONNUMERIC)

# %%

# filter static vario fit values, NaNs
rootpathname = '/Users/deemsj/Documents/tuol_vario/regional_variograms_v8/snowoff/'
infile = rootpathname + 'static_vario_fits_v8.txt'
outfile = rootpathname + 'static_vario_fits_v8_filtered_nan.txt'

static_vario_stats = pd.read_csv(infile, index_col=0, parse_dates=True)

srDcols = [i for i in static_vario_stats.columns if 'srD' in i]
srD = static_vario_stats.filter(like='srD', axis=1)
srD[(srD > 3.0) | (srD < 2.0)] = float('nan')
static_vario_stats[srDcols] = srD

lrDcols = [i for i in static_vario_stats.columns if 'lrD' in i]
lrD = static_vario_stats.filter(like='lrD', axis=1)
lrD[(lrD > 3.0) | (lrD < 2.0)] = float('nan')
static_vario_stats[lrDcols] = lrD

SBdistcols = [i for i in static_vario_stats.columns if 'SBdist' in i]
SBdist = static_vario_stats.filter(like='SBdist', axis=1)
SBdist[(SBdist > 700.0) | (SBdist < 2.0)] = float('nan')
static_vario_stats[SBdistcols] = SBdist

static_vario_stats.to_csv(outfile, quoting=csv.QUOTE_NONNUMERIC)


#%%

#plot time series of variograms
import test_sd_vario

rootpathname = '/Users/deemsj/Documents/tuol_vario/regional_variograms_v8/snow_depth/reg_var_sd_v8/'
sdinfile = rootpathname + 'sd_vario_fits_v8_filtered_nan.txt'

datelistfile = '/Users/deemsj/Documents/tuol_vario/regional_variograms_v8/datelist.txt'
figoutpath = '/Users/deemsj/Documents/tuol_vario/plots/'

datelist = open(datelistfile).read().splitlines()
sd_vario_stats = pd.read_csv(sdinfile, index_col=0, parse_dates=True)

#nab all 2017 flights
flights2017 = [j for j in datelist if '2017' in j]
srD = [j for j in sd_vario_stats.columns if 'srD' in j]
SBdist = [k for k in sd_vario_stats.columns if 'SBdist' in k]

#extract columns for 2017, and for specific rows in 2017
srD2017 = [j for j in srD if '2017' in j]
SBdist2017 = [k for k in SBdist if '2017' in k]
srD100 = sd_vario_stats.loc[100,srD2017]
SBdist100 = sd_vario_stats.loc[100,SBdist2017]
srD785 = sd_vario_stats.loc[785,srD2017]
SBdist785 = sd_vario_stats.loc[785,SBdist2017]
srD2695 = sd_vario_stats.loc[2695,srD2017]
SBdist2695 = sd_vario_stats.loc[2695,SBdist2017]

test_sd_vario.test_sd_vario(8,20170303,785, lag_s=1, lag_f=84, min_stop_frac=0.03)
test_sd_vario.test_sd_vario(8,20170401,785, lag_s=1, lag_f=84, min_stop_frac=0.03)
test_sd_vario.test_sd_vario(8,20170502,785, lag_s=1, lag_f=84, min_stop_frac=0.03)
test_sd_vario.test_sd_vario(8,20170604,785, lag_s=1, lag_f=84, min_stop_frac=0.03)
test_sd_vario.test_sd_vario(8,20170709,785, lag_s=1, lag_f=84, min_stop_frac=0.03)
test_sd_vario.test_sd_vario(8,20170717,785, lag_s=1, lag_f=84, min_stop_frac=0.03)
test_sd_vario.test_sd_vario(8,20170727,785, lag_s=1, lag_f=84, min_stop_frac=0.03)
test_sd_vario.test_sd_vario(8,20170816,785, lag_s=1, lag_f=84, min_stop_frac=0.03)

srDcols = [i for i in sd_vario_stats.columns if 'srD' in i]
srDcols2017 = [i for i in srDcols if '2017' in i]
SBdistcols = [i for i in sd_vario_stats.columns if 'SBdist' in i]
SBdistcols2017 = [i for i in SBdistcols if '2017' in i]

plt.plot(datelist,sd_vario_stats[srDcols])
plt.plot.show()

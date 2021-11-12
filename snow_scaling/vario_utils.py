r# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#I/O and numbery stuff
#import pickle
import numpy as np
import scipy
import pandas as pd

#plotters
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


########################
#load pickles
with open('/Users/deemsj/Documents/tuol_vario/regional_variograms_v4/snow_depth/20130503_snow_depth.pickle', 'rb') as f:
    sd20130503 = pd.read_pickle(f)
with open('/Users/deemsj/Documents/tuol_vario/regional_variograms_v4/snow_depth/20160416_snow_depth.pickle', 'rb') as f:
    sd20160416 = pd.read_pickle(f);
with open('/Users/deemsj/Documents/tuol_vario/regional_variograms_v4/snow_depth/20160625_snow_depth.pickle', 'rb') as f:
    sd20160625 = pd.read_pickle(f);

with open('/Users/deemsj/Documents/tuol_vario/regional_variograms_v4/snow_depth/20160625_snow_depth.pickle', 'rb') as f:
    sd20130403 = pickle.load(f);


# log transforms
loglags = np.log10(sd20160326['vario_dfs'][0].dist[1:5][6:94]);
logmeans = np.log10(sd20160326['vario_dfs'][200].gamma[6:94]);

loglags = np.log10(sd20130403['lags'][6:94]);
logmeans = np.log10(sd20130403['mean'][346][6:94]);

loglags = np.log10(sd20160416['lags'][6:94]);
logmeans = np.log10(sd20160416['mean'][50][6:94]);

loglags = np.log10(sd20160625['lags'][6:94]);
logmeans = np.log10(sd20160625['mean'][50][6:94]);


########################
#plotting
plt.figure()
plt.loglog(sd20160326['lags'],sd20160326['mean'][50],'o')



"""
########################
piecewise fitting
"""


# %% piecewise git
"""
currently best functionality, but breakpoint not optimal in all cases, requiring solving for
intersection of segments; robustness of fit not certain...
https://www.datadoghq.com/blog/engineering/piecewise-regression/
https://github.com/DataDog/piecewise
"""
from piecewise.regressor import piecewise
from piecewise.plotter import plot_data_with_regression

model = piecewise(loglags,logmeans)
len(model.segments)
model.segments[0].coeffs

plot_data_with_regression(loglags,logmeans)


# %% PWLF
from pyearth import Earth
import pwlf

myPWLF = pwlf.piecewise_lin_fit(loglags,logmeans);

res = myPWLF.fit(2);

xHat = np.linspace(min(loglags), max(loglags), num=1000)
yHat = myPWLF.predict(xHat)



#py-earth - spline regression...
#***may not work unless basis functions can be constrained to be linear...
model = Earth('max_degree',1,'allow_linear',False)
model.fit(loglags,logmeans)
#Print the model
print(model.trace())
print(model.summary())

#Plot the model
y_hat = model.predict(loglags)
plt.figure()
plt.plot(loglags,logmeans,'r.')
plt.plot(loglags,y_hat,'b.')
plt.xlabel('log lags')
plt.ylabel('gamma')
plt.title('test fit')
plt.show()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 15:37:32 2017

@author: deemsj
"""


'''
Port of the R seg.lm.fit function.
'''

import statsmodels.api as sm
import numpy as np
import warnings
from copy import copy


class Lm_Seg(object):
    """
    """
    def __init__(self, x, y, brk):
        super(Lm_Seg, self).__init__()
        self.x = x
        self.y = y
        self.brk = brk

        # Make sure the starting break point is in range of the data
        if not (self.x > self.brk).any():
            raise ValueError("brk is outside the range.")

        # Check for nans, infs...
        if not np.isfinite(x).all():
            self.y = self.y[np.isfinite(self.x)]
            self.x = self.x[np.isfinite(self.x)]

        if not np.isfinite(y).all():
            self.x = self.x[np.isfinite(self.y)]
            self.y = self.y[np.isfinite(self.y)]

    def fit_model(self, tol=1e-3, iter_max=100, h_step=2.0, epsil_0=10,
                  constant=True, verbose=True):
        '''
        '''
        # Fit a normal linear model to the data
        if constant:
            x_const = sm.add_constant(self.x)
            model = sm.OLS(self.y, x_const)
        else:
            model = sm.OLS(self.y, self.x)
        init_lm = model.fit()

        if verbose:
            print init_lm.summary()

        epsil = epsil_0

        # Before we get into the loop, make sure that this was a bad fit
        if epsil_0 < tol:
            warnings.warning('Initial epsilon is smaller than tolerance. \
                             The tolerance should be set smaller.')
            return init_lm

        # Sum of residuals
        dev_0 = np.sum(init_lm.resid**2.)

        # Count
        it = 0
        h_it = 0

        # Now loop through and minimize the residuals by changing where the
        # breaking point is.
        while np.abs(epsil) > tol:
            U = (self.x - self.brk) * (self.x > self.brk)
            V = deriv_max(self.x, self.brk)

            X_all = np.vstack([self.x, U, V]).T
            if constant:
                X_all = sm.add_constant(X_all)

            model = sm.OLS(self.y, X_all)
            fit = model.fit()

            beta = fit.params[2]  # Get coef
            gamma = fit.params[3]  # Get coef

            # Adjust the break point
            new_brk = copy(self.brk)
            new_brk += (h_step * gamma) / beta

            # If the new break point is outside of the allowed range, reset
            # the step size to half of the original, then try stepping again
            if not (self.x > new_brk).any():
                while True:
                    h_step /= 2.0
                    new_brk += (h_step * gamma) / beta
                    h_it += 1
                    if (self.x > new_brk).any():
                        self.brk = new_brk
                        break
                    if h_it >= 5:
                        raise ValueError("Cannot find suitable step size. \
                                          Check number of breaks.")
            else:
                self.brk = new_brk

            dev_1 = np.sum(fit.resid**2.)

            epsil = (dev_1 - dev_0) / (dev_0 + 1e-3)

            dev_0 = dev_1

            if verbose:
                print "Iteration: %s/%s" % (it+1, iter_max)
                print fit.summary()
                print "Break Point: " + str(self.brk)
                print "Epsilon: " + str(epsil)

            it += 1

            if it > iter_max:
                warnings.warning("Max iterations reached. \
                                 Result may not be minimized.")
                break

        # With the break point hopefully found, do a final good fit
        U = (self.x - self.brk) * (self.x > self.brk)
        V = deriv_max(self.x, self.brk)

        X_all = np.vstack([self.x, U, V]).T
        X_all = sm.add_constant(X_all)

        model = sm.OLS(self.y, X_all)
        self.fit = model.fit()
        self._params = self.fit.params
        cov_matrix = self.fit.cov_params()
        self._errs = np.asarray([np.sqrt(cov_matrix[i, i])
                                 for i in range(cov_matrix.shape[0])])

        self.brk_err = brk_errs(fit.params, fit.cov_params())

        self.get_slopes()

        return self

    def model(self, x=None, model_return=False):
        p = self.params

        trans_pt = np.abs(self.x-self.brk).argmin()

        mod_eqn = lambda k: p[0] + p[1]*k*(k < self.brk) + \
            ((p[1]+p[2])*k + (-p[2])*k[trans_pt])*(k >= self.brk)

        if model_return or x is None:
            return mod_eqn

        return mod_eqn(x)

    def get_slopes(self):
        '''
        '''
        n_slopes = self.params[1:-2].shape[0]
        self._slopes = np.empty(n_slopes)
        self._slope_errs = np.empty(n_slopes)

        for s in range(n_slopes):
            if s == 0:
                self._slopes[s] = self.params[s+1]
                self._slope_errs[s] = self.param_errs[s+1]
            else:
                self._slopes[s] = self.params[s+1] + self._slopes[:s]
                self._slope_errs[s] = \
                    np.sqrt(self.param_errs[s+1]**2 + self._slope_errs[:s]**2)

        return self

    @property
    def slopes(self):
        return self._slopes

    @property
    def slope_errs(self):
        return self._slope_errs

    @property
    def params(self):
        return np.append(self._params, self.brk)

    @property
    def param_errs(self):
        return np.append(self._errs, self.brk_err)

    def plot(self, x, show_data=True):
        '''
        '''
        import matplotlib.pyplot as p

        if show_data:
            p.plot(self.x, self.y, 'bD')

        p.plot(x, self.model(x), 'g')

        p.grid(True)

        p.show()


def deriv_max(a, b, pow=1):
    if pow == 1:
        dum = -1 * np.ones(a.shape)
        dum[a < b] = 0
        return dum
    else:
        return -pow * np.max(a - b, axis=0) ** (pow-1)


def brk_errs(params, cov):
    '''
    Given the covariance matrix of the fits, calculate the standard
    error on the break.
    '''

    # Var gamma
    term1 = cov[3, 3]

    # Var beta * (beta/gamma)^2`
    term2 = cov[2, 2] * (params[3]/params[2])**2.

    # Correlation b/w gamma and beta
    term3 = 2 * cov[3, 2] * (params[3]/params[2])

return np.sqrt(term1 + term2 + term3)
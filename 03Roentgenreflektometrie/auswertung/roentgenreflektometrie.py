
# coding: utf-8

# In[204]:

# ==================================================
# 	import modules
# ==================================================

import sys
import os

import inspect

# calc with uncertainties and arrays of uncertainties [[val, std], ...]
import uncertainties as uc
import uncertainties.unumpy as unp

# calc with arrays
import numpy as np
import pandas as pd

# plot engine
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider, Button
from matplotlib import rc

# for fitting curves
from scipy import optimize

# constants
import scipy.constants as const

font = {'size'   : 18,}
#        'weight' : 'bold'}
rc('font', **font)


# In[205]:

def show(var):
    '''
    print equations with matplotlib
    '''
    
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    var_name = [
        var_name for var_name,
        var_val in callers_local_vars if var_val is var
    ]
    var_format = " VARIABLE: {} ".format(var_name[0])
    print("{:=^50}".format(var_format))

    if isinstance(var, (int, float, uc.UFloat)):
        print("{} = {}".format(var_name[0], var))
    else:
        print(var)

    print("")  # newline


# In[206]:

def print_tex(s):
    assert isinstance(s, str)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.axis('off')
    ax.text(0.0, 0.5,
            s.replace('\t', ' ').replace('\n', ' ').replace('%', ''),
            color='k', size='x-large'
            )
    plt.show()


# # Beginn Auswertung 

# In[207]:

daten = pd.read_csv("../daten/unt.dat",
                    header=None,
                    skipinitialspace=True,
                    sep=' ',
                    names=['angle','diffuse'],
                    index_col='angle',
                   )
daten_diff = pd.read_csv("../daten/ref.dat",
                    header=None,
                    skipinitialspace=True,
                    sep=' ',
                    names=['angle','reflection'],
                    index_col='angle',
                   )

daten = pd.concat([daten, daten_diff], axis=1)
daten['difference'] = daten.reflection - daten.diffuse
daten.head()


# #                                Aufgabe 8                                

# In[208]:

# ==================================================
# 	Diffusen Scan von Reflektivitätsscan
# 	abziehen
# ==================================================

fig = plt.figure(figsize=(19.2,10.8))
ax = fig.add_subplot(111)

daten['reflection'].plot(
    ax=ax,
    color='r',
    linestyle='none',
    marker='+',
    markersize=6,
    label='Reflektivitätsscan'
)

daten['diffuse'].plot(
    ax=ax,
    color='b',
    linestyle='none',
    marker='o',
    markersize=4,
    label='Diffuser Scan'
)

ax.set_xlabel(r'$\alpha$ in Grad')
ax.set_ylabel(r'Intensität')
ax.set_xlim((0,4))
ax.semilogy()
ax.legend(loc='best')

ax.grid()
fig.tight_layout()
fig.savefig("../tex/bilder/data.pdf")
plt.show()


# # ==================================================
# # 	Geometriewinkel
# # ==================================================

# In[209]:

def Geom(a):
    return D*np.sin(np.deg2rad(a))/d0

d0 = 0.1  # mm
D = 30  # mm

alpha_g = np.arcsin(d0/D)
alpha_g_deg = np.rad2deg(alpha_g)

show(alpha_g_deg)


# In[210]:

daten['geom'] = Geom(theta_rho)
daten['geom'][daten.index.values >= alpha_g_deg] = 1
daten['geom'][0] = np.nan
daten['corrected'] = daten['difference']/daten['geom']
daten.head()


# In[211]:

# ===== Plot =======================================
fig = plt.figure(figsize=(19.2,10.8))
ax = fig.add_subplot(111)

daten['corrected'].plot(
    ax=ax,
    color='r',
    linestyle='none',
    marker='+',
    markersize=6,
    label='Mit Geometriefaktor'
)

daten['difference'].plot(
    ax=ax,
    color='b',
    linestyle='none',
    marker='o',
    markersize=4,
    label='Ohne Geometriefaktor'
)

ax.set_xlabel(r'$\alpha$ in Grad')
ax.set_ylabel(r'Intensität')
ax.semilogy()
ax.set_xlim((0,1))
ax.legend(loc='best')
ax.grid()

fig.tight_layout()
fig.savefig("../tex/bilder/geometriefaktor.pdf")

plt.show()


# In[212]:

# ==================================================
# 	Normierung
# ==================================================

norm = daten.query('angle > 0.06 & angle < 0.15').corrected.mean()
print(norm)
daten['normalized'] = daten['corrected']/norm


# ###########################################################################
# #                                Aufgabe 9                                #
# ###########################################################################

# In[219]:

# ==================================================
# 	Fit
# ==================================================

def k_z(j, n, k, a):
    Return = k*np.sqrt(n[j]**2 - np.cos(a)**2)
    return Return


def r_sig(j, n, k, a, sig):
    k_j = k_z(j, n, k, a)
    k_j1 = k_z(j+1, n, k, a)
    divident = k_j - k_j1
    divisor = k_j + k_j1
    exponent = -2.0*k_j*k_j1*sig**2

    return divident / divisor * np.exp(exponent)


def X_sig_fit(X, z2, n2, n3, sig1, sig2):
    a, j = X
    z = [0.0, z2]
    n = [1.0, n2, n3]
    sig = [sig1, sig2]

    if j == 2:
        return 0
    else:
        e_plus = np.exp(2*1j*k_z(j, n, k, a)*z[j])
        e_minus = np.exp(-2*1j*k_z(j, n, k, a)*z[j])
        divident = (
            r_sig(j, n, k, a, sig[j]) +
            X_sig_fit((a, j+1), z2, n2, n3, sig1, sig2)*e_plus
        )
        divisor = (
            1.0 + r_sig(j, n, k, a, sig[j]) *
            X_sig_fit((a, j+1), z2, n2, n3, sig1, sig2)*e_plus
        )

        return e_minus * divident / divisor


def X_sig_fit_squared(X, z2, n2, n3, sig1, sig2):
    return np.abs(X_sig_fit(X, z2, n2, n3, sig1, sig2))**2


k = 2.0*np.pi / 1.54e-10
z1 = 0.0
z2 = -209.8e-10
n1 = 1.0
n2 = 1.0 - 3.50 * 1e-06
n3 = 1.0 - 9.24 * 1e-06
sig1 = 4.78 * 1e-10
sig2 = 3.28 * 1e-10
n = [n2, n3]
z = [z1, z2]
sig = [sig1, sig2]

initialFit = X_sig_fit_squared(
            (theta_test_rad, 0),
            *values,
        )


values = [z2, n2, n3, sig1, sig2]

fit_data = daten.query('angle > 0.25 & angle < 1.3')
theta_fit = fit_data.index.values
psd3_fit = fit_data['normalized']
sigma_fit = len(theta_fit) * [0.00001]

val, cor = optimize.curve_fit(
    X_sig_fit_squared,
    (np.deg2rad(theta_fit), 0),
    psd3_fit,
    p0=[z2, n2, n3, sig1, sig2],
    maxfev=100000,
    sigma=sigma_fit
)

theta_plot = np.deg2rad(daten.index.values)
theta_test = np.linspace(0.1, 2.5, 200)
theta_test_rad = np.deg2rad(theta_test)


fig = plt.figure(figsize=(19.2,10.8))
ax = fig.add_subplot(111)

daten['normalized'].plot(
    ax=ax,
    color='k',
    linestyle='none',
    marker='+',
    markersize=4,
    label='Messwerte'
)

ax.semilogy(
    theta_test,
    initialFit,
    color='r',
    linestyle='-',
    label='Per Hand angepasst'
)
ax.semilogy(
    theta_test,
    X_sig_fit_squared(
        (theta_test_rad, 0),
         -2.10e-08,
        1-2.8e-06,
        1-7.2e-06,
        -5.5e-10,
        2.4e-10,
    ),
    color='b',
    linestyle='-',
    label='Fit'
)

#ax.semilogy()
ax.set_xlabel(r'$\alpha$ in Grad')
ax.set_ylabel(r'Intensität')

ax.grid()
ax.legend(loc='best')

fig.savefig('../tex/bilder/fit.pdf')
plt.show()


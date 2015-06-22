#!/usr/bin/python3
# -*- coding: utf-8 -*-

output_silent = False

import numpy as np
from scipy import optimize, interpolate, misc, stats, constants
import os
import sys
import re
import matplotlib.pyplot as plt
import scipy.optimize as optimization
import math
import matplotlib.cm as cm
import matplotlib.ticker as mtick

for arg in sys.argv:
    if(arg=='silent'):
        output_silent = True

#########################################
# Preparation				#
#########################################

def expo(x,A,Ea):
    return A*np.exp(-Ea*x/constants.Boltzmann)

path = './tauC_values'
temperature, T2, error = np.loadtxt(path, usecols=(0,1,2), unpack=True, comments='#')

fig = plt.figure()
ax = fig.add_subplot(111)

plt.errorbar(1/temperature, T2, yerr=np.sqrt(error), fmt="none", marker="o")
plt.plot(1/temperature, T2, marker="o",ms=3, ls="", label="Tau_C Werte")


var, cov = optimize.curve_fit(expo, 1/temperature, T2, p0=(2e-5,-2e-26), maxfev=10000)
xRef=np.linspace(0.009,0.011,100)
yRef=expo(xRef,var[0],var[1])
plt.plot(xRef,yRef,label="exponentieller Fit")

fOut=open("Ea.output","w")
tempVar=var[1]/constants.e
tempCov=np.sqrt(cov[1,1])/constants.e
tempString = str('%.2E' % tempVar)+"} \pm "+str('%.2E' % tempCov) +"}\n"
fOut.write("E_A = (" + tempString.replace("E","\\cdot 10^{")+") [eV]")
fOut.close()

plt.yticks(np.arange(10e-5, 10e-4, 0.001))
ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.grid()
plt.yscale("log")
plt.xlabel(r"Temperatur$^{-1} \left[\frac{1}{K}\right]$")
plt.ylabel(r"$\tau_C$ [s]")
plt.legend()
plt.title(r"$\tau_C$ Tieftemperatur F2")
plt.savefig('F2_Fit.pdf')

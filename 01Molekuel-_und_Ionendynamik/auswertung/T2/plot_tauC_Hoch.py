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



sys.exit()


for arg in sys.argv:
    if(arg=='silent'):
        output_silent = True

#########################################
# Preparation				#
#########################################

def expo(x,A,Ea):
    return A*np.exp(-Ea/x/constants.Boltzmann)

path = './T2_data'
temperature, T2, error = np.loadtxt(path, usecols=(0,1,2), unpack=True, comments='#')

plt.errorbar(1/temperature, T2, yerr=np.sqrt(error), fmt="none", marker="o")
plt.plot(1/temperature, T2, marker="o",ms=3, ls="", label=r"$\tau_C$ Werte")


var, cov = optimize.curve_fit(expo, 1/temperature, T2, p0=(2e-5,-2e-26), maxfev=10000)
xRef=np.linspace(0.002,0.004,100)
yRef=expo(xRef,var[0],var[1])
plt.plot(xRef,yRef,label="exponentieller Fit")

fOut=open("Ea.output","w")
fOut.write("E_A = ("+str('%.2E' % var[1])+" \pm "+str('%.2E' % cov[1,1]) + ") [J]")
fOut.close()

plt.xlim((2.5e-3,3.6e-3))
#plt.ylim((3.e-5,4e-5))
plt.yticks(np.arange(10e-5, 10e-4, 0.001))
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.grid()
plt.yscale("log")
plt.xlabel(r"Temperatur$^{-1} \left[\frac{1}{K}\right]$")
plt.ylabel(r"$\tau_C$")
plt.legend()
plt.title(r"$\tau_C$ Hochtemperatur $T_2$")
plt.savefig('T2_hochTemperaturPlot.pdf')

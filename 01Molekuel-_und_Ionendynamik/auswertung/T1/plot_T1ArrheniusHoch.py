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

for arg in sys.argv:
    if(arg=='silent'):
        output_silent = True

def quad(x,a,b,c):
    return (a*(x-b)**2+c)

#########################################
# Preparation				#
#########################################

path = './T1_valuesHoch'
table = np.loadtxt(path, usecols=(0,1,2), unpack=False, comments='#')
table=table[np.lexsort((table[:,1],table[:,2],table[:,0]))]
temperature, T1, error = (table[:,0],table[:,1],table[:,2])

plt.errorbar(1/temperature, T1, yerr=error, fmt="none", marker="o")
plt.plot(1/temperature, T1, marker="o", ls="", label="T1 Werte")

var, cov = optimize.curve_fit(quad, 1/temperature, T1, p0=(1,0,0.1), maxfev=100000)
xRef=np.linspace(0.002,0.004,100)
yRef=quad(xRef,var[0],var[1],var[2])
plt.plot(xRef,yRef,label="quadratischer Fit")


f=open("minimum.output","w")
tempString = "b = \\left("+str('%.2E' % var[1])+"} \pm "+str('%.2E' % np.sqrt(cov[1,1]))+"}\\right) \\left[\\frac{1}{K}\\right]"
f.write(tempString.replace("E","\\cdot 10^{"))
f.close()


plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.grid()
plt.yscale("log")
plt.xlabel(r"Temperatur$^{-1}$ $\left[\frac{1}{K}\right]$")
plt.ylabel("Zeit [s]")
#plt.xlim((96,110))
#plt.ylim((0.03,0.1))
plt.legend()
plt.title(r"Arrhenius Hochtemperatur $T_1$")
plt.savefig('T1_hochTemperaturPlot.pdf')

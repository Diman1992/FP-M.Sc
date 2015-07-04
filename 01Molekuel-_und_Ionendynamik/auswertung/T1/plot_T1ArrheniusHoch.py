#!/usr/bin/python3
# -*- coding: utf-8 -*-

output_silent = False

import numpy as np
from scipy import optimize, interpolate, misc, stats, constants
import os
import sys
import re
import matplotlib
import matplotlib.pyplot as plt
import scipy.optimize as optimization
import math
import matplotlib.cm as cm
import matplotlib.ticker as mtick

for arg in sys.argv:
    if(arg=='silent'):
        output_silent = True

def quad(x,a,b,c):
    return (a*(x-b)**2+c)

#########################################
# Preparation				#
#########################################

fig = plt.figure()
ax = fig.add_subplot(111)

ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))

path = './T1_valuesHoch'
table = np.loadtxt(path, usecols=(0,1,2), unpack=False, comments='#')
table=table[np.lexsort((table[:,1],table[:,2],table[:,0]))]
temperature, T1, error = (table[:,0],table[:,1],table[:,2])

plt.plot(1/temperature, T1, marker="o", ls="", color="black", label="T1 Werte")

var, cov = optimize.curve_fit(quad, 1/temperature, T1, p0=(1,0,0.1), maxfev=100000)
xRef=np.linspace(0.002,0.004,100)
yRef=quad(xRef,var[0],var[1],var[2])
plt.plot(xRef,yRef,color="black",label="quadratischer Fit")

ax.set_yscale('log')
ax.set_yticks([0.14, 0.16, 0.18,0.20,0.22,0.24,0.26])
ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())




plt.grid()
plt.xlabel(r"Temperatur$^{-1}$ $\left[\frac{1}{K}\right]$")
plt.ylabel("Zeit [s]")
plt.ylim((0.13,0.27))
plt.legend()
plt.title(r"Arrhenius Hochtemperatur $T_1$")
plt.tight_layout()
plt.savefig('T1_hochTemperaturPlot.pdf')


f=open("minimum.output","w")
tempString = "b = \\left("+str(round(var[1]*1e3,2))+" \pm "+str(round(np.sqrt(cov[1,1])*1e3,2))+"\\right) \\cdot 10^{-3}\ \\left[\\frac{1}{K}\\right]"
f.write(tempString.replace("E","\\cdot 10^{"))
f.close()

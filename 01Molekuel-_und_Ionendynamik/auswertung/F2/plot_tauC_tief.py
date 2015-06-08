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

#########################################
# Preparation				#
#########################################

def expo(x,A,Ea):
    return A*np.exp(-Ea*x/constants.Boltzmann)

path = './tauC_values'
temperature, T2, error = np.loadtxt(path, usecols=(0,1,2), unpack=True, comments='#')

plt.errorbar(1/temperature, T2, yerr=error, fmt="none", marker="o")
plt.plot(1/temperature, T2, marker="o",ms=3, ls="", label="Tau_C Werte")


var, cov = optimize.curve_fit(expo, 1/temperature, T2, p0=(2e-5,-2e-26), maxfev=10000)
xRef=np.linspace(0.009,0.011,100)
yRef=expo(xRef,var[0],var[1])
plt.plot(xRef,yRef,label="exponentieller Fit")

fOut=open("Ea.output","w")
fOut.write("E_A = "+str('%.2E' % var[1])+" \pm "+str('%.2E' % cov[1,1]))
fOut.close()

print("Ea: ",var[1])
print("A: ",var[0])
plt.yticks(np.arange(10e-5, 10e-4, 0.001))
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.grid()
plt.yscale("log")
plt.xlabel("1/Temperatur [1/K]")
plt.ylabel("Tau_C")
plt.legend()
plt.title("tauC Hochtemperatur F2")
plt.savefig('F2_hochTemperaturPlot.pdf')

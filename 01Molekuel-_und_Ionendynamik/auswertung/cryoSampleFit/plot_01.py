#!/usr/bin/python3
# -*- coding: utf-8 -*-

output_silent = False

import numpy as np
from scipy import optimize, interpolate, misc, stats, constants
import os
import sys
import matplotlib.pyplot as plt
import scipy.optimize as optimization
import math

for arg in sys.argv:
    if(arg=='silent'):
        output_silent = True

#########################################
# Preparation				#
#########################################

def p(var):
    print(var+" = "+'\n'+str(eval(var))+'\n')


cryo, sample = np.round(np.loadtxt('cryoSampleTemp', unpack=True, comments='#')/1000)


new_1=open("01_cryoFit:m","w")
new_2=open("01_cryoFit:b","w")




def f(x,m,b):
    return m*x+b
var, cov = optimize.curve_fit(f, cryo, sample, maxfev=100)
y = f(cryo, var[0],var[1])


new_1.write("m &= (")
new_1.write(str(round(var[0],3)))
new_1.write(" \pm ")
new_1.write(str(round(np.sqrt(cov[0,0]),3)))
new_1.write(")")
new_2.write("b &= (")
new_2.write(str(round(-1/var[0],3)))
new_2.write(" \pm ")
new_2.write(str(round(np.sqrt(cov[1,1]),3)))
new_2.write(")\,[\\text{K}]")

new_1.close()
new_2.close()

plt.scatter(cryo, sample, color="red", marker="+", s=70, label=r'Messwerte')
plt.plot(cryo, y, "b-", label=r'Linearer Fit')
plt.xlabel('Temperatur Kryostat T[K]')
plt.ylabel('Temperatur Probe T[K]')
plt.xlim((300,440))
plt.ylim((300,440))
#plt.ylabel(r"ln$\left( \frac{M_0-M_z}{2M_0} \right)$")
plt.grid()
plt.legend(loc='upper right')
plt.savefig('01_regressionTemp.pdf')

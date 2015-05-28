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

def lin(x,m,b):
    return m*x+b

def kohlrausch(x,T1,v):
    return np.exp(-(x/T1)**(1-v))

def p(var):
    print(var+" = "+'\n'+str(eval(var))+'\n')

def F2(path):
    time, amplitude, error = np.loadtxt(path, usecols=(0,5,6), unpack=True, comments='#')
    print(time)
    print(amplitude)
    #var, cov = optimize.curve_fit(kohlrausch, time, amplitude, maxfev=100)
    #plt.scatter(time,amplitude)
    #plt.show()

colors = iter(cm.jet(np.linspace(0, 1, 8)))

def T1(path,ax,temp):
    time, amplitude, error = np.loadtxt(path, usecols=(0,5,6), unpack=True, comments='#')
    print(time)
    print(amplitude)
    #var, cov = optimize.curve_fit(kohlrausch, time, amplitude, maxfev=100)
    ax.scatter(time,amplitude, color=next(colors),label=temp)


path='../_daten/tieftemperatur/'


figT1 = plt.figure()
axT1 = plt.gca()

for root, dirs, files in os.walk(path):
    options = root.split(sep="_")
    if len(options)>3:
        typ = options[3]
        temperature = options[4][:-1]
        print(typ,temperature)
        if(typ=="F2"):
            for f in files:
                if(f.endswith(".nmr")):
                    filePath = root+"/"+f
                    F2(filePath)
        if(typ=="T1"):
            for f in files:
                if(f.endswith(".nmr")):
                    filePath = root+"/"+f
                    T1(filePath,axT1,str(temperature))
            axT1.set_xscale('log')
            axT1.legend()
            #temperature = round(temperature * 0.922 - 1.085)

plt.show()

"""
new_1=open("01_cryoFit:m","w")
new_2=open("01_cryoFit:b","w")




y = f(cryo, var[0],var[1])


new_1.write("m = (")
new_1.write(str(round(var[0],3)))
new_1.write(" \pm ")
new_1.write(str(round(cov[0,0],3)))
new_1.write(")\,")
new_2.write("b = (")
new_2.write(str(round(-1/var[0],3)))
new_2.write(" \pm ")
new_2.write(str(round(1/(pow(var[0],2))*(cov[1,1]),3)))
new_2.write(")\,\\text{K}")

new_1.close()
new_2.close()

plt.scatter(cryo, sample, color="red", marker="+", s=70, label=r'Messwerte')
plt.plot(cryo, y, "b-", label=r'Linearer Fit')
plt.xlabel('T[K]')
plt.ylabel('T[K]')
#plt.ylabel(r"ln$\left( \frac{M_0-M_z}{2M_0} \right)$")
plt.grid()
plt.legend(loc='upper right')
plt.savefig('01_regressionTemp.pdf')
plt.show()
#plt.close()
"""

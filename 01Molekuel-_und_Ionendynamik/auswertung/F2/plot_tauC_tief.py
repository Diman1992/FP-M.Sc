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

def lin(x,m,b):
    return m*x+b
    #return A*np.exp(-Ea*(x/constants.Boltzmann))

path = './tauC_values'
temperature, T2, error, evTime = np.loadtxt(path, usecols=(0,1,2,3), unpack=True, comments='#')

temp_1=list()
temp_2=list()
T2_1 =list()
T2_2 =list()
error_1=list()
error_2=list()

for i,time in enumerate(evTime):
    if time==1.5e-5:
        temp_1.append(temperature[i])
        T2_1.append(T2[i])
        error_1.append(error[i])
    else:
        temp_2.append(temperature[i])
        T2_2.append(T2[i])
        error_2.append(error[i])

temp_1.append(1/2.94865680e-03)
temp_2.append(1/2.94865680e-03)
T2_1.append(1/np.pi/2/117.025e6)
T2_2.append(1/np.pi/2/117.025e6)



fig = plt.figure()
ax = fig.add_subplot(111)

###########
#erste Zeit
temperature = np.array(temp_1)
T2 = np.array(T2_1)
error = np.array(error_1)

plt.errorbar(1/temperature[:-1], T2[:-1], yerr=np.sqrt(error), fmt="none", color="red", ecolor="red", marker="o")
plt.plot(1/temperature[:-1], T2[:-1], marker="o",ms=3, ls="", color="red", label=r"$\tau_C$ Werte $1.5e^{-5}$")

# fit Funktion
var, cov = optimize.curve_fit(lin, 1/temperature, np.log(T2), maxfev=10000)
# zeichne Gerade
xRef=np.linspace(2.5e-3,1.1e-2,100)
yRef=np.exp(lin(xRef,var[0],var[1]))
plt.plot(xRef,yRef,label="exponentieller Fit",color="red")

# berechne Tau0
fOut=open("Ea_1.output","w")
b=np.exp(var[1])
bCov=np.exp(b)*np.sqrt((cov[1,1]))
tempString1 = str(round(b*1e12,2))+"\\cdot10^{-12} \pm "+str(round(bCov,2))
fOut.write("\\tau_{0, 1.5} &= (" + tempString1 +")\\text{[s]}\\\\")
#berechne EA
tempString2 = str(round(var[0]*constants.Boltzmann/constants.e*1000,1))+" \\pm "+str(round(np.sqrt(cov[0,0])*constants.Boltzmann/constants.e*1000,1))
fOut.write("E_{A, 1.5} &= (" + tempString2 +")\ \\text{[meV]}")
fOut.close()
print(r"$\tau_0$ = " +str(b) + r"$\pm $ " + str(bCov))

##########
#zweite Zeit
temperature = np.array(temp_2)
T2 = np.array(T2_2)
error = np.array(error_2)

plt.errorbar(1/temperature[:-1], T2[:-1], yerr=np.sqrt(error), fmt="none", color="blue", ecolor="blue", marker="o")
plt.plot(1/temperature[:-1], T2[:-1], marker="o",ms=3, ls="", color="blue", label=r"$\tau_C$ Werte $2.0e^{-5}$")

# fit Funktion
var, cov = optimize.curve_fit(lin, 1/temperature, np.log(T2), maxfev=10000)
# zeichne Gerade
xRef=np.linspace(2.5e-3,1.1e-2,100)
yRef=np.exp(lin(xRef,var[0],var[1]))
plt.plot(xRef,yRef,label="exponentieller Fit",color="blue")

# berechne Tau0
fOut=open("Ea_2.output","w")
b=np.exp(var[1])
bCov=np.exp(b)*np.sqrt((cov[1,1]))
tempString1 = str(round(b*1e12,2))+"\\cdot10^{-12} \pm "+str(round(bCov,2))
fOut.write("\\tau_{0, 2.0} &= (" + tempString1 +")\\text{[s]}\\\\")
#berechne EA
tempString2 = str(round(var[0]*constants.Boltzmann/constants.e*1000,1))+" \\pm "+str(round(np.sqrt(cov[0,0])*constants.Boltzmann/constants.e*1000,1))
fOut.write("E_{A, 2.0} &= (" + tempString2 +")\ \\text{[meV]}")
fOut.close()
print(r"$\tau_0$ = " +str(b) + r"$\pm $ " + str(bCov))

plt.scatter(2.94865680e-03, 1/np.pi/2/117.025e6, color="green", label="Lamorfrequenz Datenpunkt")

plt.ylim((1e-10,10))

plt.yticks(np.arange(10e-5, 10e-4, 0.001))
ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.grid()
plt.yscale("log")
plt.xlabel(r"Temperatur$^{-1} \left[\frac{1}{K}\right]$")
plt.ylabel(r"$\tau_C$ [s]")
plt.legend(loc=4)
plt.title(r"$\tau_C$ Tieftemperatur F2")
plt.savefig('F2_Fit.pdf')

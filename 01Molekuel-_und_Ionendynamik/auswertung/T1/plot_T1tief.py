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

def kohlrausch(x,T1,v,A,c):
    return np.exp(-(x/T1)**v)*A+c

def p(var):
    print(var+" = "+'\n'+str(eval(var))+'\n')

    time, amplitude, error = np.loadtxt(path, usecols=(0,5,6), unpack=True, comments='#')

colors = iter(cm.jet(np.linspace(0, 1, 8)))
markers = iter([".","d","2","x","8","4","s","*","D","+","o","x","3","p"])

def T1(path,ax,temp,f,f2):
    time, amplitude, error = np.loadtxt(path, usecols=(0,5,6), unpack=True, comments='#')

    var, cov = optimize.curve_fit(kohlrausch, time, amplitude, p0=(30,0.99,-4000,4000), maxfev=1000000)
    xRef = np.linspace(min(time),max(time),num=1000)
    yRef = kohlrausch(xRef, var[0],var[1],var[2],var[3])

    col = next(colors)
    mark = next(markers)
    plt.plot(xRef, yRef,color=col)
    ax.scatter(time,amplitude, color=col, marker=mark, label=str(int(temp))+"K")

    f.write(str(temperature)+"\t"+str(var[0])+"\t"+str(np.sqrt(cov[0,0]))+"\n")
    tempString = str(temperature) + " & " + str(round(var[0],2))+" \\pm "+str(round(np.sqrt(cov[0,0]),2))+" & " + str(round(var[1]*10,2))+" \\pm "+str(round(np.sqrt(cov[1,1])*10,2)) +" \\\\\\hline\n"
    f2.write(tempString.replace("E","\\cdot 10^{"))
path='../_daten/tieftemperatur/'


figT1 = plt.figure()
axT1 = plt.gca()
outFile = open('T1_valuesTief', 'w')
outFile2 = open('T1_valuesTief_table', 'w')
outFile.write("# Temperatur \t T1 \t std\n")
outFile2.write("\\text{Temperatur } [K] & T_1\ [s] & \\nu\ [10^{-1}] \\\\\\hline\n")

filelist = list()

for root, dirs, files in os.walk(path):
    options = root.split(sep="_")
    if len(options)>3:
        typ = options[3]
        temperature = options[4][:-1]
        if(typ=="T1"):
            temperature = round(float(temperature) * 0.922 - 1.085)

            for f in files:
                if(f.endswith(".nmr")):
                    filelist.append((temperature,root+"/"+f))

filelist = sorted(filelist,key=lambda x: x[0])
for temperature, filePath in filelist:
    T1(filePath,axT1,temperature,outFile,outFile2)

outFile.close()
axT1.set_xscale('log')
axT1.grid()
plt.title(r"$T_1$ Echo Amplitude Tieftemperatur")
plt.xlabel("Zeit [s]")
plt.ylabel("Amplitude")
axT1.legend(loc=2)
plt.savefig('T1_tiefTemperaturFit.pdf')

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

def kohlrausch(x,T1,v,A,b,c):
    return np.exp(-(x/T1)**v)*A+c

def p(var):
    print(var+" = "+'\n'+str(eval(var))+'\n')

    time, amplitude, error = np.loadtxt(path, usecols=(0,5,6), unpack=True, comments='#')
    #print(time)
    #print(amplitude)
    #var, cov = optimize.curve_fit(kohlrausch, time, amplitude, maxfev=100)
    #plt.scatter(time,amplitude)
    #plt.show()

colors = iter(cm.jet(np.linspace(0, 1, 14)))

def T1(path,ax,temp,f,f2):
    time, amplitude, error = np.loadtxt(path, usecols=(0,5,6), unpack=True, comments='#')

    var, cov = optimize.curve_fit(kohlrausch, time, amplitude, p0=(0.5,0.99,-400,0,400), maxfev=1000000)
    xRef = np.linspace(min(time),max(time),num=1000)
    yRef = kohlrausch(xRef, var[0],var[1],var[2],var[3],var[4])

    print("T1: ", var[0])
    print("v: ", var[1])
    print("A: ", var[2])
    print("b: ", var[3])
    print("c: ", var[4])

    plt.plot(xRef, yRef, "b-")
    ax.scatter(time,amplitude, color=next(colors),label=str(int(temp))+"K")

    f.write(str(temperature)+"\t"+str(var[0])+"\t"+str(cov[0,0])+"\n")
    f2.write(str(temperature)+" & "+str(round(var[0],2))+"\\\\\\hline\n") #" & "+str(cov[0,0])+"\\\\")

path='../_daten/hochtemperatur/'


figT1 = plt.figure()
axT1 = plt.gca()
outFile = open('T1_valuesHoch', 'w')
outFile2 = open('T1_valuesHoch_table', 'w')
outFile.write("# Temperatur \t T1 \t std\n")
outFile2.write("Temperatur & T1 \\\\\\hline\n")

for root, dirs, files in os.walk(path):
    options = root.split("_")
    if len(options)>3:
        typ = options[3]
        temperature = options[4][:-1]
        if(typ=="T1"):
            print("\n\nTemp: "+str(temperature))
            print(root)
            for f in files:
                if(f.endswith(".info")):
                    filePath = root+"/"+f
                    inpFile = open(filePath)
                    for line in inpFile:
                        if line.startswith("Cryostat Temperature"):
                            temperature=float(line[line.find(":")+2:])
                            temperature = round(temperature * 0.922 - 1.085)
                            print("Temp: "+str(temperature))

            for f in files:
                if(f.endswith(".nmr")):
                    filePath = root+"/"+f
                    T1(filePath,axT1,temperature,outFile,outFile2)

outFile.close()
outFile2.close()
axT1.set_xscale('log')
axT1.grid()
plt.xlim((9e-4,10))
plt.ylim((-10,700))
plt.title("T1 Echo Amplitude Hochtemperatur")
plt.xlabel("Zeit [s]")
plt.ylabel("Amplitude")
plt.legend(loc=2)
plt.savefig('T1_hochTemperaturFit.pdf')
#plt.show()

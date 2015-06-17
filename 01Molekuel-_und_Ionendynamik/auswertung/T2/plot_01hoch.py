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

def Mt2(t,Mtau,Mz0,M0,Tc,T1,beta1,beta2):
    return (Mtau+(Mz0-Mtau)*np.exp(-(t/Tc)**beta1))*np.exp(-(t/T1)**beta2)+M0

def p(var):
    print(var+" = "+'\n'+str(eval(var))+'\n')

colors = iter(cm.jet(np.linspace(0, 1, 14)))
markers = iter([".","d","2","x","8","4","s","*","D","+","o","x","3","p"])

def T2(path,ax,temp):#,f,f2):
    time, amplitude, error = np.loadtxt(path, usecols=(0,5,6), unpack=True, comments='#')
    """
    var, cov = optimize.curve_fit(Mt2, time, amplitude, p0=(400,700,-2,2,0.1,1,0.1), maxfev=1000000)
    xRef = np.logspace(-5,-1,num=10000)
    yRef = Mt2(xRef, var[0],var[1],var[2],var[3],var[4],var[5],var[6])

    plt.plot(xRef, yRef, "b-")
    """
    plt.scatter(time,amplitude, color=next(colors), marker=next(markers), label=str(temp)+"K")
    plt.xscale("log")

    """
    f.write(temp+"\t"+str(var[3])+"\t"+str(cov[3,3])+"\n")
    tempString = temp+" & "+str('%.2E' % var[3])+"} & "+str('%.2E' % cov[3,3])+"} \\\\\\hline\n"
    tempString=tempString.replace("E","\\cdot 10^{")
    f2.write(tempString)
    #plt.show()
    """


path='../_daten/hochtemperatur/'
filelist = list()


figT2 = plt.figure()
axT2 = plt.gca()
axT2.set_xscale('log')


"""
fOut=open("tauC_T2","w")
fOut.write("#Temp\ttauC\tstd\n")
fOut2=open("tauC_T2_table","w")
fOut2.write("\\text{Temperatur} & \\tau_C & \\text{Standardabweichung}\\\\\\hline\n")
"""

for root, dirs, files in os.walk(path):
    options = root.split(sep="_")
    if len(options)>3:
        typ = options[3]
        temperature = options[4][:-1]
        if(typ=="T2"):
            for f in files:
                if(f.endswith(".info")):
                    filePath = root+"/"+f
                    inpFile = open(filePath)
                    for line in inpFile:
                        if line.startswith("Cryostat Temperature"):
                            temperature=float(line[line.find(":")+2:])
                            temperature = round(temperature * 0.922 - 1.085)
            for f in files:
                if(f.endswith(".nmr")):
                    filelist.append((temperature,root+"/"+f))

filelist = sorted(filelist,key=lambda x: x[0])
for temperature, filePath in filelist:
    T2(filePath,axT2,temperature)#,outFile,outFile2)


#fOut.close()
#fOut2.close()

plt.grid()
plt.legend()
plt.ylim((-100,1000))
plt.title(r"$T_2$ Hochtemperatur Messwerte")
plt.xlabel("Zeit [s]")
plt.ylabel("Echo Amplitude")
plt.savefig("T2_hochTemperaturFit.pdf")

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
from operator import itemgetter

for arg in sys.argv:
    if(arg=='silent'):
        output_silent = True

#########################################
# Preparation				#
#########################################

def Mt(t,Mz0,Tc,beta1):
    return Mz0*np.exp(-(t/Tc)**beta1)
def lin(x,m,b):
    return m*x+b

def p(var):
    print(var+" = "+'\n'+str(eval(var))+'\n')

colors = iter(cm.jet(np.linspace(0, 1, 10)))
markers = iter([".","d","2","x","8","4","s","*","D","+","o","x","3","p"])

def F2(path,ax,temp,evTime, f,f2):
    time, amplitude, error = np.loadtxt(path, usecols=(0,5,6), unpack=True, comments='#')

    var, cov = optimize.curve_fit(Mt, time, amplitude, p0=(700,2,1), maxfev=1000000)

    xRef = np.logspace(-4,3,num=10000)
    yRef = Mt(xRef, var[0],var[1],var[2])

    col = next(colors)
    print("ts:",evTime)
    plt.scatter(time,amplitude, color=col, marker=next(markers), label=temp+"K, evo= " + str(evTime)+"s")
    plt.plot(xRef,yRef,color=col)

    f.write(temp+"\t"+str(var[1])+"\t"+str(np.sqrt(cov[1,1]))+"\t" + str(evTime) +"\n")
    tempString = temp+" & "+str(round(var[1]*10,2))+" \\pm "+str(round(np.sqrt(cov[1,1])*10,2))+" & "+str(round(var[2],2))+" \\pm "+str(round(np.sqrt(cov[2,2]),2))+" \\\\\\hline\n"
    if(evTime==2.0e-5):
        tempString="\\rowcolor{gray!10}" +tempString
    f2.write(tempString)



path='../_daten/tieftemperatur/'
filelist = list()
fOut=open("tauC_values","w")
fOut2=open("tauC_values_table","w")

figF2 = plt.figure()
axF2 = plt.gca()
axF2.set_xscale('log')

for root, dirs, files in os.walk(path):
    options = root.split(sep="_")
    if len(options)>3:
        typ = options[3]
        temperature = options[4][:-1]
        temperature = round(int(temperature) * 0.922 - 1.085)
        if(typ=="F2"):
            for f in files:
                if(f.endswith(".info")):
                    print(f)
                    filePath = root+"/"+f
                    inpFile = open(filePath)
                    for line in inpFile:
                        if line.startswith("Evolution time"):
                            evTime=float(line[line.find(":")+2:])
                            print(evTime)
            for f in files:
                if(f.endswith(".nmr")):
                    print(evTime)
                    filelist.append((temperature,root+"/"+f,evTime))

filelist = sorted(filelist,key=itemgetter(0,2))
"""
tempo = filelist[-3]
filelist[-3] = filelist[-4]
filelist[-4] = tempo
"""
for temperature, filePath, evTime in filelist:
    F2(filePath,axF2,str(temperature), evTime, fOut,fOut2)

fOut.close()
fOut2.close()

axF2.grid()
axF2.legend()
plt.title("F2 Plot Tieftemperatur")
plt.xlabel("Zeit [s]")
plt.ylabel("Echo Amplitude")
plt.savefig("F2_Plot.pdf")
plt.show()

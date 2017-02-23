#!/usr/bin/python3
# -*- coding: utf-8 -*-

output_silent = True
output_gen = True
import numpy as np
from scipy import optimize, interpolate, misc, stats, constants, signal
import matplotlib.pyplot as plt
import os, sys
for arg in sys.argv:
	if arg=='silent': output_silent = True
#from latex_array import latex_array
#from latex_number import latex_number
#from load_strings import load_strings
#from linregress import linregress
#from plotting import *
#from operator import truediv
import glob
import pprint

def getAmplitude(source):
	min = source[0]
	max = source[0]
	for i in source:
		if(i <= min):
			min = i
		elif(i >= max):
			max = i
	return abs(max-min)

def getAverage(source):
	average = 0
	for i in source:
		average = average + i

	return average/len(source)

def linearFit(x,y,d):
	def f(x,a,b):
		return a*x+b

	var, cov = optimize.curve_fit(f,x,y,sigma=d,maxfev=10000)
	temp = dict()
	temp["var"] = var
	temp["cov"] = cov
	temp["x"] = np.linspace((min(x)),(max(x)),num=5000)
	temp["y"] = f(temp["x"],var[0],var[1])
	return temp

sinus = np.loadtxt("./data/b_1.csv",delimiter=',')
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(sinus[:,0],sinus[:,1],'r-',label=r"Angelegte Sinusspannung")
ax1.set_ylabel(r"$U_1$/V")
ax1.set_ylim(-0.04,0.04)
ax1.legend(loc="upper left")
for tl in ax1.get_yticklabels():
    tl.set_color('r')
ax2 = ax1.twinx()
ax2.plot(sinus[:,0],sinus[:,2]-getAverage(sinus[:,2]),'b-',label=r"Gemessene Cosinusspannung")
ax2.set_ylabel(r"$U_A$/V")
ax2.set_ylim(-0.9,0.9)
ax2.legend(loc="lower left")
for tl in ax2.get_yticklabels():
    tl.set_color('b')
plt.xlabel("$t$/s")
plt.savefig("./results/b/sinus.pdf")
#plt.show()
plt.close()

rechteck = np.loadtxt("./data/b_4.csv",delimiter=',')
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(rechteck[:,0],-rechteck[:,1],'r-',label=r"Angelegte Rechteckspannung")
ax1.set_ylabel(r"$U_1$/V")
ax1.set_ylim(-0.07,0.07)
ax1.legend(loc="upper left")
for tl in ax1.get_yticklabels():
    tl.set_color('r')
ax2 = ax1.twinx()
ax2.plot(rechteck[:,0],rechteck[:,2]-getAverage(rechteck[:,2]),'b-',label=r"Gemessene Dreiecksspannung")
ax2.set_ylabel(r"$U_A$/V")
ax2.set_ylim(-1.4,1.4)
ax2.legend(loc="lower left")
for tl in ax2.get_yticklabels():
    tl.set_color('b')
plt.xlabel("$t$/s")
plt.savefig("./results/b/rechteck.pdf")
#plt.show()
plt.close()


dreieck = np.loadtxt("./data/b_5.csv",delimiter=',')
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(dreieck[:,0],dreieck[:,1],'r-',label=r"Angelegte Dreiecksspannung")
ax1.set_ylabel(r"$U_1$/V")
ax1.set_ylim(-0.03,0.03)
ax1.legend(loc="upper left")
for tl in ax1.get_yticklabels():
    tl.set_color('r')
ax2 = ax1.twinx()
ax2.plot(dreieck[:,0],dreieck[:,2]-getAverage(dreieck[:,2]),'b-',label=r"Gemessene Rechteckspannung")
ax2.set_ylabel(r"$U_A$/V")
ax2.set_ylim(-0.9,0.9)
ax2.legend(loc="lower left")
for tl in ax2.get_yticklabels():
    tl.set_color('b')
plt.xlabel("$t$/s")
plt.savefig("./results/b/dreieck.pdf")
#plt.show()
plt.close()

R = 100
deltaR = 0.01
C = 102.3 * 10**-9
deltaC = 0.02
U0 = 10
deltaU0 = 0.01

deltaUa = ( (deltaR)**2 + (deltaC)**2 )**0.5
print(deltaUa)

charCurve = np.loadtxt("./data/b.csv")
#print(charCurve)
plt.plot(1/charCurve[:,0],charCurve[:,1],"bx",label="Messwerte und Fit")
plt.errorbar(1/charCurve[:,0],charCurve[:,1],yerr=deltaUa*charCurve[:,1],fmt="bx")
fit = linearFit(1/charCurve[:,0],charCurve[:,1],deltaUa*charCurve[:,1])
plt.plot(fit["x"],fit["y"],"b-")
#pprint.pprint(fit)
plt.xlabel("$\\frac{1}{f}$ /$10^3$ s")
plt.ylabel("$U_A$/V")
plt.legend()
#plt.xscale("log")
#plt.yscale("log")
plt.savefig("./results/b/charKurve.pdf")
plt.show()
plt.close()

file = open("./results/b/bb.tex","w")
file.write(str("b = ("+str(np.around(fit["var"][1],2)) + " $\\pm$ " + str(np.around(fit["cov"][1,1],8)) + ")\\ \\si{\\volt}"))
file.close()
file = open("./results/b/ba.tex","w")
file.write(str("a = ("+str(np.around(fit["var"][0],2)) + " $\\pm$ " + str(np.around(fit["cov"][0,0],8)) + ")"))
file.close()
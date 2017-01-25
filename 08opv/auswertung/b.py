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

def linearFit(x,y):
	def f(x,a,b):
		return a*x+b

	var, cov = optimize.curve_fit(f,x,y,maxfev=10000)
	temp = dict()
	temp["var"] = var
	temp["cov"] = cov
	temp["x"] = np.linspace((min(x)),(max(x)),num=5000)
	temp["y"] = f(temp["x"],var[0],var[1])
	return temp

sinus = np.loadtxt("./data/b_1.csv",delimiter=',')
#print(sinus)
plt.plot(sinus[:,0],sinus[:,1]/getAmplitude(sinus[:,1])*getAmplitude(sinus[:,2]),'r-',label=r"Angelegte Sinusspannung")
plt.plot(sinus[:,0],sinus[:,2]-getAverage(sinus[:,2]),'b-',label=r"Gemessene Cosinusspannung")
plt.xlabel("$t$ [s]")
plt.ylabel("$U$ [V]")
plt.ylim(-0.8,1.0)
plt.legend()
plt.savefig("./results/b/sinus.pdf")
#plt.show()
plt.close()

rechteck = np.loadtxt("./data/b_4.csv",delimiter=',')
plt.plot(rechteck[:,0],-rechteck[:,1]/getAmplitude(rechteck[:,1])*getAmplitude(rechteck[:,2]),'r-',label=r"Angelegte Rechteckspannung")
plt.plot(rechteck[:,0],rechteck[:,2]-getAverage(rechteck[:,2]),'b-',label=r"Gemessene Dreiecksspannung")
plt.xlabel("$t$ [s]")
plt.ylabel("$U$ [V]")
plt.ylim(-1.5,1.7)
plt.legend()
plt.savefig("./results/b/rechteck.pdf")
#plt.show()
plt.close()

dreieck = np.loadtxt("./data/b_5.csv",delimiter=',')
plt.plot(dreieck[:,0],-dreieck[:,1]/getAmplitude(dreieck[:,1])*getAmplitude(dreieck[:,2]),'r-',label=r"Angelegte Dreiecksspannung")#,linewidth=0.10)
plt.plot(dreieck[:,0],dreieck[:,2]-getAverage(dreieck[:,2]),'b-',label=r"Gemessene Rechteckspannung")
plt.xlabel("$t$ [s]")
plt.ylabel("$U$ [V]")
plt.ylim(-0.6,0.8)
plt.legend()
plt.savefig("./results/b/dreieck.pdf")
#plt.show()
plt.close()


charCurve = np.loadtxt("./data/b.csv")
#print(charCurve)
plt.plot(1/charCurve[:,0],charCurve[:,1],"bx",label="Messwerte und Fit")
fit = linearFit(1/charCurve[:,0],charCurve[:,1])
plt.plot(fit["x"],fit["y"],"b-")
pprint.pprint(fit)
plt.xlabel("$1/f$ [1/kHz]")
plt.ylabel("$U$ [V]")
plt.legend()
#plt.xscale("log")
#plt.yscale("log")
plt.savefig("./results/b/charKurve.pdf")
#plt.show()
plt.close()

file = open("./results/b/bb.tex","w")
file.write(str("$b = ("+str(np.around(fit["var"][1],2)) + "\\pm" + str(np.around(fit["cov"][1,1],8)) + ")\\ \\si{\\volt}$"))
file.close()
file = open("./results/b/ba.tex","w")
file.write(str("$a = ("+str(np.around(fit["var"][0],2)) + "\\pm" + str(np.around(fit["cov"][0,0],8)) + ")$"))
file.close()
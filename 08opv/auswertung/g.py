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
import peakutils

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

def expFit(x,y):
	def f(x,a,b,c):
		return b*x**a+c

	var, cov = optimize.curve_fit(f,x,y)
	temp = dict()
	temp["var"] = var
	temp["cov"] = cov
	temp["x"] = np.linspace(min(x),max(x),num=5000)
	temp["y"] = f(np.linspace(min(x),max(x),num=5000),var[0],var[1],var[2])
	return temp

def expSinFit(x,y):
	def f(t,omega,phi,A,l):
		return A*np.sin(omega*t+phi)*np.exp(l*t+phi)

	var,cov = optimize.curve_fit(f,x,y,maxfev=10000,p0=[2*np.pi/0.0014,0.546,-1,-5])
	temp = dict()
	temp["var"] = var
	temp["cov"] = cov
	temp["x"] = np.linspace(min(x),max(x),num=5000)
	temp["y"] = f(temp["x"],var[0],var[1],var[2],var[3])
	return temp

def cosFit(x,y):
	def f(t,omega,phi,A):
		return A*np.cos(omega*t+phi)

	var,cov = optimize.curve_fit(f,x,y,p0=[2*np.pi/0.0014,0.546,5.3])
	temp = dict()
	temp["var"] = var
	temp["cov"] = cov
	temp["x"] = np.linspace(min(x),max(x),num=5000)
	temp["y"] = f(temp["x"],var[0],var[1],var[2])
	return temp





schwing = np.loadtxt("./data/g_0.csv",delimiter=",")
plt.plot(schwing[:,0],schwing[:,1],"b-",label="Angelegte Rechteckspannung")
plt.plot(schwing[:,0],schwing[:,2],"g-",label="Gemessene Sinusspannung")
plt.xlabel("$t$ [s]")
plt.ylabel("$U$ [V]")
#schwing = schwing[(schwing[:,0]>0.505)&(schwing[:,0]<0.55)]
#fit = cosFit(schwing[:,0],schwing[:,1])
#print(fit["var"][0])
#plt.plot(fit["x"],fit["y"],"r-")
plt.xlim(0.5,0.55)
plt.legend()
plt.savefig("./results/g/schwing1.pdf")
#plt.show()
plt.close()

schwing = np.loadtxt("./data/g_1.csv",delimiter=",")
plt.plot(schwing[:,0],schwing[:,2],"b-",label="Angelegte Rechteckspannung")
plt.plot(schwing[:,0],schwing[:,1],"g-",label="Gemessene Sinusspannung")
plt.xlabel("$t$ [s]")
plt.ylabel("$U$ [V]")
fit = cosFit(schwing[:,0],schwing[:,1])
print("omega: ", fit["var"][0])
plt.plot(fit["x"],fit["y"],"r-")
#plt.xlim(0.5,0.55)
plt.legend()
plt.savefig("./results/g/schwing2.pdf")
#plt.show()
plt.close()

def fff(t,omega,phi,A,l):
	return A*np.e**(-l*t+phi)*np.sin(omega*t+phi)

daempf = np.loadtxt("./data/g_2.csv",delimiter=",")
plt.plot(daempf[:,0],daempf[:,2],"b-",label="Angelegte Rechteckspannung")
plt.plot(daempf[:,0],daempf[:,1],"g-",label="Gemessene gedämpfte Sinusspannung")
plt.xlabel("$t$ [s]")
plt.ylabel("$U$ [V]")
daempf = daempf[(daempf[:,0]>0.546)&(daempf[:,0]<0.566)]
fit = expSinFit(daempf[:,0],daempf[:,1])
#print(fit["var"][0])
plt.plot(fit["x"],fit["y"],"r-",label="Fit gedämpfte Sinusspannung")
#plt.plot(daempf[:,0],fff(daempf[:,0],2*np.pi/0.0014,0.546,-20,5))
plt.xlim(0.545,0.575)
plt.legend()
plt.savefig("./results/g/daempf.pdf")
#plt.show()
plt.close()

pprint.pprint(fit)

file = open("./results/g/daempfParameter.tex","w")
string = str("U_0 = " + str(fit["var"][2]) + 
	" V\\\\ \\tau = " + str(1/fit["var"][3]) + 
	" \\si{\\second}\\\\ \\varphi = " + str(fit["var"][1])+
	"\\\\ \\omega = " + str(fit["var"][0]) + "\\frac{1}{\\si{\\second}}")
file.write(string)
file.close()
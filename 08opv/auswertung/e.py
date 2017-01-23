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
		return b*x**a + c

	var, cov = optimize.curve_fit(f,x,y)
	temp = dict()
	temp["var"] = var
	temp["cov"] = cov
	temp["x"] = np.linspace(min(x),max(x),num=5000)
	temp["y"] = f(np.linspace(min(x),max(x),num=5000),var[0],var[1],var[2])
	return temp

frequencies = np.loadtxt("./e_freq.csv")
data = dict()
for i in range(0,len(frequencies)):
	print(frequencies[i],": ",str("./data/e_" + str(i) + ".csv"))
	data[frequencies[i]] = np.loadtxt(str("./data/e_" + str(i) + ".csv"),delimiter=",")

#pprint.pprint(data)

plt.plot(data[0.5][:,0],data[0.5][:,1])
plt.plot(data[0.5][:,0],data[0.5][:,2])
#plt.show()
#plt.plot()
plt.close()

plt.plot(data[frequencies[0]][:,0],data[frequencies[0]][:,1])
plt.plot(data[frequencies[0]][:,0],data[frequencies[0]][:,2]/getAmplitude(data[frequencies[-1]][:,2])*getAmplitude(data[frequencies[-1]][:,1]),"bx")
#print(signal.argrelextrema(data[frequencies[-1]][:,1],np.greater,order=30))
#plt.show()
plt.plot()
plt.close()

phases = list()
for frequency in frequencies:
	def getPhase(t,y1,y2):
		def cos(x,omega,phi,A):
			return A*np.cos(omega*x+phi)

		var1, cov1 = optimize.curve_fit(cos,t,y1,p0=[2*np.pi*frequency*1000,1,getAmplitude(y1)/2])
		var2, cov2 = optimize.curve_fit(cos,t,y2,p0=[2*np.pi*frequency*1000,1,getAmplitude(y1)/2])
		temp = dict()
		temp["x"] = np.linspace(min(t),max(t),num=5000)
		temp["y1"] = cos(temp["x"],var1[0],var1[1],var1[2])
		temp["y2"] = cos(temp["x"],var2[0],var2[1],var2[2])
		temp["phi"] = var1[1]-var2[1]/np.pi*180
		temp["omega"] = [var1[0],var2[0]]
		temp["A"] = [var1[2],var2[2]]
		return temp

	print(frequency)
	fit = getPhase(data[frequency][:,0],data[frequency][:,1],data[frequency][:,2])
	pprint.pprint(fit)
	phases.append(fit["phi"])

#print(phases)
for i in range(0,len(phases)):
	while(phases[i] > 180):
		phases[i] = phases[i] - 180
	while(phases[i] < 0):
		phases[i] = phases[i] + 180

print(frequencies)
print(phases)
plt.close()
plt.plot(frequencies,phases,"rx")
fit = expFit(frequencies,phases)
pprint.pprint(fit)
plt.plot(fit["x"],fit["y"])
plt.xscale("log")
plt.yscale("log")
plt.show()
plt.close()
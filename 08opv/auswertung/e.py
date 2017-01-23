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


frequencies = np.loadtxt("./e_freq.csv")
data = dict()
for i in range(0,len(frequencies)):
	print(frequencies[i])
	data[frequencies[i]] = np.loadtxt(glob.glob("./data/e*.csv")[i],delimiter=",")

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
	def getPhase(x,y1,y2):
		def cos(t,omega,phi,A):
			return A*np.cos(omega*t+phi)

		var1, cov1 = optimize.curve_fit(cos,x,y1)
		var2, cov2 = optimize.curve_fit(cos,x,y2)
		print(var1)
		print(var2)
		print((var1[1]-var2[1])/np.pi*180+180)
		plt.plot(x,y1,"bx")
#		plt.plot(x,y2,"rx")
		plt.plot(np.linspace(min(x),max(x),num=5000),cos(np.linspace(min(x),max(x),num=5000),var1[0],var1[1],var1[2]),"b-")
#		plt.plot(np.linspace(min(x),max(x),num=5000),cos(np.linspace(min(x),max(x),num=5000),var2[0],var2[1],var2[2]),"r-")
		return ((var1[1]-var2[1])/np.pi*180+180)#, (cov1[1]-cov2[1])	

	phases.append(getPhase(data[frequency][:,0],data[frequency][:,1],data[frequency][:,2]))


#	data[frequency][:,2] = data[frequency][:,2]/getAmplitude(data[frequency][:,2])*getAmplitude(data[frequency][:,1])
#	print(frequency)
#	maxima1 = peakutils.peak.indexes(data[frequency][:,1],thres=0.4,min_dist=3000) #signal.argrelextrema(data[frequency][:,1],np.greater,order=80,mode="wrap")
#	peakutils.plot.plot(data[frequency][:,0],data[frequency][:,1],maxima1)
#	maxima2 = peakutils.peak.indexes(data[frequency][:,2],thres=0.4,min_dist=3000) #signal.argrelextrema(data[frequency][:,2],np.greater,order=35,mode="wrap")
#	if(True):#frequency == 0.5):
#		plt.plot(data[frequency][:,0],data[frequency][:,1])
#		plt.plot(data[frequency][:,0],data[frequency][:,2])
#		print(len(maxima1))
#		print(maxima1[0])
#		print(data[frequency][maxima1[0][-1],0])
#		print(len(maxima2))
#		print(maxima2[0])
#		print(data[frequency][maxima2[0][-1],0])
#		deltat = data[frequency][maxima2[3],0]-data[frequency][maxima1[3],0]
#		phase = frequency * 1000 * 360 * deltat
#		phases.append(phase)
#		print(phase)
#		plt.show()
#		plt.close()

print(phases)
for i in range(0,len(phases)):
	while(phases[i] > 90):
		phases[i] = phases[i] - 180
	while(phases[i] < 0):
		phases[i] = phases[i] + 180


print(phases)
plt.close()
plt.plot(frequencies,phases,"rx")
plt.xscale("log")
plt.yscale("log")
plt.show()
plt.close()
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
#	print(source)
	min = source[0]
	max = source[0]
#	print(min, max)
	for i in source:
		if(i <= min):
			min = i
		elif(i >= max):
			max = i
#	print('min: ',min,' max: ',max)
	return abs(max-min)

def linearFit(x,y,minimum):
	x = np.array(x)
#	pprint.pprint(x)
	y = np.array(y)
#	pprint.pprint(y)
	def f(x,a,b):
		return b*x**a

#	guessA = (max(np.log(y[x > minimum]))-min(np.log(y[x > minimum])))/(max(np.log(x[x > minimum]))-min(np.log(x[x > minimum])))
#	print(np.log(y[x > minimum]))
	var, cov = optimize.curve_fit(f,(x[x >minimum]),(y[x > minimum]),maxfev=10000)
#	print(var[0])
#	print(var[1])
	temp = dict()
	temp["var"] = var
	temp["cov"] = cov
	temp["x"] = np.linspace((min(x[x > minimum])),(max(x[x > minimum])),num=5000)
	temp["y"] = f(temp["x"],var[0],var[1])#(var[0]*temp["x"]+var[1])#temp["x"]**var[0]*np.exp(var[1])#f(temp["x"],var[0], var[1])
#	print(temp["y"][0],temp["y"][-1])
	return temp


pi = np.pi

frequencies = np.loadtxt('a_freq.csv', delimiter=',')
thresholds = np.loadtxt('a_thresholds.csv')
amplitudes = list()

Rn = 1000
print("Rn = 1000")
for i in range(1,26):
	if(i != 12):
#		print(str('./data/scope_' + str(i) + '.csv'))
		amplitudes.append(getAmplitude(np.loadtxt(str('./data/scope_' + str(i) + '.csv'),delimiter=',')[:,2]))
plt.plot(frequencies[frequencies != 10],amplitudes,'bx')
fit = linearFit(frequencies[frequencies != 10], amplitudes, thresholds[0,2])
plt.plot(fit["x"], fit["y"], 'b-')

Rn = 500
print("Rn = 500")
frequencies = np.loadtxt('a_freq.csv',delimiter=',')
amplitudes = list()
for i in range(26,51):
	if(True):
#		print(str('./data/scope_' + str(i) + '.csv'))
		amplitudes.append(getAmplitude(np.loadtxt(str('./data/scope_' + str(i) + '.csv'),delimiter=',')[:,2]))
plt.plot(frequencies[::-1],amplitudes,'rx')
fit = linearFit(frequencies, amplitudes, thresholds[1,2])
plt.plot(fit["x"], fit["y"], 'r-')

Rn = 10000
print("Rn = 10000")
frequencies = np.loadtxt('a_freq.csv',delimiter=',')
amplitudes = list()
for i in range(51,76):
	if(True):
#		print(str('./data/scope_' + str(i) + '.csv'))
		amplitudes.append(getAmplitude(np.loadtxt(str('./data/scope_' + str(i) + '.csv'),delimiter=',')[:,2]))
plt.plot(frequencies,amplitudes,'gx')
fit = linearFit(frequencies, amplitudes, thresholds[2,2])
plt.plot(fit["x"], fit["y"], 'g-')

Rn = 330
print("Rn = 330")
frequencies = np.loadtxt('a_freq.csv', delimiter=',')
amplitudes = list()
for i in range(76,101):
	if(True):
#		print(str('./data/scope_' + str(i) + '.csv'))
		amplitudes.append(getAmplitude(np.loadtxt(str('./data/scope_' + str(i) + '.csv'),delimiter=',')[:,2]))
plt.plot(frequencies[::-1],amplitudes,'kx')
fit = linearFit(frequencies, amplitudes, thresholds[3,2])
plt.plot(fit["x"], fit["y"], 'k-')

#plt.xscale('log')
#plt.yscale('log')
plt.show()
plt.close()
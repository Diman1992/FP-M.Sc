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

bla = np.loadtxt('data/scope_99.csv',delimiter=',')
print(getAmplitude(bla[:,2]))
#bla = np.log(bla)
#pprint.pprint(bla)
plt.plot(bla[:,0],bla[:,1])
plt.plot(bla[:,0],bla[:,2])
#plt.show()
plt.close()

Rn = 1000
pi = np.pi
amplitudes = list()
for i in range(1,26):
	print(i)
	amplitudes.append(getAmplitude(np.loadtxt(str('./data/scope_' + str(i) + '.csv'),delimiter=',')[:,2]))

print(amplitudes)
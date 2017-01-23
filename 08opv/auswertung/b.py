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

sinus = np.loadtxt("./data/b_1.csv",delimiter=',')
#print(sinus)
plt.plot(sinus[:,0],sinus[:,1]/getAmplitude(sinus[:,1])*getAmplitude(sinus[:,2]),'r-')
plt.plot(sinus[:,0],sinus[:,2]-getAverage(sinus[:,2]),'b-')
#plt.show()
plt.close()

rechteck = np.loadtxt("./data/b_4.csv",delimiter=',')
plt.plot(rechteck[:,0],-rechteck[:,1]/getAmplitude(rechteck[:,1])*getAmplitude(rechteck[:,2]),'r-')
plt.plot(rechteck[:,0],rechteck[:,2]-getAverage(rechteck[:,2]),'b-')
#plt.show()
plt.close()

dreieck = np.loadtxt("./data/b_5.csv",delimiter=',')
plt.plot(dreieck[:,0],-dreieck[:,1]/getAmplitude(dreieck[:,1])*getAmplitude(dreieck[:,2]),'r-')#,linewidth=0.10)
plt.plot(dreieck[:,0],dreieck[:,2]-getAverage(dreieck[:,2]),'b-')
plt.savefig("./results/b/dreieck.pdf",format="pdf")
plt.show()
plt.close()


charCurve = np.loadtxt("./data/b.csv")
#print(charCurve)
plt.plot(1/charCurve[:,0],charCurve[:,1],"bx")
#plt.xscale("log")
#plt.yscale("log")
#plt.show()
plt.close()
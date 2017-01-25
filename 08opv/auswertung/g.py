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
		return A*np.sin(omega*t+phi)*np.exp(l*t)

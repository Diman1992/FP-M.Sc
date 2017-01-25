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
import tabulate
tabulate.LATEX_ESCAPE_RULES={}

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
		return b*x**a

	var, cov = optimize.curve_fit(f,x,y,maxfev=10000)
	temp = dict()
	temp["var"] = var
	temp["cov"] = cov
	temp["x"] = np.linspace((min(x)),(max(x)),num=5000)
	temp["y"] = f(temp["x"],var[0],var[1])
	return temp


sinus = np.loadtxt("./data/c_26.csv",delimiter=',')
#print(sinus)
plt.plot(sinus[:,0],sinus[:,1]/getAmplitude(sinus[:,1])*getAmplitude(sinus[:,2]),'r-',label=r"Angelegte Sinusspannung")
plt.plot(sinus[:,0],sinus[:,2]-getAverage(sinus[:,2]),'b-',label=r"Gemessene Cosinusspannung")
plt.xlabel("$t$ [s]")
plt.ylabel("$U$ [V]")
plt.ylim(-0.3,0.5)
plt.legend()
plt.savefig("./results/c/sinus.pdf")
#plt.show()
plt.close()

rechteck = np.loadtxt("./data/c_27.csv",delimiter=',')
plt.plot(rechteck[:,0],-rechteck[:,1]/getAmplitude(rechteck[:,1])*getAmplitude(rechteck[:,2]),'r-',label=r"Angelegte Rechteckspannung")
plt.plot(rechteck[:,0],rechteck[:,2]-getAverage(rechteck[:,2]),'b-',label=r"Gemessene Delta-pearks")
plt.xlabel("$t$ [s]")
plt.ylabel("$U$ [V]")
plt.ylim(-10,12)
plt.legend()
plt.savefig("./results/c/rechteck.pdf")
#plt.show()
plt.close()

dreieck = np.loadtxt("./data/c_1.csv",delimiter=',')
plt.plot(dreieck[:,0],-dreieck[:,1]/getAmplitude(dreieck[:,1])*getAmplitude(dreieck[:,2]),'r-',label=r"Angelegte Dreiecksspannung")#,linewidth=0.10)
plt.plot(dreieck[:,0],dreieck[:,2]-getAverage(dreieck[:,2]),'b-',label=r"Gemessene Rechteckspannung")
plt.xlabel("$t$ [s]")
plt.ylabel("$U$ [V]")
plt.ylim(-0.4,0.6)
plt.legend()
plt.savefig("./results/c/dreieck.pdf")
#plt.show()
plt.close()

frequencies = np.loadtxt("c_freq.csv")
amplitudes = list()
for i in range(1,14):
	if(True):
#		print(str('./data/c_' + str(i) + '.csv'))
		amplitudes.append(getAmplitude(np.loadtxt(str('./data/c_' + str(i) + '.csv'),delimiter=',')[:,2]))
plt.plot(1/frequencies,amplitudes,"bx",label="Meswerte und Fit bei angelegter Dreiecksspannung")
fit = linearFit(1/frequencies,amplitudes)
plt.plot(fit["x"],fit["y"],"b-")
dreiecka = str("$("+str(np.around(fit["var"][0],2)) + "\\pm" + str(np.around(fit["cov"][0,0],8)) + ")$")
dreieckb = str("$("+str(np.around(fit["var"][1],2)) + "\\pm" + str(np.around(fit["cov"][1,1],8)) + ")\\ \\si{\\volt}$")

amplitudes = list()
for i in range(14,27):
	if(True):
#		print(str('./data/c_' + str(i) + '.csv'))
		amplitudes.append(getAmplitude(np.loadtxt(str('./data/c_' + str(i) + '.csv'),delimiter=',')[:,2]))
plt.plot(1/frequencies[::-1],amplitudes,"rx",label="Meswerte und Fit bei angelegter Sinusspannung")
fit = linearFit(1/frequencies[::-1],amplitudes)
plt.plot(fit["x"],fit["y"],"r-")
sinusa = str("$("+str(np.around(fit["var"][0],2)) + "\\pm" + str(np.around(fit["cov"][0,0],8)) + ")$")
sinusb = str("$("+str(np.around(fit["var"][1],2)) + "\\pm" + str(np.around(fit["cov"][1,1],8)) + ")\\ \\si{\\volt}$")


amplitudes = list()
for i in range(27,40):
	if(True):
#		print(str('./data/c_' + str(i) + '.csv'))
		amplitudes.append(getAmplitude(np.loadtxt(str('./data/c_' + str(i) + '.csv'),delimiter=',')[:,2]))
plt.plot(1/frequencies,amplitudes,"gx",label="Meswerte und Fit bei angelegter Rechtecksspannung")
fit = linearFit(1/frequencies,amplitudes)
plt.plot(fit["x"],fit["y"],"g-")
rechtecka = str("$("+str(np.around(fit["var"][0],2)) + "\\pm" + str(np.around(fit["cov"][0,0],8)) + ")$")
rechteckb = str("$("+str(np.around(fit["var"][1],2)) + "\\pm" + str(np.around(fit["cov"][1,1],8)) + ")\\ \\si{\\volt}$")


#pprint.pprint(fit)
plt.xlabel("$1/f$ [1/kHz]")
plt.ylabel("$U$ [V]")
plt.xlim(0.4,11)
plt.legend()
plt.xscale("log")
plt.yscale("log")
plt.savefig("./results/c/charKurve.pdf")
plt.show()
plt.close()

fitParameter = np.array([["Spannungsfunktion","$a$","$b\\ [\\si{\\volt}]$"],
	["Sinus",sinusa,sinusb],
	["Dreieck",dreiecka,dreieckb],
	["Rechteck",rechtecka,rechteckb]])
#Matrix(VTheorie).generate_tex("./results/a/a_VTheorie")
file = open("./results/c/cFitParameter.tex","w")
file.write(tabulate.tabulate(fitParameter, tablefmt="latex", floatfmt=".2f"))
file.close()

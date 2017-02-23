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

def linearFit(x,y,d):
	def f(x,a,b):
		return b*x**a

	var, cov = optimize.curve_fit(f,x,y,sigma=d,maxfev=10000)
	temp = dict()
	temp["var"] = var
	temp["cov"] = cov
	temp["x"] = np.linspace((min(x)),(max(x)),num=5000)
	temp["y"] = f(temp["x"],var[0],var[1])
	return temp

C = 102.3 * 10**-9
deltaC = 0.02
R = 100
deltaR = 0.01

deltaUa = ( (deltaR)**2 + (deltaC)**2 )**0.5


sinus = np.loadtxt("./data/c_26.csv",delimiter=',')
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(sinus[:,0],sinus[:,1],'r-',label=r"Angelegte Sinusspannung")
ax1.set_ylabel(r"$U_1$/V")
ax1.set_ylim(-0.7,0.7)
ax1.legend(loc="upper left")
for tl in ax1.get_yticklabels():
    tl.set_color('r')
ax2 = ax1.twinx()
ax2.plot(sinus[:,0],sinus[:,2]-getAverage(sinus[:,2]),'b-',label=r"Gemessene Cosinusspannung")
ax2.set_ylabel(r"$U_A$/V")
ax2.set_ylim(-0.5,0.5)
ax2.legend(loc="lower left")
for tl in ax2.get_yticklabels():
    tl.set_color('b')
plt.xlabel("$t$/s")
plt.savefig("./results/c/sinus.pdf")
#plt.show()
plt.close()

rechteck = np.loadtxt("./data/c_27.csv",delimiter=',')
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(rechteck[:,0],-rechteck[:,1],'r-',label=r"Angelegte Rechteckspannung")
ax1.set_ylabel(r"$U_1$/V")
ax1.set_ylim(-0.75,0.75)
ax1.legend(loc="upper left")
for tl in ax1.get_yticklabels():
    tl.set_color('r')
ax2 = ax1.twinx()
ax2.plot(rechteck[:,0],rechteck[:,2]-getAverage(rechteck[:,2]),'b-',label=r"Gemessene Delta-pearks")
ax2.set_ylabel(r"$U_A$/V")
ax2.set_ylim(-13,13)
ax2.legend(loc="lower left")
for tl in ax2.get_yticklabels():
    tl.set_color('b')
plt.xlabel("$t$/s")
plt.savefig("./results/c/rechteck.pdf")
#plt.show()
plt.close()

dreieck = np.loadtxt("./data/c_1.csv",delimiter=',')
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(dreieck[:,0],-dreieck[:,1],'r-',label=r"Angelegte Dreiecksspannung")
ax1.set_ylabel(r"$U_1$/V")
ax1.set_ylim(-0.6,0.6)
ax1.legend(loc="upper left")
for tl in ax1.get_yticklabels():
    tl.set_color('r')
ax2 = ax1.twinx()
ax2.plot(dreieck[:,0],dreieck[:,2]-getAverage(dreieck[:,2]),'b-',label=r"Gemessene Rechteckspannung")
ax2.set_ylabel(r"$U_A$/V")
ax2.set_ylim(-0.65,0.65)
ax2.legend(loc="lower left")
for tl in ax2.get_yticklabels():
    tl.set_color('b')
plt.xlabel("$t$/s")
plt.savefig("./results/c/dreieck.pdf")
#plt.show()
plt.close()

frequencies = np.loadtxt("c_freq.csv")
amplitudes = list()
for i in range(1,14):
	if(True):
#		print(str('./data/c_' + str(i) + '.csv'))
		amplitudes.append(getAmplitude(np.loadtxt(str('./data/c_' + str(i) + '.csv'),delimiter=',')[:,2]))
amplitudes = np.array(amplitudes)
plt.plot(1/frequencies,amplitudes,"bx",label="Meswerte und Fit bei angelegter Dreiecksspannung")
plt.errorbar(1/frequencies,amplitudes,yerr=deltaUa*amplitudes,fmt="bx")
fit = linearFit(1/frequencies,amplitudes,deltaUa*amplitudes)
plt.plot(fit["x"],fit["y"],"b-")
dreiecka = str("("+str(np.around(fit["var"][0],2)) + " $\\pm$ " + str(np.around(fit["cov"][0,0],8)) + ")")
dreieckb = str("("+str(np.around(fit["var"][1],2)) + " $\\pm$ " + str(np.around(fit["cov"][1,1],8)) + ")\\ \\si{\\volt}")

amplitudes = list()
for i in range(14,27):
	if(True):
#		print(str('./data/c_' + str(i) + '.csv'))
		amplitudes.append(getAmplitude(np.loadtxt(str('./data/c_' + str(i) + '.csv'),delimiter=',')[:,2]))
amplitudes = np.array(amplitudes)
plt.plot(1/frequencies[::-1],amplitudes,"rx",label="Meswerte und Fit bei angelegter Sinusspannung")
plt.errorbar(1/frequencies[::-1],amplitudes,yerr=deltaUa*amplitudes,fmt="rx")
fit = linearFit(1/frequencies[::-1],amplitudes,deltaUa*amplitudes)
plt.plot(fit["x"],fit["y"],"r-")
sinusa = str("("+str(np.around(fit["var"][0],2)) + " $\\pm$ " + str(np.around(fit["cov"][0,0],8)) + ")")
sinusb = str("("+str(np.around(fit["var"][1],2)) + " $\\pm$ " + str(np.around(fit["cov"][1,1],8)) + ")\\ \\si{\\volt}")

amplitudes = list()
for i in range(27,40):
	if(True):
#		print(str('./data/c_' + str(i) + '.csv'))
		amplitudes.append(getAmplitude(np.loadtxt(str('./data/c_' + str(i) + '.csv'),delimiter=',')[:,2]))
amplitudes = np.array(amplitudes)
plt.plot(1/frequencies,amplitudes,"gx",label="Meswerte und Fit bei angelegter Rechtecksspannung")
plt.errorbar(1/frequencies,amplitudes,yerr=deltaUa*amplitudes,fmt="gx")
fit = linearFit(1/frequencies,amplitudes,deltaUa*amplitudes)
plt.plot(fit["x"],fit["y"],"g-")
rechtecka = str("("+str(np.around(fit["var"][0],2)) + " $\\pm$ " + str(np.around(fit["cov"][0,0],8)) + ")")
rechteckb = str("("+str(np.around(fit["var"][1],2)) + " $\\pm$ " + str(np.around(fit["cov"][1,1],8)) + ")\\ \\si{\\volt}")


#pprint.pprint(fit)
plt.xlabel("$\\frac{1}{f}$ /$10^3$ s")
plt.ylabel("$U_A$/V")
plt.xlim(0.4,11)
plt.legend()
plt.xscale("log")
plt.yscale("log")
plt.savefig("./results/c/charKurve.pdf")
plt.show()
plt.close()

fitParameter = np.array([["Spannungsfunktion","$a$","$b/\\si{\\volt}]$"],
	["Sinus",sinusa,sinusb],
	["Dreieck",dreiecka,dreieckb],
	["Rechteck",rechtecka,rechteckb]])
#Matrix(VTheorie).generate_tex("./results/a/a_VTheorie")
file = open("./results/c/cFitParameter.tex","w")
file.write(tabulate.tabulate(fitParameter, tablefmt="latex", floatfmt=".2f"))
file.close()

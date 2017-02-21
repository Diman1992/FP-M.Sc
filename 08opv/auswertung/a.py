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
#from pylatex import Matrix

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
	y = np.array(y)
	def f(x,a,b):
		return b*x**a

	var, cov = optimize.curve_fit(f,(x[x >minimum]),(y[x > minimum]),maxfev=10000)
	temp = dict()
	temp["var"] = var
	temp["cov"] = cov
	temp["x"] = np.linspace((min(x[x > minimum])),(max(x[x > minimum])),num=5000)
	temp["y"] = f(temp["x"],var[0],var[1])
	return temp

def constFit(x,y,maximum):
	x = np.array(x)
	y = np.array(y)
	def f(x,c):
		return c

	var, cov = optimize.curve_fit(f,(x[x <maximum]),(y[x < maximum]),maxfev=10000)
	return var[0]


pi = np.pi

frequencies = np.loadtxt('a_freq.csv', delimiter=',')
thresholds = np.loadtxt('a_thresholds.csv')
amplitudes = list()
R1 = 100
Rn = [1000,500,10000,330]
Uein = 20

VTheorie = np.array([["$R_n$ [$\\Omega$]","$R_1$ [$\\Omega$]","$V_\\text{Theorie}$"],[Rn[0],R1,Rn[0]/R1],[Rn[1],R1,Rn[1]/R1],[Rn[2],R1,Rn[2]/R1],[Rn[3],R1,Rn[3]/R1]])
#Matrix(VTheorie).generate_tex("./results/a/a_VTheorie")
file = open("./results/a/a_VTheorie.tex","w")
file.write(tabulate.tabulate(VTheorie, tablefmt="latex", floatfmt=".2f"))
file.close()

aTable = np.array(
	["$R_n$ [$\\Omega$]",
	"$a$","$\\Delta a$",
	"b [V]","$\\Delta$b [V]",
	"$V_\\text{Real}$",
	"$f_\\text{Grenz}$ [kHz]","$\\Delta f_\\text{Grenz}$ [kHz]", 
	"$V_\\text{Real} \\cdot f_\\text{Grenz}$ [kHz]",
	"$V_\\text{Leerlauf}$"])

Rn = 1000
print("Rn = 1000")
for i in range(1,26):
	if(i != 12):
#		print(str('./data/scope_' + str(i) + '.csv'))
		amplitudes.append(getAmplitude(np.loadtxt(str('./data/scope_' + str(i) + '.csv'),delimiter=',')[:,2]))
plt.plot(frequencies[frequencies != 10],amplitudes,'bx',label=r"Messwerte und Fit für R=1000 $\Omega$")
fit = linearFit(frequencies[frequencies != 10], amplitudes, thresholds[0,2])
plt.plot(fit["x"], fit["y"], 'b-')

a = fit["var"][0]
deltaa = fit["cov"][0,0]
b = fit["var"][1]
deltab = fit["cov"][1,1]
Vreal = constFit(frequencies[frequencies != 10], amplitudes, thresholds[0,1])
Vfgrenz = Vreal/2**0.5
fgrenz = (Vfgrenz/b)**(1/a)
deltafgrenz = ( ( -(Vfgrenz/b)**(1/a)/a**2 * np.log(Vfgrenz/b) * deltaa )**2 + ( -(Vfgrenz/b)**(1/a)/a/b * deltab )**2 )**0.5
Vf = fgrenz * Vreal
Vleerlauf = (1/Vreal - R1/Rn)
bla = np.array([Rn,np.around(a,2),np.around(deltaa,4),np.around(b,2),np.around(deltab,3),np.around(Vreal,2),np.around(fgrenz,2),np.around(deltafgrenz,2),np.around(Vf,2),np.around(Vleerlauf,2)])
aTable = np.vstack((aTable,bla))


#pprint.pprint(fit)

Rn = 500
print("Rn = 500")
amplitudes = list()
for i in range(26,51):
	if(True):
#		print(str('./data/scope_' + str(i) + '.csv'))
		amplitudes.append(getAmplitude(np.loadtxt(str('./data/scope_' + str(i) + '.csv'),delimiter=',')[:,2]))
plt.plot(frequencies[::-1],amplitudes,'rx',label=r"Messwerte und Fit für R=500 $\Omega$")
fit = linearFit(frequencies[::-1], amplitudes, thresholds[1,2])
plt.plot(fit["x"], fit["y"], 'r-')

a = fit["var"][0]
deltaa = fit["cov"][0,0]
b = fit["var"][1]
deltab = fit["cov"][1,1]
Vreal = constFit(frequencies, amplitudes, thresholds[1,1])
Vfgrenz = Vreal/2**0.5
fgrenz = (Vfgrenz/b)**(1/a)
deltafgrenz = ( ( -(Vfgrenz/b)**(1/a)/a**2 * np.log(Vfgrenz/b) * deltaa )**2 + ( -(Vfgrenz/b)**(1/a)/a/b * deltab )**2 )**0.5
Vf = fgrenz * Vreal
Vleerlauf = (1/Vreal - R1/Rn)
bla = np.array([Rn,np.around(a,2),np.around(deltaa,4),np.around(b,2),np.around(deltab,3),np.around(Vreal,2),np.around(fgrenz,2),np.around(deltafgrenz,2),np.around(Vf,2),np.around(Vleerlauf,2)])
aTable = np.vstack((aTable,bla))


Rn = 10000
print("Rn = 10000")
amplitudes = list()
for i in range(51,76):
	if(True):
#		print(str('./data/scope_' + str(i) + '.csv'))
		amplitudes.append(getAmplitude(np.loadtxt(str('./data/scope_' + str(i) + '.csv'),delimiter=',')[:,2]))
plt.plot(frequencies,amplitudes,'gx',label=r"Messwerte und Fit für R=10000 $\Omega$")
fit = linearFit(frequencies, amplitudes, thresholds[2,2])
plt.plot(fit["x"], fit["y"], 'g-')

a = fit["var"][0]
deltaa = fit["cov"][0,0]
b = fit["var"][1]
deltab = fit["cov"][1,1]
Vreal = constFit(frequencies, amplitudes, thresholds[2,1])
Vfgrenz = Vreal/2**0.5
fgrenz = (Vfgrenz/b)**(1/a)
deltafgrenz = ( ( -(Vfgrenz/b)**(1/a)/a**2 * np.log(Vfgrenz/b) * deltaa )**2 + ( -(Vfgrenz/b)**(1/a)/a/b * deltab )**2 )**0.5
Vf = fgrenz * Vreal
Vleerlauf = (1/Vreal - R1/Rn)
bla = np.array([Rn,np.around(a,2),np.around(deltaa,4),np.around(b,2),np.around(deltab,3),np.around(Vreal,2),np.around(fgrenz,2),np.around(deltafgrenz,2),np.around(Vf,2),np.around(Vleerlauf,2)])
aTable = np.vstack((aTable,bla))

Rn = 330
print("Rn = 330")
amplitudes = list()
for i in range(76,101):
	if(True):
#		print(str('./data/scope_' + str(i) + '.csv'))
		amplitudes.append(getAmplitude(np.loadtxt(str('./data/scope_' + str(i) + '.csv'),delimiter=',')[:,2]))
plt.plot(frequencies[::-1],amplitudes,'kx',label=r"Messwerte und Fit für R=330 $\Omega$")
fit = linearFit(frequencies[::-1], amplitudes, thresholds[3,2])
plt.plot(fit["x"], fit["y"], 'k-')

a = fit["var"][0]
deltaa = fit["cov"][0,0]
b = fit["var"][1]
deltab = fit["cov"][1,1]
Vreal = constFit(frequencies, amplitudes, thresholds[3,1])
Vfgrenz = Vreal/2**0.5
fgrenz = (Vfgrenz/b)**(1/a)
deltafgrenz = ( ( -(Vfgrenz/b)**(1/a)/a**2 * np.log(Vfgrenz/b) * deltaa )**2 + ( -(Vfgrenz/b)**(1/a)/a/b * deltab )**2 )**0.5
Vf = fgrenz * Vreal
Vleerlauf = (1/Vreal - R1/Rn)
bla = np.array([Rn,np.around(a,2),np.around(deltaa,4),np.around(b,2),np.around(deltab,3),np.around(Vreal,2),np.around(fgrenz,2),np.around(deltafgrenz,2),np.around(Vf,2),np.around(Vleerlauf,2)])
aTable = np.vstack((aTable,bla))

plt.xlabel(r"$f$ [kHz]")
plt.ylabel(r"$U$ [V]")
plt.xscale('log')
plt.yscale('log')
plt.legend(loc="upper right",prop={'size':10})
plt.savefig("./results/a/a.pdf")
#plt.show()
#plt.close()

#Matrix(aTable).generate_tex("./results/a/a_VReal")

aTable = np.transpose(aTable)
file = open("./results/a/a_VReal.tex","w")
file.write(tabulate.tabulate(aTable, tablefmt="latex"))#, floatfmt="{.2f}"))
file.close()

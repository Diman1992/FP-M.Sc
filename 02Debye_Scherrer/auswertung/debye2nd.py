#!/usr/bin/env python3

import numpy as np
from scipy import stats
import matplotlib.pylab as plt
import matplotlib as mpl
from matplotlib import rc
from scipy import optimize, interpolate, misc, constants
import os
import sys
import re
import scipy.optimize as optimization
import math
import matplotlib.cm as cm

def sortArrayUpways(arr):
	n = len(arr)
	for i in range(0,n):
		for j in range(0,n):
			if(arr[i]<arr[j]):
				temp = arr[j]
				arr[j] = arr[i]
				arr[i] = temp

def killmultiples(arr):
	n = len(arr)
	for i in range(0,n):
		ind = arr[i]
		for j in range(0,n):
			if(arr[j]==arr[i]):
				arr[j] = 0
				print(arr)
		
	

#####parameter
R = 57.4
F = 130
rho = 1
lamda = 1.5417e-10

####Messwerte
r1_mess = np.array([45,65,81,97,114,135,157])
r2_mess = np.array([28,39,48,56,63,69,83,89,95,102,114,122,148,163]) #original [28,39,48,56,63,69,83,89,95,102,114,122,148,163]
r2_mess = r2_mess+3
####Theory filling for fcc and bcc
fcc = list()
bcc = list()

N = 0
for h in range(0,8):
	for k in range(0,8):
		for l in range(0,8):
#			if(len(fcc)<len(r2_mess)):
				if((h%2==0 and k%2==0 and l%2==0) or (h%2==1 and k%2==1 and l%2==1)):
					N = h**2+k**2+l**2
					fcc.append(N) 
#			if(len(bcc)<len(r1_mess)):
				if((h+k+l)%2==0):
					N = h**2+k**2+l**2
					bcc.append(N)


sortArrayUpways(bcc)
sortArrayUpways(fcc)

print(bcc)
print(fcc)

bcc1=np.array([2,4,6,8,10,12,14])
fcc1=np.array([3,4,8,11,12,16,19])
bcc2=np.array([2,4,6,8,10,12,14,16,18,20,22,24,26,30])#,32,34,36,38])
fcc2=np.array([3,4,8,11,12,16,19,20,24,27,32,35,36,40])#,43,44,48,51])

#####Winkel
theta1 = r1_mess/(2*R)
theta2 = r2_mess/(2*R)
costheta1 = np.cos(theta1)**2
costheta2 = np.cos(theta2)**2

#####Structure? Compare theory with measures
s1_expbcc = bcc1[0]/np.sin(theta1[0])**2 * np.sin(theta1)**2
s1_expfcc = fcc1[0]/np.sin(theta1[0])**2 * np.sin(theta1)**2
s2_expbcc = bcc2[0]/np.sin(theta2[0])**2 * np.sin(theta2)**2
s2_expfcc = fcc2[0]/np.sin(theta2[0])**2 * np.sin(theta2)**2

print("bcc0",bcc1[0])
print("sin0",np.sin(theta1[0])**2)
print("sini",np.sin(theta1)**2)

print("th_bcc1",bcc1)
print("ex_bcc1",s1_expbcc)
print("diffbcc",np.sum(abs(s1_expbcc-bcc1))/len(r1_mess))
print("th_fcc1",fcc1)
print("ex_fcc1",s1_expfcc)
print("difffcc",np.sum(abs(s1_expfcc-fcc1))/len(r1_mess))

print("th_bcc2",bcc2)
print("ex_bcc2",s2_expbcc)
print("diffbcc",np.sum(abs(s2_expbcc-bcc2))/len(r2_mess))
print("th_fcc2",fcc2)
print("ex_fcc2",s2_expfcc)
print("difffcc",np.sum(abs(s2_expfcc-fcc2))/len(r2_mess))



#netzebenen
a1 = lamda/2*np.sin(theta1) * np.sqrt(bcc1)
a2 = lamda/2*np.sin(theta2) * np.sqrt(fcc2)

a1 = a1*10**10
a2 = a2*10**10
print("mean a1",np.mean(a1))
print("mean a2",np.mean(a2))



#fit
cosSquare1 = np.cos(theta1)**2
cosSquare2 = np.cos(theta2)**2
print(len(a1),len(cosSquare1))
slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(cosSquare1,a1)

slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(cosSquare2,a2)
print("m1 = "+str(slope1), "b1 = "+str(intercept1), "MgS: 520 (falsche Farbe), BaO: 554, SrO: 516, LiBr: 550, KF: 534", r_value1, p_value1, std_err1)
print("m2 = "+str(slope2), "b2 = "+str(intercept2), "MgS: 520 (falsche Farbe), BaO: 554, SrO: 516, LiBr: 550, KF: 534", r_value2, p_value2, std_err2)

#plot
x = np.linspace(0,1,100)
fit1 = slope1*x+intercept1
fit2 = slope2*x+intercept2

fig = plt.figure()
ax = plt.gca()

plt.xlim((0,1))
plt.xlabel(r"cos$^2 (\theta)$")
plt.ylabel("Gitterparameter $a$")

i=2
if (i==1):
	plt.plot(x,fit1)
	plt.title("Korrektur zum Gitterparameter des Metalls")
	ax.scatter(cosSquare1, a1)
	plt.savefig("a1",dpi=100)
if (i==2):
	plt.plot(x,fit2)
	plt.title("Korrektur zum Gitterparameter des Salzes")
	ax.scatter(cosSquare2, a2)
	plt.savefig("a2",dpi=100)



plt.show()



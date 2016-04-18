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

############
# bcc: h+k+l gerade
# fcc: h+k+l alle gerade oder ungerade
############

#####parameter
R = 57.4
F = 130
rho = 1
lamda = 1.5417e-7

#####Messwerte
r1_mess = np.array([32.0,44.0,53.0, 65.0,81.0])
r21_mess = np.array([34.0,46.0,56.0,61.0,65.0,74.0,78.0])
r21_mess = np.pi*R-r21_mess #möglicherweise geshiftet um viertel Umfang
r22_mess = np.array([31.0,38.0,44.0,51.0,65.0,69.0,74.0])
r2_mess = np.concatenate([r21_mess, r22_mess])
sortArrayUpways(r2_mess)
print("r1: ",r1_mess)
print("r2: ",r2_mess)


#####Miller-Indizes
h1 = np.array([1,1,1,2,2])
k1 = np.array([0,1,1,0,1])
l1 = np.array([0,0,1,0,0])
h2 = np.array([1,2,2,3,4,3,4,5,6,6,5,6,4,5])
k2 = np.array([0,1,2,1,0,3,2,3,0,2,4,2,4,5])
l2 = np.array([0,1,0,0,0,0,0,0,0,0,1,2,4,1])

#####Winkel
theta1 = r1_mess/(2*R)
theta1_0 = theta1[0]
theta2 = r2_mess/(2*R)
theta2_0 = theta2[0]
print("Winkel1: ",theta1)

#####Strukturfaktoren
s_exp1 = (np.sin(theta1))**2/(np.sin(theta1_0))**2
s_theo1 = h1**2 + k1**2 + l1**2
#1 = bcc
s_exp2 = (np.sin(theta2))**2/(np.sin(theta2_0))**2 #theta/2 laut V5-Gitterkonstantenbestimmung - sonst für theta>90 grad
s_theo2 = h2**2 + k2**2 + l2**2
#2 = fcc
print("se1(bcc): ", s_exp1)
print("se2(fcc): ", s_exp2)
print("st1: ", s_theo1)
print("st2: ", s_theo2)

#####Gitterkonstante
d1 = lamda/(2*np.sin(theta1))
d2 = lamda/(2*np.sin(theta2))
a1 = d1 * np.sqrt(s_theo1)
a2 = d2 * np.sqrt(s_theo2) 

print("a1-mean: ", np.mean(a1))
print("a2-mean: ", np.mean(a2))
cosSquare1 = np.cos(theta1)**2
cosSquare2 = np.cos(theta2)**2
a1 = a1*10**7
a2 = a2*10**7

slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(cosSquare1,a1)
slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(cosSquare2,a2)
print("m1 = "+str(slope1), "b1 = "+str(intercept1), "MgS: 520 (falsche Farbe), BaO: 554, SrO: 516, LiBr: 550, KF: 534", r_value1, p_value1, std_err1)
print("m2 = "+str(slope2), "b2 = "+str(intercept2), "Yb: 548, Sn: 583 (centerced tetragonal!), Sr: 608, Ge: 565" , r_value2, p_value2, std_err2)
x = np.linspace(0,1,100)
fit1 = slope1*x+intercept1
fit2 = slope2*x+intercept2

fig = plt.figure()
ax = plt.gca()

####output
f = open('workfile','w')
f.write("r1\ttheta\tsexp\tstheo\tmiller\ta\n")
for i in range(0,len(a1)):
	f.write(str(round(r1_mess[i],2))+ "\t" + str( round(theta1[i],2)) + "\t" +  str( round(s_exp1[i],2)) +  "\t" + str(round(s_theo1[i],2)) +  "\t" + str(h1[i])+str(k1[i])+str(l1[i]) +str("\t") + str(round(a1[i],2)))
	f.write("\n")

f.write("\n\n\n")
f.write("r2\ttheta\tsexp\tstheo\tmiller\ta\n")
for i in range(0,len(a2)):
	f.write(str(round(r2_mess[i],2))+ "\t" + str( round(theta2[i],2)) + "\t" +  str( round(s_exp2[i],2)) +  "\t" + str(round(s_theo2[i],2)) +  "\t" + str(h2[i])+str(k2[i])+str(l2[i]) +str("\t")+ str(round(a2[i],2)))
	f.write("\n")

f.close()

plt.plot(x,fit1)
plt.xlim((0,1))
plt.title("Korrektur zum Gitterparameter der ersten Probe")
plt.xlabel(r"cos$^2 (\theta)$")
plt.ylabel("Gitterparameter $a$")
#plt.legend(loc=2)
#plt.plot(x,fit2)
ax.scatter(cosSquare1, a1)
#plt.savefig("a1",dpi=100)

#ax.scatter(cosSquare2, a2)
#plt.savefig("a2",dpi=100)
plt.show()


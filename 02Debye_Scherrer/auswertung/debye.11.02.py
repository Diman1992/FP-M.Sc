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

def isInList(arr, j):
	n = len(arr)
	for i in range(0,n):
		if(arr(i) == j): return True
	return False

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

#Miller-Indizes:
Nfcc = list()
Nbcc = list()
fcc = list()
bcc = list()  #wie NaCl (außer wenn f1 = f2; dann nur h+k+l gerade)

fcc.append(0)
bcc.append(0)

N = 0
for h in range(0,5):
	for k in range(0,5):
		for l in range(0,5):
			if((h%2==0 and k%2==0 and l%2==0) or (h%2==1 and k%2==1 and l%2==1)):
				N = h**2+k**2+l**2
				fcc.append(N) 
			if((h+k+l)%2==0):
				N = h**2+k**2+l**2
				bcc.append(N)


fcc = np.array([3,4,11,12,24])#16,19,20,24,27,32])#36]) 

print(fcc)
#####Winkel
theta1 = r1_mess/(2*R)
theta2 = r2_mess/(2*R)

costheta1 = np.cos(theta1)**2
costheta2 = np.cos(theta2)**2

#netzebenen
a1fcc = lamda/2*np.sin(theta1) * fcc
#a1bcc = lamda/2*np.sin(theta1) * bcc



print("r1: ", r1_mess)
print("th: ", theta1)
print("cos2: ", costheta1)
print("a1fcc: ", a1fcc)

plt.plot(costheta1, a1fcc)
plt.show()













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


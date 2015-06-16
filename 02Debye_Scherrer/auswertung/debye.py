#!/usr/bin/env python3

import numpy as np
import matplotlib.pylab as plt
import matplotlib as mpl

def findLowest(theta):
	n = len(theta)
	theta_0 = theta[0]
	for i in range(1,n-1):
		if(theta[i]<theta_0):
			theta_0 = theta[i]	
	return theta_0


def sortArrayUpways(arr):
	n = len(arr)
	for i in range(0,n):
		for j in range(0,n):
			if(arr[i]<arr[j]):
				temp = arr[j]
				arr[j] = arr[i]
				arr[i] = temp

R = 57.4
lamda = 1.5417e-7
r_mess = np.array([32.0,39.5,50.5,53.0, 68.5])
sortArrayUpways(r_mess)

theta = r_mess/(2*R)

theta_0 = theta[0]
s_exp = 4*(np.sin(theta))**2/(np.sin(theta_0))**2
#s_theo = 

a = np.sqrt(s_exp)*lamda/np.sin(theta)


print(s_exp)
print(a)

##test
t = np.linspace(1,4,100)
s = np.sin(t)**2/np.sin(t[0])**2


fig = plt.figure()
ax = plt.gca()
ax.scatter(t, s)
#plt.show()


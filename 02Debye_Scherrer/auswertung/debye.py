#!/usr/bin/env python3

import numpy as np
import matplotlib.pylab as plt
import matplotlib as mpl

def sortArrayUpways(arr):
	n = len(arr)
	for i in range(0,n):
		for j in range(0,n):
			if(arr[i]<arr[j]):
				temp = arr[j]
				arr[j] = arr[i]
				arr[i] = temp
#####parameter
R = 57.4
lamda = 1.5417e-7

#####messwerte
r1_mess = np.array([32.0,44.0,53.0, 65.0,81.0])
r21_mess = np.array([34.0,46.0,56.0,61.0,65.0,74.0,78.0])
r21_mess = np.pi*R-r21_mess #möglicherweise geshiftet um viertel Umfang
r22_mess = np.array([31.0,38.0,44.0,51.0,65.0,69.0,74.0])
rReal2_mess = np.concatenate([r21_mess, r22_mess])
#rReal2_mess = np.array([124.0,136.0,146.0,151.0,155.0,164.0,168.0,31.0,38.0,44.0,51.0,65.0,69.0,74.0])
sortArrayUpways(rReal2_mess)
print("rReal ", rReal2_mess)

#####s-theorie
h1 = np.array([2,2,3,3,3])
k1 = np.array([0,2,1,2,3])
l1 = np.array([0,0,0,0,2])
h21 = np.array([2,2,3,2,3,4,3])
k21 = np.array([0,2,1,2,2,1,3])
l21 = np.array([0,0,0,2,1,0,1])
h22 = np.array([2,2,2,3,4,3,4])
k22 = np.array([0,1,2,1,0,3,2])
l22 = np.array([0,1,0,0,0,0,0])

#####Winkel
theta1 = r1_mess/(2*R)
theta1_0 = theta1[0]
theta21 = r21_mess/(2*R)
theta21_0 = theta21[0]
theta22 = r22_mess/(2*R)
theta22_0 = theta22[0]
thetaReal = rReal2_mess/(2*R)
thetaReal0 = thetaReal[0]
print("theta", theta21)

#####Strukturfaktoren
s_exp1 = 4*(np.sin(theta1))**2/(np.sin(theta1_0))**2
s_theo1 = h1**2 + k1**2 + l1**2
s_exp21 = 4*(np.sin(theta21))**2/(np.sin(theta21_0))**2
s_theo21 = h21**2 + k21**2 + l21**2
s_exp22 = 4*(np.sin(theta22))**2/(np.sin(theta22_0))**2
s_theo22 = h22**2 + k22**2 + l22**2
s_expReal = 4*(np.sin(thetaReal))**2/(np.sin(thetaReal0))**2

#a = np.sqrt(s_exp)*lamda/np.sin(theta1)


print("s_exp1: ",s_exp1)
print("s_theo1: ",s_theo1)
print("s_exp21: ",s_exp21)
print("s_theo21: ",s_theo21)
print("s_exp22: ",s_exp22)
print("s_theo22: ",s_theo22)
print("SULtimate", s_expReal)

##test
t = np.linspace(1,4,100)
s = np.sin(t)**2/np.sin(t[0])**2


fig = plt.figure()
ax = plt.gca()
ax.scatter(t, s)
#plt.show()


#####Faktorprüfung

for i in range(0,len(h1)):
	if((h1[i] + k1[i] + l1[i])%2 ==0):
		print("1: True")
	else:
		print("1: False")

for i in range(0,len(h2)):
	if(h2[i]%2==0 and k2[i]%2==0 and l2[i]%2==0):
		print("2: True")
	elif((h2[i]%2!=0 or h2[i]==0) and (k2[i]%2!=0 or k2[i]==0) and (l2[i]%2!=0 or l2[i]==0)):
		print("2: True")
	else:
		print("2: False")



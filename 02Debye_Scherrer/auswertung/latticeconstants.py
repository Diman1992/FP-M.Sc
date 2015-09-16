import numpy as np

def sortArrayUpways(arr):
	n = len(arr)
	for i in range(0,n):
		for j in range(0,n):
			if(arr[i]<arr[j]):
				temp = arr[j]
				arr[j] = arr[i]
				arr[i] = temp

lattice = list()
indextriple = 0
maxindex = 7

for h in range(0,maxindex+1):
	for k in range(0,maxindex+1):
		for l in range(0,maxindex+1):
			lattice.append(h**2+k**2+l**2)
			#if(h**2+k**2+l**2==indextriple):
			print(h,k,l,h**2+k**2+l**2)

sortArrayUpways(lattice)
#print(lattice)

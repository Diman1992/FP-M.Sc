import numpy as np

def sortArrayUpways(arr):
	n = len(arr)
	for i in range(0,n):
		for j in range(0,n):
			if(arr[i][0]<arr[j][0]):
				temp = arr[j][0]
				arr[j][0] = arr[i][0]
				arr[i][0] = temp

lattice = list()
indextriple = 0
maxindex = 7

for h in range(0,maxindex+1):
	for k in range(0,maxindex+1):
		for l in range(0,maxindex+1):
			inter = np.array([h**2+k**2+l**2,h+k+l])
			lattice.append(inter)
			#if(h**2+k**2+l**2==indextriple):
			if((h%2==0 and k%2==0 and l%2==0) or (h%2==1 and k%2==1 and l%2==1)):
				print(h,k,l,h**2+k**2+l**2)

sortArrayUpways(lattice)
#print(lattice[3][2])
print(lattice)

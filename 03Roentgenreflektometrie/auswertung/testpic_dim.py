import numpy as np
import matplotlib.pylab as plt

n1 = 1
n2 = 1-1e-6
n3 = 1-2e-6

s1 = 8e-10
s2 = 3e-10

z2 = 500e-10

ai = np.linspace(0.25,0.7,num=1e5)
ai = ai*np.pi/180

qz = 4*np.pi/1.54*np.sin(ai)

k = 2*np.pi/1.54*1e-10

kz1 = k * np.sqrt(n1**2-np.cos(ai)**2)
kz2 = k * np.sqrt(abs(n2**2-np.cos(ai)**2))
kz3 = k * np.sqrt(abs(n3**2-np.cos(ai)**2))

r12 = (kz1-kz2)/(kz1+kz2) * np.exp(-2*kz1*kz2*s1**2)
r23 = (kz2-kz3)/(kz2+kz3) * np.exp(-2*kz2*kz3*s1**2)
x2 = np.exp(-2j*kz2*z2) * r23
x1 = (r12+x2)/(1+r12*x2)

fig = plt.figure()
ax = plt.gca()
ax.set_yscale("log")

ax.scatter(qz,abs(x1)**2)
plt.show()

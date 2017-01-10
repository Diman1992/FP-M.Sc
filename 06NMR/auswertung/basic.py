#!/usr/bin/python3
# -*- coding: utf-8 -*-

output_silent = True

import numpy as np
from scipy import optimize, interpolate, misc, stats, constants
import os, sys
for arg in sys.argv:
	if arg=='silent': output_silent = True
sys.path.append("./scripts")
from latex_array import latex_array
from latex_number import latex_number
from load_strings import load_strings
from linregress import linregress
from plotting import *
from scipy import signal
from random import random
import uncertainties as uc
#########################################
# Preparation				#
#########################################

def f(x, U_0, T2):
    return U_0 * np.exp(-x / T2)

def p(p_var):
        print(p_var+" = "+'\n'+str(eval(p_var))+'\n')
	
# create 'results' - folders
if ( not os.path.exists('results')):
	os.mkdir('results')
	
tt1, Ut1 = np.loadtxt("Data_T_1.txt", unpack = True)
#tt1, Ut1 = np.loadtxt("nmrT1", unpack = True)
tt2, Ut2 = np.loadtxt("MG_2.csv", unpack = True)#,delimiter=",")
tD, UD = np.loadtxt("diffusion",unpack = True)
tD = tD/1000 # tD in ms



# carr-purcell data
tcp, Ucp = np.loadtxt("data/cp2.csv", unpack=True,delimiter=",")
Ucp = 2*Ucp[-0.01 < tcp]
tcp = tcp[-0.01 < tcp]
Ucp = Ucp[tcp < 1.0]
tcp = tcp[tcp < 1.0]


gradWidth, tGrad = np.loadtxt("gradWidth",unpack = True)


Ut2 = Ut2[-0.12 <= tt2]
tt2 = tt2[-0.12 <= tt2]
Ut2 = Ut2[tt2 < 1.63]
tt2 = tt2[tt2 < 1.63]

Ut2max = signal.argrelmax(Ut2)
Ut2max = np.array(Ut2max)
Ut2max = Ut2max[Ut2[Ut2max] > 0.5]
Ut2max = Ut2max[2::2]

#########################################
# Analysis				#
#########################################


def Ft1(tau, m):
    return m*tau
    
Mt1 = (Ut1[0]+Ut1)/(2*Ut1[0])
t1Log = np.log(Mt1)
selectindex = tt1.tolist().index(1.0)
p('t1Log')
#m,merr,b,berr = linregress(tt1,t1Log)

var1,cov1 = optimize.curve_fit(Ft1,tt1[1:],t1Log[1:])
m = var1[0]
merr = np.sqrt(cov1[0][0])

t1 = -1/m
t1_err = 1/(m**2)*merr
p('t1')
p('m')
p('merr')

merr = 0.001

p('Ut2[Ut2max]')

t1 = -1/m
t1_err = 1/(m**2)*merr

alen = len(tt1)
latex_array("results/T1_tab.res",np.array([tt1[:(alen/2)],Ut1[:(alen/2)],tt1[(alen/2):],Ut1[(alen/2):]]),transpose=True,format=['{:.2f}','{:.3f}','{:.2f}','{:.3f}'])
latex_array("results/T1_tab_new.res",np.array([tt1,Ut1]),transpose=True,format=['{:.2f}','{:.3f}'])
m_t,m_t_err,ex = latex_number("results/m.res",m,merr,unit="r\second^-1",exponent = 0)
T1_t, T1_t_err, ex = latex_number("results/T1.res", t1, t1_err, unit=r"\second",exponent = 0)

var, cov = optimize.curve_fit(f, tt2[Ut2max], Ut2[Ut2max])
U_0 = var[0]
U_0_err = np.sqrt(cov[0][0])
U0_t, U0_t_err, ex = latex_number("results/T2_M0.res", U_0, U_0_err, unit=r"\volt", exponent=0)
T2 = var[1]
T2_err = np.sqrt(cov[1][1])
T2_t, T2_t_err, ex = latex_number("results/T2.res", T2, T2_err, unit=r"\second", exponent= 0)

##### Berechnung der Halbwertsbreite #####

halfwidth = np.mean(gradWidth)
halfwidth_err = np.std(gradWidth)

p('halfwidth')
p('halfwidth_err')

uhalf = uc.ufloat(halfwidth,halfwidth_err)

latex_number("../auswertung/results/halfwidth.res",halfwidth,halfwidth_err, unit=r"\micro\second")
latex_array("../auswertung/results/halfw_tab.res",np.array([gradWidth,tGrad]),transpose=True,format=['{:.0f}','{:.0f}'])

##########Diffusion####
#T_2 = 1.42
#t_05 = 0.000112


UD0 = -0.99
#UD0 = 2.483
d= 0.0044#probendurchmesser
gG = 8.8/(d*(halfwidth*10**(-6)))
ugG = 8.8/(d*(uhalf*10**(-6)))

p('ugG')
Mdiff = np.log(UD/UD0) + (tD)/T2

def fdiff(tau, m):
    return m*tau

var, cov = optimize.curve_fit(fdiff, (tD)**3, Mdiff, maxfev=100000)


mdiff = var[0]
mdifferr = np.sqrt(cov[0][0])
p('mdiff')
p('mdifferr')

umdiff = uc.ufloat(mdiff,mdifferr)
p('umdiff')
D = -12*mdiff/(gG**2)
uD = -12*umdiff/(ugG**2)
p('D')
p('uD')


latex_number("results/mdiff.res",umdiff.nominal_value,umdiff.std_dev,exponent = 5,unit=r"\meter\second^{-3}")
latex_number("results/D.res",uD.nominal_value,uD.std_dev,exponent = -9,unit=r"\meter^2\per\second")

alen = len(tD)
latex_array("results/diff_tab.res",np.array([1000*tD[:alen/2],UD[:alen/2],1000*tD[alen/2:],UD[alen/2:]]),transpose=True,format=['{:.0f}','{:.2f}','{:.0f}','{:.2f}'])



###Stokes

#fallzeit
t0 = 918 #s
alpha = 1.024*10**(-9) #m^2/s^2
#interpol
deltavis = 0.5-(t0-900)/100* 0.1
#rho wasser T = 295
rhowasser = 997.77 #kg/m^3
eta = rhowasser * alpha*(t0 - deltavis)

p('eta')
p('deltavis')


k = 1.3806488*pow(10,-23)
T = 295

r = (k*T)/(6*np.pi*eta*uD.nominal_value)*pow(10,10) # in angström
r_Err = (k*T)/(6*np.pi*eta*pow(D,2))*uD.std_dev*pow(10,10) # in angström

latex_number("results/stokes_r.res",r,r_Err, unit = r"\angstrom", exponent = 0)
latex_number("results/eta.res",round(eta,6),None,exponent = -6)

#########################################
# Plotting / Saving			#
#########################################

off = Ucp[tcp<0.0]
offset= sum(off)/len(off)
Ucp = Ucp-offset

off = Ut2[tt2<0.0]
offset= sum(off)/len(off)
Ut2 = Ut2-offset

t_l = np.linspace(min(tt2), max(tt2), 100)


freesize = 418.25555 #pt ; obtain via \showthe\columnwidth in latex
fig, ax = init_plot(freesize)
ax.set_xlabel(r'$t / \si{\second}$')
ax.set_ylabel(r'$U / \si{\volt}$')
ax.plot(tt2, Ut2, lw=0.4)
ax.plot(tt2[Ut2max], Ut2[Ut2max], "rx", markersize=3, lw=0.4, label="Maxima")
ax.plot(t_l, f(t_l, U_0, T2), "g--", lw=0.4, label=
        "Fit: $" + U0_t + r"\cdot e^{\frac{-t}{" + T2_t + "}}$")
ax.set_xlim(min(tt2), max(tt2))
pretty_plot(ax)
fig.savefig('results/T2.pdf')
if not output_silent: plt.show()
if not output_silent: plt.close()
plt.clf()

fig, ax = init_plot(freesize)
ax.set_xlabel(r"$t / \si{\second}$")
ax.set_ylabel(r"$U / \si{\volt}$")
ax.plot(tcp, Ucp)
ax.set_xlim(min(tcp), max(tcp))
ax.set_ylim(1.01*min(Ucp),1.01*max(Ucp))
pretty_plot(ax)
fig.savefig('results/T2_carr_purcell.pdf')
if not output_silent: plt.show()
if not output_silent: plt.close()
plt.clf()

t_l1 = np.linspace(min(tt1),max(tt1),100)
fig, ax = init_plot(freesize)
ax.set_xlabel(r't[s]')
ax.set_ylabel(r'$\ln(\frac{M_0 - M_z}{2M_0})$')

ax.plot(tt1,t1Log,"x",label="Messwerte")
ax.plot(t_l1,Ft1(t_l1,m),'--',label="linearer Fit")
pretty_plot(ax)
fig.savefig('results/T1.pdf')
if not output_silent: plt.show()
if not output_silent: plt.close()
plt.clf()


t_lD = np.linspace(min((tD)**3),max((tD)**3),100)
fig, ax = init_plot(freesize)
ax.set_xlabel(r'$t^3$[$s^3$]')
ax.set_ylabel(r'$\ln(\frac{M_y}{M_0})+\frac{t}{T_2}$')

ax.plot((tD)**3,Mdiff,"x",label="Messwerte")
ax.plot(t_lD,fdiff(t_lD,mdiff),'--',label="linearer Fit")
ax.set_xlim(min(t_lD), max(t_lD))
pretty_plot(ax)
fig.savefig('results/TDiff.pdf')
if not output_silent: plt.show()
if not output_silent: plt.close()
plt.clf()

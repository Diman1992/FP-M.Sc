#!/usr/bin/python3
# -*- coding: utf-8 -*-

output_silent = False

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
	
tt1, Ut1 = np.loadtxt("nmrT1", unpack = True)
tt2, Ut2 = np.loadtxt("MG_2.csv", unpack = True)#,delimiter=",")
tD, UD = np.loadtxt("diffusion",unpack = True)


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

Mt1 = (Ut1[0]+Ut1)/(2*Ut1[0])
t1Log = np.log(Mt1)
selectindex = tt1.tolist().index(1.0)
p('t1Log')
m,merr,b,berr = linregress(tt1[1:-2],t1Log[1:-2])

t1 = 1/m
p('t1')
p('m')
p('merr')

p('Ut2[Ut2max]')
var, cov = optimize.curve_fit(f, tt2[Ut2max], Ut2[Ut2max])
U_0 = var[0]
U_0_err = np.sqrt(cov[0][0])
U0_t, U0_t_err, ex = latex_number("results/T2_M0.res", U_0, U_0_err, unit=r"\volt", exponent=0)
T2 = var[1]
T2_err = np.sqrt(cov[1][1])
T2_t, T2_t_err, ex = latex_number("results/T2.res", T2, T2_err, exp=0, unit=r"\second")



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



ax.set_xlabel(r't[s]')
ax.set_ylabel(r'$\ln(\frac{M_0 - M_z}{2M_0})$')

ax.plot(tt1,t1Log,"x")
#pretty_plot(ax)
#fig.savefig('')
#if not output_silent: plt.show()
#if not output_silent: plt.close()
plt.clf()

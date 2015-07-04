#!/usr/bin/python3
# -*- coding: utf-8 -*-

output_silent = False

import numpy as np
from scipy import optimize, interpolate, misc, stats, constants
import os
import sys
import re
import matplotlib
import matplotlib.pyplot as plt
import scipy.optimize as optimization
import math
import matplotlib.cm as cm
import matplotlib.ticker as mtick

for arg in sys.argv:
    if(arg=='silent'):
        output_silent = True

#########################################
# Preparation				#
#########################################

fig = plt.figure()
ax = fig.add_subplot(111)

# Plotte Hochtemperatur
path = './T1_valuesHoch'
table = np.loadtxt(path, usecols=(0,1,2), unpack=False, comments='#')
table=table[np.lexsort((table[:,1],table[:,2],table[:,0]))]
temperature, T1, error = (table[:,0],table[:,1],table[:,2])
plt.plot(1/temperature, T1, marker="o", ls="", color="black", label="T1 Werte")

# Plotte Tieftemperatur
path = './T1_valuesTief'
temperature, T1, error = np.loadtxt(path, usecols=(0,1,2), unpack=True, comments='#')

plt.plot(1/temperature, T1, marker="o", ls="", color="black")

ax.set_yscale('log')

ax.xaxis.set_major_locator(mtick.MaxNLocator(4))
ax.xaxis.set_minor_locator(mtick.MaxNLocator(8))
ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
plt.grid()
plt.xlabel(r"Temperatur$^{-1} \left[\frac{1}{K}\right]$")
plt.ylabel("Zeit [s]")
#plt.xlim((96,110))
#plt.ylim((21,29))
plt.legend()
plt.title(r"Arrhenius Gesamttemperaturbereich $T_1$")
plt.tight_layout()
plt.savefig('T1_tiefTemperaturPlot.pdf')
plt.show()

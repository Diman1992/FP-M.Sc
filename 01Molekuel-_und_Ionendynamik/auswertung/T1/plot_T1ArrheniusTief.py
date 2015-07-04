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

path = './T1_valuesTief'
temperature, T1, error = np.loadtxt(path, usecols=(0,1,2), unpack=True, comments='#')

plt.plot(1/temperature, T1, marker="o", ls="", color="black", label="T1 Werte")

ax.set_yscale('log')
ax.set_yticks([20,22,24,26,28,30])
ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
plt.grid()
plt.xlabel(r"Temperatur$^{-1} \left[\frac{1}{K}\right]$")
plt.ylabel("Zeit [s]")
#plt.xlim((96,110))
plt.ylim((21,29))
plt.legend()
plt.title(r"Arrhenius Tieftemperatur $T_1$")
plt.tight_layout()
plt.savefig('T1_tiefTemperaturPlot.pdf')

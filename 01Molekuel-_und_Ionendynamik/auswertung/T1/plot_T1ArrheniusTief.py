#!/usr/bin/python3
# -*- coding: utf-8 -*-

output_silent = False

import numpy as np
from scipy import optimize, interpolate, misc, stats, constants
import os
import sys
import re
import matplotlib.pyplot as plt
import scipy.optimize as optimization
import math
import matplotlib.cm as cm

for arg in sys.argv:
    if(arg=='silent'):
        output_silent = True

#########################################
# Preparation				#
#########################################

path = './T1_valuesTief'
temperature, T1, error = np.loadtxt(path, usecols=(0,1,2), unpack=True, comments='#')

plt.errorbar(1/temperature, T1, yerr=error, fmt="none", marker="o")
plt.plot(1/temperature, T1, marker="o", ls="", label="T1 Werte")

plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.grid()
plt.yscale("log")
plt.xlabel(r"Temperatur$^{-1} \left[\frac{1}{K}\right]$")
plt.ylabel("Zeit [s]")
#plt.xlim((96,110))
#plt.ylim((0.03,0.1))
plt.legend()
plt.title(r"Arrhenius Tieftemperatur $T_1$")
plt.savefig('T1_tiefTemperaturPlot.pdf')

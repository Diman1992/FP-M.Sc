#!/usr/bin/python3

import sys
sys.path.append("../")
from plotting import plot_range_text

print(plot_range_text((1000, 2000))==('kilo',1000))
print(plot_range_text((1, 2))==('',1))
print(plot_range_text((1,2),inital_range=1e4)==('kilo',10**1))
print(plot_range_text((1,2),inital_range='mega')==('mega',1))
print(plot_range_text((1e6, 2*1e6))==('mega',10**6))
print(plot_range_text((1e-9, 2*1e-9))==('nano', 10**-9))
print(plot_range_text((1000,1000))==('kilo',10**3))
print(plot_range_text((1e-10, 1e-10))==('pico', 10**-12))
import numpy as np
import os, sys
sys.path.append("../")
from latex_number import *
from round_to_significance import *

x = 8.8413510483026e-6
x_err = 1.6721842079167582e-7

print(latex_number('latex_number_results/norm', 123, 14.6, noprint=True)==('120','15',0))

print(latex_number('latex_number_results/norm', 123456789, 123, noprint=True)==('123456800','120',0))

print(latex_number('latex_number_results/norm', 123456789, 123, exponent=3, noprint=True)==('123456.80','0.12',3))

print(latex_number('latex_number_results/norm', x, x_err, noprint=True)==('880','17',-8))

print(latex_number('latex_number_results/norm', 123, 14, exponent=11, noprint=True)==('0.00000000120','0.00000000014', 11))

print(latex_number('latex_number_results/norm', 123, 14, exponent=-4, noprint=True)==('1200000','140000', -4))

print(latex_number('latex_number_results/norm', 1000, 0, noprint=True)==('1000','0',0))

print(latex_number('latex_number_results/norm', 0, 12, noprint=True)==('0','12',0))

print(latex_number('latex_number_results/norm', 0, 0, noprint=True)==('0','0',0))

print(latex_number('latex_number_results/norm', 0, None, noprint=True)==('0',None,0))
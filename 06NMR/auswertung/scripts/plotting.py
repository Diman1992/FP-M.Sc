global debug
debug = False
debug = True

import numpy as np
import matplotlib
from matplotlib import rcParams
rcParams['text.latex.preamble']=[
##"\\usepackage[ngerman,german]{babel}",
#"\\usepackage[T1]{fontenc}",
"\\usepackage{lmodern}",
#"\\usepackage[utf8]{inputenc}",
"\\usepackage{amsfonts}",
"\\usepackage{amssymb}",
"\\usepackage{amsmath}",
"\\usepackage{amscd}",
"\\usepackage{amstext}",
"\\usepackage{siunitx}",
"\\sisetup{detect-all,fraction=nice,free-standing-units=true,space-before-unit=true,use-xspace=true,group-separator={{\text{~}}},per-mode=fraction}"
] 
rcParams['text.latex.unicode']=True
rcParams['text.usetex']=True
rcParams['font.family']='serif'
##rcParams['font.serif']='computer modern math'
##rcParams['font.weight']='normal'
rcParams['font.style']='normal'
rcParams['font.size']=11
rcParams['axes.labelsize']=11
rcParams['legend.fontsize']=10
rcParams['xtick.labelsize']=8
rcParams['ytick.labelsize']=8
##rcParams['pgf.texsystem'] = 'pdflatex'
##matplotlib.use('ps')
import matplotlib.pyplot as plt

# set the plotting ranges and add grid+legend
def pretty_plot(ax, perct=0.01):
	# x-spacing
	x0, x1 = ax.get_xlim()
	#print(ax.get_xscale())
	x_space = (0,0)
	if(ax.get_xscale()=='log'):
		#print('logscele')	
		# on logscale we need to different spacing
		# he left end at 9
		left_pos = 9/10*x0
		# right end at 10.1
		right_pos = 1.1*x1
		x_space = (left_pos, right_pos)
	else:
		space = (1.0*x1-1.0*x0)*perct
		if(space == 0): space = x1* perct
		x_space = (1.0*x0-space,1.0*x1+space)
	ax.set_xlim(x_space[0], x_space[1])
	# y-spacing
	#y0, y1 = ax.get_ylim()
	#space = (y1-y0)*0.05
	#ax.set_ylim(y0, y1)
	# other stuff
	ax.legend(loc='best')
	ax.grid()

# set the figuresize	
def init_plot(freesize = 412.56496, **kwargs): #freesize in pt ; obtain via \showthe\columnwidth in latex
	no_axes = False
	polar = False
	for arg in kwargs:
		if (arg == "no_axes"): no_axes = kwargs[arg]
		if (arg == 'polar'): polar = kwargs[arg]
		else: print("init_plot: unknown kwarg: "+ arg)
	inches_x= freesize/72.27 # 72.27 pt/inch
	inches_y = inches_x / 1.61803399
	fig = plt.figure(1)
	fig.set_figwidth(inches_x)
	fig.set_figheight(inches_y)
	fig.set_tight_layout(True)
	fig.set_size_inches([inches_x, inches_y])
	if no_axes:
		return fig
	else:
		ax = fig.add_subplot(1,1,1, polar=polar)
		return (fig, ax)
		
# returns a string with the best latex-unit found to show the range and the scaling-value that the values need to be divided by
# possible args = inital_range: what is the default unit
# e.g.: 1e3 or as text 'micro'
# returns: 
def plot_range_text(range_tuple, **kwargs):
	x0, x1 = range_tuple
	inital_range = 0
	for arg in kwargs:
		if (arg == "inital_range"): inital_range = kwargs[arg]
		else: print("plot_range_text: unknown kwarg: "+ arg)
	if(inital_range) != 1:
		if(type(inital_range)==str):
			# inital_range is a string and we need to convert it to a number
			unit_str_to_int = {
				'pico':1e-12,
				'nano':1e-9,
				'micro':1e-6,
				'milli':1e-3,
				'':1e0,
				'kilo':1e3,
				'mega':1e6,
				'giga':1e9,
				'tera':1e12
			}
			inital_range = unit_str_to_int[inital_range]
	if(inital_range < 0): # this should not happen
		print('plot_range_text: inital_range was < 0')
		return
	#inital_range = int(inital_range) # if we enter the inital range as a float make it an int
	range = x1 - x0
	# we need to make sure not to call log(0), and we are only interested in the order of magnitude (oom)
	if(range==0): range=1
	# also: if the range is negative we need to make it positive
	range = np.sing(range)*range
	oom = np.log10(range) # oom in the value-range
	# if x0 and x1 are in the same range we need to use only one as the computational basis
	if(oom == 0): oom = np.log10(np.sign(x0)*x0)
	if(inital_range ==0): inital_range = 1 # same reason as above
	inital_oom = np.log10(inital_range)
	if debug: print('plot_range_text: oom =',oom, 'inital_oom=',inital_oom)
	# from here on we use abs values for the bases -> we need to store the sign
	
	#if(oom>4): print('plot_range_text: the range goes overo',oom,' orders of magnitude. maybe logscale?')
	# make those floats into ints
	oom = int(oom)
	inital_oom = int(inital_oom)
	# now we have the range lets determine the appropiate unit
	if debug: print('plot_range_text: type(oom)=',type(om))
	if debug: print('plot_range_text: type(inital_range)=',type(inital_range))
	good_unit = base + inital_base
	if debug: print('plot_range_text: good_unit =',good_unit)
	if debug: print('plot_range_text: type(good_unit)=',type(good_unit))
	# si units always in steps of 1e3 -> take modulus to get to next-lower unit
	#	ex: 	val = 1e4		-> good_unit = 4 	-> exponent = 4 - 4 mod 3 = 3
	#		-> val disp as 10 k
	#	ex2: val = 1e-10	-> good_unit = -10 	-> exponent = -10 - 10 mod 3 = -9
	#		-> val_disp as 0.1 nano
	good_unit = good_unit - good_unit % 3
	if debug: print('plot_range_text: good_unit_base after mod =',good_unit)
	unit_int_to_str = {
		-12:'pico',
		-9:'nano',
		-6:'micro',
		-3:'milli',
		0:'',
		3:'kilo',
		6:'mega',
		9:'giga',
		12:'tera'
	}
	good_unit_name = unit_int_to_str[good_unit]
	exponent = inital_base - good_unit
	# return the name of the unit and the amount the values have to be scaled by
	if debug: print('plot_range_text: returning', good_unit_name,',10**', exponent)
	return (good_unit_name, 10**base)

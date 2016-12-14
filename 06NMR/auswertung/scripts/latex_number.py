import numpy as np
import io as io
from round_to_significance import round_to_significance

def latex_number(file, var, error=None, **kwargs):
	use_brackets = True
	# If there is no error then default to no brackets
	if error == None: use_brackets=False
	use_exponent = None
	replace_char=['','']
	noprint=False
	unit = None
	for arg in kwargs:
		if (arg == "brackets"): use_brackets = kwargs[arg]
		elif (arg == "exponent"): use_exponent = kwargs[arg]
		elif (arg=="replace_char"): replace_char=kwargs[arg]
		elif (arg=="noprint"): noprint=kwargs[arg]
		elif arg=='unit': unit=kwargs[arg]
		else: print("latex_number: unknown kwarg: "+ arg)
	
	if np.size(error)==1: # only +- error given
		var, error, exponent, digits = round_to_significance(var, error, use_exponent)
		var = str(var).replace(replace_char[0],replace_char[1])
		if error!=None: error = str(error).replace(replace_char[0],replace_char[1])
	else: # first in error is negative, second positive...
		var1, error[0], exponent, digits = round_to_significance(var, error[0], use_exponent)
		var2, error[1], exponent, digits2 = round_to_significance(var, error[1], exponent)
		if digits2 > digits:
			var1 = var2
		var = var1
		if error[0]==error[1]:
			error = error[0]
	
	if file!=None:
		file_h = io.open(file, 'w')	
		if (use_brackets): file_h.write("\\left( ")
		file_h.write(str(var))
		if np.size(error)==1:
			if (error != None): file_h.write(" \\pm  ")
			if (error != None): file_h.write(str(error))
		else:
			if (error != None): file_h.write("\\:")
			if (error != None): file_h.write("^{+")
			if (error != None): file_h.write(str(error[1]))
			if (error != None): file_h.write("}_{-")
			if (error != None): file_h.write(str(error[0]))
			if (error != None): file_h.write("}")
		if (use_brackets): file_h.write(" \\right)")
		
		# write down the exponent
		if (exponent != 0):
			file_h.write(" \\times 10^{")
			file_h.write(str(exponent))
			file_h.write("} ")
			if unit != None:
				file_h.write('\\:') # space between unit and exponent
		
		if unit != None:
			if not use_brackets: file_h.write(' \\:') # space between number and unit
			file_h.write('\\si{')
			file_h.write(unit)
			file_h.write('}')
		
		file_h.write('\n')
		file_h.close()
		if noprint==False: print("File " + str(file) + " written. -> ("+str(var)+';\t'+str(error)+';\t'+str(exponent)+')')
	
	return (var, error, exponent)
	

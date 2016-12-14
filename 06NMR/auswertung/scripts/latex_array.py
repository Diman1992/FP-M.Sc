import io as io
import sys as sys
import numpy as np
from latex_array import *

debug = False
#~ debug = True

s_this = "latex_array: "

def latex_array_p(var):
	print(var+" = "+'\n'+str(eval(var))+'\n')

def latex_array_print_list(lists, file_h, format=None, **kwargs):
	transpose_single = False
	replace_char = ["",""]
	print_end_newline = True
	for arg in kwargs:
		if (arg == "transpose_single"):
			transpose_single = kwargs[arg]
		elif (arg == "replace_char"):
			replace_char = kwargs[arg]
		elif (arg == 'print_end_newline'):
			print_end_newline = kwargs[arg]
		else:
			print('latex_array_print_list: unknown arg', arg, '=', kwargs[arg])

	if debug: print("latex_array_print_list called with (lists, format):", lists, format)
	
	if type(lists)==np.ndarray: lists = lists.tolist()
	if type(lists) == list and type(lists[0]) == list:
		for i in range(0, len(lists)):
			if type(lists[i])==np.ndarray: lists[i] = lists[i].tolist()
			if format != None:
				if np.array(format).shape==(1,) or np.array(format).shape==():
					latex_array_print_list(lists[i], file_h, format, replace_char=replace_char)
				else:
					if debug: print("np.array(format).shape", np.array(format).shape)
					if debug: print("np.array(lists[i]).shape", np.array(lists[i]).shape)
					if(np.array(format).shape == np.array(lists[i]).shape):
						# the formastring is for this thing
						latex_array_print_list(lists[i], file_h, format, replace_char=replace_char)
					else:
						latex_array_print_list(lists[i], file_h, format[i], replace_char=replace_char)
			else:
				latex_array_print_list(lists[i], file_h, replace_char=replace_char)
				
	else:
		if debug: print("start loop with:", lists, format)
		for i in range(0, len(lists)):
			to_write = "!!!ERROR!!!"
			if debug: print(s_this+"lists[i], format:", lists[i], format)
			if format!=None:
				# format exists but might contain a 'None'
				if np.array(lists).shape == np.array(format).shape:
					if(format[i]!=None):
						to_write = format[i].format(lists[i])
					else:
						to_write = str(lists[i])
					if debug: print("to_write", to_write)
				elif np.array(format).shape == (1,):
					if (format[0]!=None):
						to_write = format[0].format(lists[i])
					else:
						to_write = str(lists[i])
					if debug: print("to_write", to_write)
				elif np.array(format).shape==():
					if (format!=None):
						try:
							to_write = format.format(lists[i])
						except:
							print(s_this+"ERROR: "+str(sys.exc_info()[1]))
							to_write = "ERROR with: '" + str(lists[i]) + ".format(" +str(format)+ ")'"
					else:
						to_write = str(lists[i])
					if debug: print("to_write", to_write)
				else:
					print(s_this+"format has bad shape")
					to_write = str( lists[i] )
			else:
				to_write = str( lists[i] )
			
			to_write = str(to_write).replace(replace_char[0], replace_char[1])
			file_h.write( to_write )
			if transpose_single and print_end_newline:
				file_h.write(" \\\\" + '\n')
			if i != (len(lists)-1) and transpose_single==False: file_h.write(" & ")
		if ( transpose_single == False and print_end_newline):
			file_h.write(" \\\\" + '\n')
		
def latex_array_transpose(table):
	# Transpose array
	transposed = []
	for i in range(0, len(table[0])):
		transposed.append([])
	for i in range(0, len(table)):
		for k in range(0, len(table[0])):
			transposed[k].append(table[i][k])
	return transposed

def latex_array_padding(table, padding_char):
	max = 0
	# determine maximum
	for i in range(0, len(table)):
		if type(table[i])==np.ndarray: table[i] = table[i].tolist()
		if (type(table[i]) == list):
			if len(table[i])>max: max = len(table[i])
		else:
			return table
			
	for i in range(0, len(table)):
		if (type(table[i]) != list):
			temp = table[i]
			table[i].append(temp)
			
		while len(table[i]) < max:
			table[i].append(padding_char)
				
	return table

def latex_array(file, table, **kwargs):
	# read kwargs
	format = None
	
	transpose = False
	transpose_single = False
	
	padding = False
	padding_char = "-"
	
	replace_char = ["",""]
	
	print_end_newline = True
	
	for arg in kwargs:
		if (arg == "format"): format = kwargs[arg] # format: exp: {:.3f}
		elif (arg == "transpose"):
			transpose = kwargs[arg]
			if transpose:
				padding = True
				print(s_this+"kwarg 'transpose=True' forces 'padding=True'.")
		elif (arg == "transpose_single"):
			if np.array(table).shape == (np.array(table).size, ):
				transpose_single = kwargs[arg]
			else:
				print(s_this+"table.shape: " + str(np.array(table).shape) + " != " + str((np.array(table).size, )) + " -> transpose_single = False")
		elif (arg == "padding"):
			if transpose:
				padding = True
			else:
				padding = kwargs[arg]
		elif (arg == "padding_char"):
			padding_char = kwargs[arg]
		elif (arg == "replace_char"):
			replace_char = kwargs[arg]
		elif (arg == 'print_end_newline'):
			print_end_newline = kwargs[arg]
		else:
			print(s_this+"!!!ERROR!!!: unknown arg: "+str(arg)+"["+str(kwargs[arg])+"] !")
	
	# make to table if still array
	if type(table)==np.ndarray: table = table.tolist()
	
	# apply padding
	if padding:
		table = latex_array_padding(table, padding_char)
	
	# transpose if wanted
	if transpose and (np.array(table).shape != (np.array(table).size, )): # table is actually multi-dimentional
		table = latex_array_transpose(table)
	
	# save the document
	file_h = io.open(file, 'w')
	latex_array_print_list(table, file_h, format, transpose_single=transpose_single, replace_char=replace_char, print_end_newline=print_end_newline)
	file_h.close()
	if debug: print('\n\n\n')
	print(s_this+"File " + str(file) + " written.")

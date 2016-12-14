import numpy as np
import io as io

def load_strings(file):
	ret = []
	file_h = io.open(file)
	line = file_h.readline()
	while line!='':
		if not line.startswith('#'):
			line = line.replace("\n", "")
			ret.append(line)
		line = file_h.readline()
			
	file_h.close()
	print("ret=" + str(ret))
	return ret

def load_comments(file):
	ret = []
	file_h = io.open(file)
	line = file_h.readline()
	while line!='':
		if line.startswith('#'):
			line = line.replace("\n", "")
			line = line.replace('#','')
			ret.append(line)
		line = file_h.readline()
			
	file_h.close()
	print("ret=" + str(ret))
	return ret
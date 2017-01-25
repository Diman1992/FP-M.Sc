import fileinput
import sys
import glob

for file in glob.glob('./data/g_*.csv'):
	i = 0
	for line in fileinput.input(file, inplace=True):
		if(i < 2):
			sys.stdout.write('#{l}'.format(l=line))
			i = i + 1
		else:
			sys.stdout.write('{l}'.format(l=line))

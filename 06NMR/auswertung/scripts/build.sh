#!/bin/sh
for i in $(find -iname "*.py") ;
do 
if [ $(dirname $i) != "." ]
then
	cd $(dirname $i)
	#mkdir results - commented out because some folders hase sub-stucture
	pwd
	python3 $(basename $i) silent
	cd .. 
fi;
done

for i in $(find -iname "*.tex") ;
do 
if [ $(dirname $i) != "." ]
then
	cd $(dirname $i)
	pwd
	pdflatex $(basename $i)
	pdflatex $(basename $i)
	pdflatex $(basename $i)
	cd .. 
fi;
done

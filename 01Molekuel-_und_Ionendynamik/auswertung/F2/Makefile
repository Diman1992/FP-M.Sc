.PHONY: all clean

all: ./F2_Plot.pdf ./F2_Fit.pdf

clean:
	rm *.pdf

./F2_Plot.pdf: ./plot_01.py
	python $<


./F2_Fit.pdf: ./plot_tauC_tief.py ./tauC_values
	python $<

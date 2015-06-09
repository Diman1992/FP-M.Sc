.PHONY: all clean

all: ./F2Plot_log.pdf ./F2_hochTemperaturPlot.pdf

clean:
	rm *.pdf

./F2Plot_log.pdf: ./plot_01.py
	python $<


./F2_hochTemperaturPlot.pdf: ./plot_tauC_tief.py ./tauC_values
	python $<

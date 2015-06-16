.PHONY: all clean

all: ./T2_hochTemperaturFit.pdf ./T2_tiefTemperaturFit.pdf ./T2_hochTemperaturPlot.pdf

clean:
	rm *.pdf

./T2_hochTemperaturFit.pdf: ./plot_01hoch.py
	python $<

./T2_tiefTemperaturFit.pdf: ./plot_01tief.py
	python $<

#./T2_hochTemperaturPlot.pdf: ./plot_tauC_Hoch.py
#	python $<

.PHONY: all clean

all: ./T2_hochTemperaturFit.pdf ./T2_tiefTemperaturFit.pdf ./T2_tiefTemperaturPlot.pdf

clean:
	rm *.pdf

./T2_hochTemperaturFit.pdf: ./plot_01hoch.py
	python3 $<

./T2_tiefTemperaturFit.pdf: ./plot_01tief.py
	python3 $<

./T2_tiefTemperaturPlot.pdf: ./plot_tauC_tief.py ./T2_data
	python3 ./plot_tauC_tief.py

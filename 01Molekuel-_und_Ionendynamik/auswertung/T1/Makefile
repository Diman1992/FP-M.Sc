.PHONY: all clean

all: ./T1_hochTemperaturFit.pdf ./T1_tiefTemperaturFit.pdf ./T1_hochTemperaturPlot.pdf ./T1_tiefTemperaturPlot.pdf

clean:
	rm *.pdf

./T1_hochTemperaturFit.pdf: ./plot_T1hoch.py
	python3 $<

./T1_tiefTemperaturFit.pdf: ./plot_T1tief.py
	python3 $<

./T1_hochTemperaturPlot.pdf: ./plot_T1ArrheniusHoch.py ./T1_valuesHoch
	python3 $<

./T1_tiefTemperaturPlot.pdf: ./plot_T1ArrheniusTief.py ./T1_valuesTief
	python3 $<

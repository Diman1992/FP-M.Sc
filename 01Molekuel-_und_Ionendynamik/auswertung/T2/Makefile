.PHONY: all clean

all: ./T2Hoch_log.pdf ./T2Tief_log.pdf ./T2_hochTemperaturPlot.pdf

clean:
	rm *.pdf

./T2Hoch_log.pdf: ./plot_01hoch.py
	python $<

./T2Tief_log.pdf: ./plot_01tief.py
	python $<

./T2_hochTemperaturPlot.pdf: ./plot_tauC_Hoch.py
	python $<

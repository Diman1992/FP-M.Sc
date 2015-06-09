SUBDIRS = T1 T2 F2
.PHONY: all clean

all:
	for d in $(SUBDIRS); do \
		(cd $$d; make all) \
	done

clean:
	for d in $(SUBDIRS); do \
		(cd $$d; make clean) \
	done

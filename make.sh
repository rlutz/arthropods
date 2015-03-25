#!/bin/sh

for variant in SIP DIP DIPwide 1xPIN 2xPIN WSL WSLalt
do	for pin_count in 6 16
	do	./arthropods.py $variant $pin_count \
		  > footprints/$variant$pin_count.fp
	done
done

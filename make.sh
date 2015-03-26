#!/bin/bash

for pin_count in 6 16
do	./arthropods -s thickened SIP${pin_count} $pin_count \
	  > footprints/SIP${pin_count}.fp
	./arthropods -U -d 300 -s dent DIP${pin_count} $pin_count \
	  > footprints/DIP${pin_count}.fp
	./arthropods -U -d 600 -s dent DIP${pin_count}_wide $pin_count \
	  > footprints/DIPwide${pin_count}.fp
	./arthropods -s thickened 1x${pin_count}PIN $pin_count \
	  > footprints/1xPIN${pin_count}.fp
	./arthropods -Z -s boxed 2x${pin_count}PIN $[$pin_count * 2] \
	  > footprints/2xPIN${pin_count}.fp
	./arthropods -A -s boxed 2x${pin_count}PIN_AB $[$pin_count * 2] \
	  > footprints/2xPIN${pin_count}_AB.fp
	./arthropods -B -s boxed 2x${pin_count}PIN_BA $[$pin_count * 2] \
	  > footprints/2xPIN${pin_count}_BA.fp
	./arthropods -Z -s wsl-arrow 2x${pin_count}PIN_WSL $[$pin_count * 2] \
	  > footprints/WSL${pin_count}.fp
	./arthropods -Z -s wsl-dent 2x${pin_count}PIN_WSL $[$pin_count * 2] \
	  > footprints/WSLalt${pin_count}.fp
	./arthropods -Z -s psl 2x${pin_count}PIN_PSL $[$pin_count * 2] \
	  > footprints/PSL${pin_count}.fp
done

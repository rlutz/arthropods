#!/bin/bash

for pin_count in 6 16
do	./arthropods --straight --style=thickened SIP${pin_count} $pin_count \
	  > footprints/SIP${pin_count}.fp
	./arthropods --u-shaped -d300 --style=dent DIP${pin_count} $pin_count \
	  > footprints/DIP${pin_count}.fp
	./arthropods --u-shaped -d600 --style=dent DIP${pin_count}_wide $pin_count \
	  > footprints/DIPwide${pin_count}.fp
	./arthropods --straight --style=thickened 1x${pin_count}PIN $pin_count \
	  > footprints/1xPIN${pin_count}.fp
	./arthropods --zigzag --style=boxed 2x${pin_count}PIN $[$pin_count * 2] \
	  > footprints/2xPIN${pin_count}.fp
	./arthropods --zigzag --style=wsl-arrow 2x${pin_count}PIN_WSL $[$pin_count * 2] \
	  > footprints/WSL${pin_count}.fp
	./arthropods --zigzag --style=wsl-dent 2x${pin_count}PIN_WSL $[$pin_count * 2] \
	  > footprints/WSLalt${pin_count}.fp
	./arthropods --zigzag --style=psl 2x${pin_count}PIN_PSL $[$pin_count * 2] \
	  > footprints/PSL${pin_count}.fp
done

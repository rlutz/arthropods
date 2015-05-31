#!/bin/bash

for pin_count in 6 16
do	./arthropods -s thickened \
	    --name=SIP${pin_count} $pin_count \
	  > footprints/SIP${pin_count}.fp
	./arthropods -r 2 -n u-shaped -d 300mil -s dent \
	    --name=DIP${pin_count} $pin_count \
	  > footprints/DIP${pin_count}.fp
	./arthropods -r 2 -n u-shaped -d 600mil -s dent \
	    --name=DIP${pin_count}_wide $pin_count \
	  > footprints/DIPwide${pin_count}.fp
	./arthropods -s thickened \
	    --name=1x${pin_count}PIN $pin_count \
	  > footprints/1xPIN${pin_count}.fp
	./arthropods -r 2 -n zigzag -s boxed \
	    --name=2x${pin_count}PIN $[$pin_count * 2] \
	  > footprints/2xPIN${pin_count}.fp
	./arthropods -r 2 -n ab -s boxed \
	    --name=2x${pin_count}PIN_AB $[$pin_count * 2] \
	  > footprints/2xPIN${pin_count}_AB.fp
	./arthropods -r 2 -n ba -s boxed \
	    --name=2x${pin_count}PIN_BA $[$pin_count * 2] \
	  > footprints/2xPIN${pin_count}_BA.fp
	./arthropods -r 2 -n ba -s socket \
	    --name=2x${pin_count}PINsocket_BA $[$pin_count * 2] \
	  > footprints/2xPIN${pin_count}socket_BA.fp
	./arthropods -r 2 -n zigzag -s wsl-arrow \
	    --name=2x${pin_count}PIN_WSL $[$pin_count * 2] \
	  > footprints/WSL${pin_count}.fp
	./arthropods -r 2 -n zigzag -s wsl-dent \
	    --name=2x${pin_count}PIN_WSL $[$pin_count * 2] \
	  > footprints/WSLalt${pin_count}.fp
	./arthropods -r 2 -n zigzag -s psl \
	    --name=2x${pin_count}PIN_PSL $[$pin_count * 2] \
	  > footprints/PSL${pin_count}.fp
done

#!/bin/bash

for pin_count in 6 16
do	./arthropods --style=thickened \
	    --name=SIP${pin_count} -P ${pin_count} \
	  > footprints/SIP${pin_count}.fp
	./arthropods --row-count=2 --numbering-scheme=u-shaped --row-distance=300mil --style=dent \
	    --name=DIP${pin_count} -P ${pin_count} \
	  > footprints/DIP${pin_count}.fp
	./arthropods --row-count=2 --numbering-scheme=u-shaped --row-distance=600mil --style=dent \
	    --name=DIP${pin_count}_wide -P ${pin_count} \
	  > footprints/DIPwide${pin_count}.fp
	./arthropods --style=thickened \
	    --name=1x${pin_count}PIN -p ${pin_count} \
	  > footprints/1xPIN${pin_count}.fp
	./arthropods --row-count=2 --numbering-scheme=zigzag --style=boxed \
	    --name=2x${pin_count}PIN -p ${pin_count} \
	  > footprints/2xPIN${pin_count}.fp
	./arthropods --row-count=2 --numbering-scheme=ab --style=boxed \
	    --name=2x${pin_count}PIN_AB -p ${pin_count} \
	  > footprints/2xPIN${pin_count}_AB.fp
	./arthropods --row-count=2 --numbering-scheme=ba --style=boxed \
	    --name=2x${pin_count}PIN_BA -p ${pin_count} \
	  > footprints/2xPIN${pin_count}_BA.fp
	./arthropods --row-count=2 --numbering-scheme=ba --style=socket \
	    --name=2x${pin_count}PINsocket_BA -p ${pin_count} \
	  > footprints/2xPIN${pin_count}socket_BA.fp
	./arthropods --row-count=2 --numbering-scheme=zigzag --style=wsl-arrow \
	    --name=2x${pin_count}PIN_WSL -p ${pin_count} \
	  > footprints/WSL${pin_count}.fp
	./arthropods --row-count=2 --numbering-scheme=zigzag --style=wsl-dent \
	    --name=2x${pin_count}PIN_WSL -p ${pin_count} \
	  > footprints/WSLalt${pin_count}.fp
	./arthropods --row-count=2 --numbering-scheme=zigzag --style=psl \
	    --name=2x${pin_count}PIN_PSL -p ${pin_count} \
	  > footprints/PSL${pin_count}.fp
done

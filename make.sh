#!/bin/bash

for pin_count in 6 16
do	./arthropods \
	    --name=SIP${pin_count} -P ${pin_count} \
	    -v SIP config \
	  > footprints/SIP${pin_count}.fp
	./arthropods \
	    --name=DIP${pin_count} -P ${pin_count} \
	    -v DIP config \
	  > footprints/DIP${pin_count}.fp
	./arthropods \
	    --name=DIP${pin_count}_wide -P ${pin_count} \
	    -v DIPwide config \
	  > footprints/DIPwide${pin_count}.fp
	./arthropods \
	    --name=1x${pin_count}PIN -p ${pin_count} \
	    -v 1xXPIN config \
	  > footprints/1xPIN${pin_count}.fp
	./arthropods \
	    --name=2x${pin_count}PIN -p ${pin_count} \
	    -v 2xXPIN config \
	  > footprints/2xPIN${pin_count}.fp
	./arthropods \
	    --name=2x${pin_count}PIN_AB -p ${pin_count} \
	    -v 2xXPIN_AB config \
	  > footprints/2xPIN${pin_count}_AB.fp
	./arthropods \
	    --name=2x${pin_count}PIN_BA -p ${pin_count} \
	    -v 2xXPIN_BA config \
	  > footprints/2xPIN${pin_count}_BA.fp
	./arthropods \
	    --name=2x${pin_count}PINsocket_BA -p ${pin_count} \
	    -v 2xXPINsocket_BA config \
	  > footprints/2xPIN${pin_count}socket_BA.fp
	./arthropods \
	    --name=2x${pin_count}PIN_WSL -p ${pin_count} \
	    -v 2xXPIN_WSL config \
	  > footprints/WSL${pin_count}.fp
	./arthropods \
	    --name=2x${pin_count}PIN_WSL -p ${pin_count} \
	    -v 2xXPIN_WSLalt config \
	  > footprints/WSLalt${pin_count}.fp
	./arthropods \
	    --name=2x${pin_count}PIN_PSL -p ${pin_count} \
	    -v 2xXPIN_PSL config \
	  > footprints/PSL${pin_count}.fp
done

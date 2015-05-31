#!/bin/bash

for pin_count in 6 16
do	./arthropods -v SIP -P ${pin_count} config \
	  > footprints/SIP${pin_count}.fp
	./arthropods -v DIP -P ${pin_count} config \
	  > footprints/DIP${pin_count}.fp
	./arthropods -v DIPwide -P ${pin_count} config \
	  > footprints/DIPwide${pin_count}.fp
	./arthropods -v 1xXPIN -p ${pin_count} config \
	  > footprints/1xPIN${pin_count}.fp
	./arthropods -v 2xXPIN -p ${pin_count} config \
	  > footprints/2xPIN${pin_count}.fp
	./arthropods -v 2xXPIN_AB -p ${pin_count} config \
	  > footprints/2xPIN${pin_count}_AB.fp
	./arthropods -v 2xXPIN_BA -p ${pin_count} config \
	  > footprints/2xPIN${pin_count}_BA.fp
	./arthropods -v 2xXPINsocket_BA -p ${pin_count} config \
	  > footprints/2xPIN${pin_count}socket_BA.fp
	./arthropods -v 2xXPIN_WSL -p ${pin_count} config \
	  > footprints/WSL${pin_count}.fp
	./arthropods -v 2xXPIN_WSLalt -p ${pin_count} config \
	  > footprints/WSLalt${pin_count}.fp
	./arthropods -v 2xXPIN_PSL -p ${pin_count} config \
	  > footprints/PSL${pin_count}.fp
done

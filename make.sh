#!/bin/bash

for pin_count in 6 16
do	./arthropods -v SIP -P ${pin_count} sip-dip
	./arthropods -v DIP -P ${pin_count} sip-dip
	./arthropods -v DIP_wide -P ${pin_count} sip-dip
	./arthropods -v 1xXPIN -p ${pin_count} connectors
	./arthropods -v 1xXPINsocket -p ${pin_count} connectors
	./arthropods -v 2xXPIN -p ${pin_count} connectors
	./arthropods -v 2xXPIN_AB -p ${pin_count} connectors
	./arthropods -v 2xXPIN_BA -p ${pin_count} connectors
	./arthropods -v 2xXPINsocket_BA -p ${pin_count} connectors
	./arthropods -v 2xXPIN_WSL -p ${pin_count} connectors
	./arthropods -v 2xXPIN_WSLalt -p ${pin_count} connectors
	./arthropods -v 2xXPIN_PSL -p ${pin_count} connectors
done

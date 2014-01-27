#include "serial_decoder.h"
#include "compat.h"

#include <stdlib.h>
#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>

int serial;

int main () {
	//Ouverture serial
	printf("Ouverture serial\n");
	serial = open ("/dev/ttyUSB0", O_RDWR | O_NOCTTY | O_SYNC);
	if (serial < 0) {
		perror("Can't open serial\n");
		return (EXIT_FAILURE);
	}
	set_interface_attribs (serial, B57600, PARENB|PARODD);  // set speed to 115,200 bps, 8n1 (no parity)
	set_blocking (serial, 1);                // set no locking

	printf("Initialisation protocole\n");

	//Initialisation protocole
	init_protocol();

	printf("Protocole pret\n");

	while (1) {
		char data = serial_read();
		executeCmd(data);
	}
	return 0;
}

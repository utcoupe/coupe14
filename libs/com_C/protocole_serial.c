#include "protocole_serial.h"
#include "compat.h"
#include "serial_decoder.h"

#include <pthread.h>
#include <fcntl.h>
#include <errno.h>
#include <termios.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>

static pthread_t poll_ordre;
pthread_mutex_t mutex;
extern int serial;

void* poll_proto () {
	while (1) {
		char data = generic_serial_read(); //blocant
		executeCmd(data);
	}
}

void init_protocol_thread () {
	printf("[MAIN]  Essai d'ouverture de %s\n", SERIAL_PATH);
	serial = open (SERIAL_PATH, O_RDWR | O_NOCTTY | O_SYNC);
	if (serial < 0) {
		perror("Can't open serial :");
		exit (EXIT_FAILURE);
	}
	set_interface_attribs (serial, B57600, PARENB|PARODD);  
	set_blocking (serial, 1);                // set blocking
	printf("[MAIN]  Initialisation protocole\n");
	protocol_blocking_reset();
	printf("[MAIN]  Protocole pret\n");
	pthread_mutex_init (&mutex, NULL);
	printf("[MAIN]  Starting com thread\n");
	pthread_create (&poll_ordre, NULL, poll_proto, NULL);
}

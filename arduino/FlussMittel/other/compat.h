/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#ifndef COMPAARDUINO_H
#define COMPAARDUINO_H

#include "parameters.h"
#include "serial_defines.h"

#define LOCAL_ADDR ADDR_FLUSSMITTEL_OTHER //Ici l'adresse locale du client
#define FORWARD_ADDR ADDR_FLUSSMITTEL_ASSERV

unsigned long timeMillis();
unsigned long timeMicros();

void serial_send(char data);
char generic_serial_read();
void forward_serial_send(char c, char addr);

#endif

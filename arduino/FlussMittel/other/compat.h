/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#ifndef COMPAARDUINO_H
#define COMPAARDUINO_H

#include "Arduino.h"
#include "parameters.h"
#include "serial_defines.h"

#define LOCAL_ADDR ADDR_FLUSSMITTEL_OTHER //Ici l'adresse locale du client
#define FORWARD_ADDR_ASSERV ADDR_FLUSSMITTEL_ASSERV
#define FORWARD_ADDR_CAM ADDR_FLUSSMITTEL_CAM

void initPins();
unsigned long timeMillis();
unsigned long timeMicros();

void serial_write(char data);
char serial_read();
void forward_serial_write(char c, char addr);

#endif

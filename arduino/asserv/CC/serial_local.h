/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 11/12/13			*
 ****************************************/
#ifndef SERIAL_LOCAL_H
#define SERIAL_LOCAL_H

#include "serial_defines.h"
#include "compaArduino.h"

#define LOCAL_ADDR ADDR_FLUSSMITTEL_ASSERV //Ici l'adresse locale du client

void sendByte(char data) { //Envoi d'un octet en serial, dépend de la plateforme
	Serial2.write(data);
}

#endif

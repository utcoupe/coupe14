/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#include "compat.h"
#include "Servo.h"

unsigned long timeMillis(){
	return millis();
}
unsigned long timeMicros(){
	return micros();
}

void serial_send(char data) { //Envoi d'un octet en serial, dépend de la plateforme
	SERIAL_MAIN.write(data);
}

char generic_serial_read(){
	return SERIAL_MAIN.read();
}

void forward_serial_send(char c, char addr) {
	if (addr == FORWARD_ADDR) {
		SERIAL_FWD.write(c);
	}
}

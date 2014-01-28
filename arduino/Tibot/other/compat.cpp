/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#include "compat.h"
#include "Servo.h"

extern Servo servoBras;

void initPins(){
	pinMode(PIN_SERVO_BRAS, OUTPUT);
	servoBras.attach(PIN_SERVO_BRAS);
}

unsigned long timeMillis(){
	return millis();
}
unsigned long timeMicros(){
	return micros();
}

void serial_send(char data) { //Envoi d'un octet en serial, dépend de la plateforme
	Serial2.write(data);
}

char generic_serial_read(){
	return Serial2.read();
}

void forward_serial_send(char c, char addr) {
	if (addr == FORWARD_ADDR_ASSERV) {
		Serial1.write(c);
	}
}

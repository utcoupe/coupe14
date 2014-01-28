/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#include "compat.h"
#include "Servo.h"

#include <Arduino.h>

extern Servo servoBras;

void initPins(){
	pinMode(PIN_SERVO_BRAS, OUTPUT);
	servoBras.attach(PIN_SERVO_BRAS);

	pinMode(PIN_INT_HAUT_ASC, INPUT_PULLUP);
	pinMode(PIN_INT_BAS_ASC, INPUT_PULLUP);
}

unsigned long timeMillis(){
	return millis();
}
unsigned long timeMicros(){
	return micros();
}

void serial_send(char data) { //Envoi d'un octet en serial, dépend de la plateforme
	Serial.write(data);
}

char serial_read(){
	return Serial.read();
}

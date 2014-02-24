/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
  
#include "Arduino.h"
#include "compat.h"
#include "parameters.h"
#include "control.h"
#include "serial_decoder.h"
#include "serial_defines.h"

unsigned long index = 0;
unsigned long timeStart = 0;
unsigned long timeLED = 0;

//Creation du controleur
Control control;

#define MAX_READ 64 
void setup(){
	TCCR3B = (TCCR3B & 0xF8) | 0x01 ;
	initPins();
	Serial2.begin(115200);
#ifdef DEBUG
	Serial.begin(115200);
#endif
	init_protocol();
	PDEBUGLN("INIT DONE");
	// LED qui n'en est pas une
	pinMode(22,OUTPUT);
	digitalWrite(22, LOW);
}

void loop(){
	/* on note le temps de debut */
	timeStart = micros();
	if (timeStart - timeLED > 1000000) {
		digitalWrite(22, LOW);
	}
		
	//Action asserv
	control.compute();

	/* zone programmation libre */
	int available = Serial2.available();
	if (available > MAX_READ) {
		available = MAX_READ;
	}
	for(int i = 0; i < available; i++) {
		// recuperer l'octet courant
		executeCmd(generic_serial_read());
	}

	/* On attend le temps qu'il faut pour boucler */
	long udelay = DUREE_CYCLE*1000-(micros()-timeStart);
	//Serial.println(udelay);
	if(udelay<0) {
		timeLED = timeStart;
		digitalWrite(22, HIGH);
		PDEBUGLN("ouch : mainloop trop longue");
	}
	else
		delayMicroseconds(udelay);
}

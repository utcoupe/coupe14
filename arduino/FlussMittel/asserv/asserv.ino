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
	TCCR1B = (TCCR1B & 0xF8) | 0x01 ;
	initPins();
	Serial2.begin(115200, SERIAL_8O1);
#ifdef DEBUG
	Serial.begin(115200);
#endif
	init_protocol();
	PDEBUGLN("INIT DONE");

	pinMode(LED_MAINLOOP, OUTPUT);
	pinMode(LED_BLOCKED, OUTPUT) ;
	digitalWrite(LED_MAINLOOP, HIGH); //HIGH = eteinte
	digitalWrite(LED_BLOCKED, HIGH); //HIGH = eteinte
}

void loop(){
	/* on note le temps de debut */
	timeStart = micros();
	if (timeStart - timeLED > 60*1000000) {
		digitalWrite(LED_MAINLOOP, HIGH);
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
	if(udelay<0) {
		timeLED = timeStart;
		digitalWrite(LED_MAINLOOP, LOW);
		PDEBUGLN("ouch : mainloop trop longue");
	}
	else
		delayMicroseconds(udelay);
}

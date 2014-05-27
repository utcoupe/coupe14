/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
  
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
	TCCR3B = (TCCR3B & 0xF8) | 0x01 ; //PWM FREQUENCY
	initPins();
	initSize();
	SERIAL_MAIN.begin(57600, SERIAL_8O1);
#ifdef DEBUG
	Serial.begin(115200, SERIAL_8N1);
#endif
	PDEBUGLN("BOOT");
	protocol_blocking_reset();
	PDEBUGLN("INIT DONE");
}

void loop(){
	/* on note le temps de debut */
	timeStart = micros();
	if (timeStart - timeLED > 60*1000000) {
		digitalWrite(LED_MAINLOOP, HIGH);
	}

	/* zone programmation libre */
	int available = SERIAL_MAIN.available();
	if (available > MAX_READ) {
		available = MAX_READ;
	}
	for(int i = 0; i < available; i++) {
		// recuperer l'octet courant
		char data = generic_serial_read();
		executeCmd(data);
	}
	//Action asserv
	control.compute();

	/* fin zone de programmation libre */
	
	
	/* On attend le temps qu'il faut pour boucler */
	long udelay = DUREE_CYCLE*1000-(micros()-timeStart);
	if(udelay<0) {
		PDEBUGLN("ouch : mainloop trop longue");
		timeLED = timeStart;
		digitalWrite(LED_MAINLOOP, LOW);
	}
	else
		delayMicroseconds(udelay);
}

/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
  
#include "compaArduino.h"
#include "parameters.h"
#include "control.h"

#include "protocol.h"

unsigned long index = 0;
unsigned long timeStart = 0;

//Creation du controleur
Control control;

#define MAX_READ 64 
void setup(){
	initPins();
	Serial.begin(57600, SERIAL_8N1);
	PDEBUGLN("INIT DONE");
	// LED qui n'en est pas une
	pinMode(16,OUTPUT);
}

void loop(){
	/* on note le temps de debut */
	timeStart = micros();

	/* La del est allumee pendant le traitement */
	digitalWrite(16, HIGH);

	//Action asserv
	control.compute();

	/* zone programmation libre */
	int available = Serial.available();
	if (available > MAX_READ) {
		available = MAX_READ;
	}
	for(int i = 0; i < available; i++) {
		// recuperer l'octet courant
		char data = Serial.read();
		executeCmd(data);
		WRDEBUG(data);
	}

	/* fin zone de programmation libre */
	
	/* On eteint la del */
	digitalWrite(16, LOW);
	
	/* On attend le temps qu'il faut pour boucler */
	long udelay = DUREE_CYCLE*1000-(micros()-timeStart);
	if(udelay<0)
		PDEBUGLN("ouch : mainloop trop longue");
	else
		delayMicroseconds(udelay);
}

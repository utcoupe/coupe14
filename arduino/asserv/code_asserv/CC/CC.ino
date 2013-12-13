/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
  
#include "compaArduino.h"
#include "parameters.h"
#include <math.h>
#include "protocole.h"
#include "command.h"
#include "message.h"
#include "control.h"

unsigned long index = 0;
unsigned long timeStart = 0;

//Creation du controleur
Control control;

#define MAX_READ 4 
void setup(){
	initPins();
	initSerialLink();
	Serial.write("INIT DONE\n");
	// LED qui n'en est pas une
	pinMode(16,OUTPUT);
}

void loop(){
	int right_error, left_error;
	/* on note le temps de debut */
	timeStart = micros();

	/* La del est allumee pendant le traitement */
	digitalWrite(16, HIGH);

	/* zone programmation libre */
	int available = Serial.available();
	if (available > MAX_READ) {
		available = MAX_READ;
	}
	for(int i = 0; i < available; i++) {
		// recuperer l'octet courant
		char data = Serial.read();
		cmd(data);
		Serial.write(data);
	}
	//Action asserv
	control.compute();

	//---- DEBUG TICKS ----
	right_error = control.getRenc()->getError();
	left_error = control.getLenc()->getError();
	if(left_error != 0)
		Serial.println("-- left ticks error : " + left_error);
	if(right_error != 0)
		Serial.println("-- right ticks error : " + right_error);
	//---- FIN DEBUG TICKS ----

	/* fin zone de programmation libre */
	
	/* On eteint la del */
	digitalWrite(16, LOW);
	
	/* On attend le temps qu'il faut pour boucler */
	long udelay = DUREE_CYCLE*1000-(micros()-timeStart);
	if(udelay<0)
		Serial.println("ouch : mainloop trop longue");
	else
		 delayMicroseconds(udelay);
}



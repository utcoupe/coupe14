/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
  
#include "Arduino.h"
#include "Servo.h"

#include "serial_decoder_forward.h"
#include "serial_defines.h"
#include "compat.h"
#include "parameters.h"

Servo servoBras;

#define MAX_READ 64 
void setup(){
	initPins();
	Serial2.begin(57600, SERIAL_8O1);
	Serial1.begin(57600, SERIAL_8O1); //Forward
#ifdef DEBUG
	Serial.begin(115200, SERIAL_8N1);
#endif
	init_protocol();
	PDEBUGLN("INIT DONE");
	// LED qui n'en est pas une
	pinMode(16,OUTPUT);
}

void loop(){

	/* La del est allumee pendant le traitement */
	digitalWrite(16, HIGH);


	/* zone programmation libre */
	int available = Serial2.available();
	if (available > MAX_READ) {
		available = MAX_READ;
	}
	for(int i = 0; i < available; i++) {
		// recuperer l'octet courant
		executeCmd(generic_serial_read());
	}

	//Forward des retours asserv
	available = Serial1.available();
	if (available > MAX_READ) {
		available = MAX_READ;
	}
	for(int i = 0; i < available; i++) {
		serial_send(Serial1.read());
	}

	/* fin zone de programmation libre */
	
	/* On eteint la del */
	digitalWrite(16, LOW);
	
}

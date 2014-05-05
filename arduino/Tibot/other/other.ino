/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
  
#include "Arduino.h"
#include "Servo.h"

#include "serial_decoder.h"
#include "serial_defines.h"
#include "serial_switch.h"
#include "compat.h"
#include "parameters.h"

#define MAX_READ 64 
void setup(){
	initPins();

	Serial2.begin(57600, SERIAL_8O1);
	Serial1.begin(57600, SERIAL_8O1); //Forward
#ifdef DEBUG
	Serial.begin(115200, SERIAL_8N1);
#endif

	initServos();
	init_protocol();
	PDEBUGLN("INIT DONE");
}

void loop(){
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
}

/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
  
#include "Arduino.h"
#include "serial_decoder.h"
#include "serial_defines.h"
#include "servo.h"


Servo servoBras;

#define MAX_READ 64 
void setup(){
	initPins();
	Serial2.begin(57600, SERIAL_8O1);
	Serial.begin(115200, SERIAL_8N1);
	init_protocol();
	PDEBUGLN("INIT DONE");
	// LED qui n'en est pas une
	pinMode(16,OUTPUT);

	servoBras.attach(PIN_SERVO_BRAS);
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
		executeCmd(serial_read());
	}

	/* fin zone de programmation libre */
	
	/* On eteint la del */
	digitalWrite(16, LOW);
	
}

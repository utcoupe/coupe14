
/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/

//#include "AFMotor.h"
#include <Servo.h>
#include <Arduino.h>

#include "serial_decoder.h"
#include "serial_defines.h"
#include "compat.h"
#include "parameters.h"

Servo servoBras;
//AF_DCMotor motor_ascenseur(1);

#define MAX_READ 64 
void setup(){
	initPins();
	Serial.begin(57600);

	init_protocol();
	//Moteurs :
	//motor_ascenseur.run(RELEASE);
	servoBras.write(0);
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
		executeCmd(serial_read());
	}
	/* fin zone de programmation libre */
	
	/* On eteint la del */
	digitalWrite(16, LOW);
	
}

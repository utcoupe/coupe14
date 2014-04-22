
/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/

#include <Servo.h>
#include <Arduino.h>

#include "AFMotor.h"
#include "AccelStepper.h"
#include "serial_decoder.h"
#include "serial_defines.h"
#include "compat.h"
#include "parameters.h"
#include "actions.h"

Servo servoRet, servoBrasAngle, servoBrasDist;
AF_Stepper stepper_motor(200, 2);
AF_DCMotor pump_motor(2, MOTOR12_64KHZ);
extern AccelStepper stepperAsc;

#define MAX_READ 64 
void setup(){
	initPins();

	Serial.begin(115200);
	Serial1.begin(115200); //Forward
#ifdef DEBUG
	Serial3.begin(115200);
#endif

	initAct();
	init_protocol();
}

void loop(){
	/*
	static long start = timeMillis();
	static bool init = true, init2 = true;
	if (init) {
		getTri(220, -40, 20);
		deposeTri(50);
		init = false;
	}
	if ((timeMillis() - start) > 10000 & init2) {
		init2 = false;
		getTri(250, 55, 20);
		deposeTri(80);
	}*/

	int available = Serial.available();
	if (available > MAX_READ) {
		available = MAX_READ;
	}
	for(int i = 0; i < available; i++) {
		// recuperer l'octet courant
		executeCmd(generic_serial_read());
	}

	available = Serial1.available();
	if (available > MAX_READ) {
		available = MAX_READ;
	}
	for(int i = 0; i < available; i++) {
		serial_send(Serial1.read());
	}
	cmdBras();
}

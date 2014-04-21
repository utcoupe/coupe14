
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

	init_act();
	//init_protocol();
}

void loop(){
	/*
	servoBrasDist.write(0);
	delay(10000);
	servoBrasDist.write(20);
	delay(10000);
	servoBrasDist.write(40);
	delay(10000);
	servoBrasDist.write(60);
	delay(10000);
	servoBrasDist.write(80);
	delay(10000);
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
	*/
	cmdBras(-1,-1,-1,0);
	//stepperAsc.run();
}

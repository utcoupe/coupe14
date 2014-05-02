
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

extern Servo servoRet, servoBrasAngle, servoBrasDist;
extern AF_DCMotor pump_motor;
extern AF_Stepper stepper_motor;
extern AccelStepper stepperAsc;
extern bool use_act;

#define MAX_READ 64 
void setup(){
	initPins();

	SERIAL_MAIN.begin(115200, SERIAL_8O1);
	SERIAL_FWD.begin(115200, SERIAL_8O1); //Forward
#ifdef DEBUG
	Serial3.begin(115200);
#endif

	initAct();
	digitalWrite(PIN_DEBUG_LED, LOW);
	init_protocol();
	digitalWrite(PIN_DEBUG_LED, HIGH);
}

void loop(){
/*
	static long start = timeMillis();
	static bool init = true, init2 = true, init3 = true;
	if (init) {
		getTri(250, 55, 60);
		deposeTri(15);
		init = false;
	}
	if ((timeMillis() - start) > 6000 & init2) {
		init2 = false;
		getTri(250, -40, 30);
		deposeTri(-45);
	}
	if ((timeMillis() - start) > 18000 & init3) {
		init3 = false;
		getTri(250, 55, 30);
		deposeTri(45);
	}*/

	int available = SERIAL_MAIN.available();
	if (available > MAX_READ) {
		available = MAX_READ;
	}
	for(int i = 0; i < available; i++) {
		// recuperer l'octet courant
		executeCmd(generic_serial_read());
	}

	available = SERIAL_FWD.available();
	if (available > MAX_READ) {
		available = MAX_READ;
	}
	for(int i = 0; i < available; i++) {
		serial_send(SERIAL_FWD.read());
	}

	if (use_act) {
		updateBras();
	}
}

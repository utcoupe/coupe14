
/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/

#include <Servo.h>
#include "Arduino.h"
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

	SERIAL_MAIN.begin(57600, SERIAL_8O1);
	SERIAL_FWD.begin(57600, SERIAL_8O1); //Forward
#ifdef DEBUG
	Serial3.begin(115200);
#endif

	initAct();
	initSize();
	digitalWrite(PIN_DEBUG_LED, LOW);
}

void loop(){
	if (!isInitDone()) { //SI on est pas encore initilisé on envoit une demande de reset
		protocol_send_reset();
	}

	int available = SERIAL_MAIN.available();
	if (available > MAX_READ) {
		available = MAX_READ;
	}
	for(int i = 0; i < available; i++) {
		// recuperer l'octet courant
		executeCmd(generic_serial_read());
	}

	updateAct();

	int availablefwd = SERIAL_FWD.available();
	if (availablefwd > MAX_READ) {
		availablefwd = MAX_READ;
	}
	for(int i = 0; i < availablefwd; i++) {
		serial_send(SERIAL_FWD.read());
	}

	updateAct();
}

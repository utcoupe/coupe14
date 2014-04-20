#include "actions.h"
#include "Servo.h"
#include "parameters.h"
#include "serial_switch.h"
#include "AccelStepper.h"
#include "TimerThree.h"
#include "AFMotor.h"

#include <math.h>
#include <Arduino.h>

extern Servo servoRet, servoBrasAngle, servoBrasDist;
extern AF_DCMotor pump_motor;
extern AF_Stepper stepper_motor;
//AccelStepper stepperAsc(1, PIN_STEPPER_STEP, PIN_STEPPER_DIR);
AccelStepper stepperAsc(forwardstep, backwardstep);

static int goal_hauteur = 0;
static double current_a;
static int current_l;

static bool got_tri = false; //True si triangle en suspension

void initPins(){
	//RETOURNEMENT
        
	pinMode(PIN_SERVO_RET, OUTPUT);
	servoRet.attach(PIN_SERVO_RET);

	//BRAS
	pinMode(PIN_SERVO_BRAS_ANGLE, OUTPUT);
	servoBrasAngle.attach(PIN_SERVO_BRAS_ANGLE);
	pinMode(PIN_SERVO_BRAS_DIST, OUTPUT);
	servoBrasDist.attach(PIN_SERVO_BRAS_DIST);
       
	pinMode(PIN_STEPPER_STEP, OUTPUT);
	pinMode(PIN_STEPPER_DIR, OUTPUT);
	pinMode(PIN_INTERRUPT_BRAS, INPUT_PULLUP);
	pinMode(PIN_INT_HAUT_ASC, INPUT_PULLUP);
}

void init_act() {
	//Moteurs :
	pump_motor.run(FORWARD);
	cmdBrasServ(0, ANGLE_DIST_MAX_DEG);
	//servoBrasAngle.write(0);
	//servoBrasDist.write(ANGLE_DIST_MAX);
	servoRet.write(ANGLE_RET); 
	pump(true);
	delay(1000);
	pump(false);
	cmdBrasServ(ANGLE_DEPOT, 0);
	servoRet.write(0); 
	//servoBrasAngle.write(ANGLE_DEPOT);
	//servoBrasDist.write(0);

	stepperAsc.setAcceleration(AMAX_STEPPER);
	stepperAsc.setMaxSpeed(VMAX_STEPPER);
	stepperAsc.move(3000);
	while(digitalRead(PIN_INT_HAUT_ASC) == 1) { //Tant qu'on est pas en haut
		stepperAsc.run();
	}
	attachInterrupt(INT_ASC_HAUT, topStop, FALLING);
	stepperAsc.setCurrentPosition(HAUTEUR_MAX * H_TO_STEP);
}

void asc_int() {
	if (digitalRead(PIN_INTERRUPT_BRAS) == 0) {
		//On touche un triangle
		Timer3.detachInterrupt();
		got_tri = true;
	}
	else if (-1 == goal_hauteur) {
		Timer3.detachInterrupt();
		got_tri = false;
	}
	cmdBras(-1,-1,-1, 0);
}

void cmdBras(double angle, int length, int height, int n_depot) {
	static int step = 0, l = 0, h = 0;
	static double a = 0;
	static int depot = n_depot;
	if (height >= 0 && step != 0) { //Si nouvel ordre avant le dernier : on le vire
		return;
	}
	switch(step) {
		case 0:
			//Lever asc
			if (height >= 0) { //-1 après la fin d'une action complete
				a = angle; l = length; h = height;
				cmdAsc(HAUTEUR_MAX);
				step++;
			}
			break;
		case 1:
			//ouvrir bras, descendre asc
			cmdBrasServ(a, l);
			//delayMicroseconds(x); //Si necessaire
			cmdAsc(h);
			pump(true);
			step++;
			break;
		case 2: {
			//Remonter asc
			int hauteur = h + MARGE_DEPOT;
			if (depot < 0) { //A l'arriere
				hauteur = MAX(hauteur, (ABS(depot) + MARGE_DEPOT));
			}
			hauteur = MIN(hauteur, HAUTEUR_MAX);
			cmdAsc(hauteur);
			step++;
			break;
			}
		case 3:
			//On rentre le bras
			//Se placer au bon rangement
			if (depot < 0) { //Depot a l'arriere
				cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
			}
			else {
				cmdBrasServ(ANGLE_DEPOT_RET, LONGUEUR_DEPOT_RET);
			}
			step++;
			Timer3.attachInterrupt(callback, 300000);
			break;
		case 4:
			//Lacher pompe, remonter
			pump(false);
			cmdAsc(HAUTEUR_MAX);
			step++;
			break;
		case 5:
			cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
			step = 0;
			setLastId();
			break;
	}
}

void cmdAsc(int h) { //h en mm
	//TESTS SECU
	goal_hauteur = h * H_TO_STEP;
	Timer3.attachInterrupt(asc_int, PERIOD_STEPPER);
}

void cmdBrasServ(double a, int l) {
	//TESTS SECU
	int d = (BRAS_OFFSET_DIST + l);
	double alpha;
	if (d == 0) {
		alpha = 0;
	} else {
		//alpha = ((L1*L1 - L2*L2 + d*d) / (2*d*L1))*180/M_PI;
		alpha = l;
	}
	int theta = (a + BRAS_OFFSET_ANGLE)*180/M_PI;
	servoBrasAngle.write(theta);
	servoBrasDist.write(alpha);
	current_a = a;
	current_l = l;
}

int getCurrentHauteur() {
	return stepperAsc.currentPosition() / H_TO_STEP;
}

void pump(bool etat) {
	if (etat) {
		pump_motor.setSpeed(PWM_PUMP);
	} else {
		pump_motor.setSpeed(0);
	}
}

void callback() {
	cmdBras(-1,-1,-1,0);
}

void topStop() {
	stepperAsc.move(0);
	stepperAsc.runToPosition();
}

void forwardstep() {  
	  stepper_motor.onestep(FORWARD, DOUBLE);
}
void backwardstep() {  
	  stepper_motor.onestep(BACKWARD, DOUBLE);
}

#include "actions.h"
#include "Servo.h"
#include "parameters.h"
#include "serial_switch.h"
#include "AccelStepper.h"
#include "TimerOne.h"
#include "AFMotor.h"
#include "compat.h"

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
static int step = 0;

volatile bool next_step= true;
volatile bool got_tri = false; //True si triangle en suspension

void initPins(){
	pinMode(PIN_DEBUG_LED, OUTPUT);//led debug
	digitalWrite(PIN_DEBUG_LED, HIGH);
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
	cmdBrasServ(0, LONGUEUR_MAX);
	servoRet.write(ANGLE_RET); 
	pump(true);
	delay(1000);
	pump(false);
	cmdBrasServ(ANGLE_DEPOT, 0);
	servoRet.write(0); 

	stepperAsc.setAcceleration(AMAX_STEPPER);
	stepperAsc.setMaxSpeed(VMAX_STEPPER);
	stepperAsc.move(6000);
	while(digitalRead(PIN_INT_HAUT_ASC) == 1) { //Tant qu'on est pas en haut
		stepperAsc.run();
	}
	stepperAsc.setCurrentPosition(HAUTEUR_MAX*H_TO_STEP + MARGE_SECU_TOP);
	topStop();
	//attachInterrupt(INT_ASC_HAUT, topStop, FALLING);
	cmdBras(0.1, 30, 20, 50);
}

void asc_int() {
	if ((step == 2) && digitalRead(PIN_INTERRUPT_BRAS) == 0) {
		//On touche un triangle
		Timer1.detachInterrupt();
		got_tri = true;
		next_step = true;
	}
	else if (stepperAsc.distanceToGo() == 0) {
		Timer1.detachInterrupt();
		got_tri = false;
		next_step = true;
	}
}

void cmdBras(double angle, int length, int height, int n_depot) {
	stepperAsc.run();
	static int l = 0, h = 0;
	static double a = 0;
	static int depot = n_depot;
	static long start = timeMicros();

	//Temporisation avant etapes 4 et 5
	if (step == 4 || step == 5) {
		long wait_time;
		if (step == 4) {
			wait_time = DELAY_REPLI_BRAS;
		} else {
			wait_time = DELAY_STOP_PUMP;
		}
		long t = timeMicros();
		if ((t - start) > wait_time) {
			next_step = true;
		}
	}

	if (next_step) {
		if (height >= 0 && step != 0) { //Si nouvel ordre avant le dernier : on le vire
			return;
		}
		switch(step) {
			case 0:
				//Lever asc
				if (height >= 0) { //-1 après la fin d'une action complete
					a = angle; l = length; h = height; depot = n_depot;
					cmdAsc(HAUTEUR_MAX);
					step++;
				}
				break;
			case 1:
				//ouvrir bras, descendre asc
				cmdBrasServ(a, l);
				cmdAsc(h);
				pump(true);
				step++;
				break;
			case 2: {
				//Remonter asc
				int hauteur;
				if (got_tri) {
					hauteur = abs(depot) + MARGE_DEPOT;
					step++;
				} else { hauteur = HAUTEUR_MAX;
					pump(false);
					step=6;
				}
				hauteur = MIN(hauteur, HAUTEUR_MAX);
				cmdAsc(hauteur);
				break;
				}
			case 3:
				//On rentre le bras
				//Se placer au bon rangement
				if (depot > 0) { //Depot a l'arriere
					cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
				}
				else {
					cmdBrasServ(ANGLE_DEPOT_RET, LONGUEUR_DEPOT_RET);
				}
				step++;
				next_step = false;
				start = timeMicros();
				break;
			case 4:
				//Lacher pompe, remonter
				pump(false);
				step++;
				next_step = false;
				start = timeMicros();
				break;
			case 5:
				cmdAsc(HAUTEUR_MAX);
				step++;
				break;
			case 6:
				cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
				step = 0;
				next_step = true;
				cmdBras(0.1, 30, 20, 80);
				setLastId();
				break;
		}
	}
}

void cmdAsc(int h) { //h en mm
	//TESTS SECU
	next_step = false;
	goal_hauteur = h * H_TO_STEP;
	stepperAsc.moveTo(goal_hauteur);
	Timer1.attachInterrupt(asc_int, PERIOD_STEPPER);
}

void cmdBrasServ(double a, int l) {
	//TESTS SECU
	int d = (BRAS_OFFSET_DIST + l)/ 10.0;
	double alpha = 0.2472*pow(d,4) - 2.759*pow(d,3) + 7.843*pow(d,2) + 6.942*d;
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
	static bool reset = true;
	if (reset) {
		next_step = false;
		reset = !reset;
	} else {
		next_step = true;
		reset = true;
	}
	if (next_step == true) {
		Timer1.detachInterrupt();
	}
}

void topStop() {
	stepperAsc.moveTo(HAUTEUR_MAX*H_TO_STEP);
	stepperAsc.runToPosition();
}

void forwardstep() {  
	  stepper_motor.onestep(FORWARD, DOUBLE);
}
void backwardstep() {  
	  stepper_motor.onestep(BACKWARD, DOUBLE);
}

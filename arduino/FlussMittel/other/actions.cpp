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

Servo servoRet, servoBrasAngle, servoBrasDist;
AF_Stepper stepper_motor(200, 2);
AF_DCMotor pump_motor(2, MOTOR12_64KHZ);
//AccelStepper stepperAsc(1, PIN_STEPPER_STEP, PIN_STEPPER_DIR);
AccelStepper stepperAsc(forwardstep, backwardstep);

static int goal_hauteur = 0, step = -1, current_alpha = 0, current_theta = 0;
static bool block_before_depot = false;
static bool call_critical = false;

bool use_act = true;

volatile bool next_step = true; //Blocage entre les etapes
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

void initAct() {
	//Moteurs :
	pump_motor.run(FORWARD);
	cmdBrasServ(-M_PI/4, LONGUEUR_MAX);
	servoRet.write(ANGLE_RET); 
	pump(true);
	delay(1000);
	pump(false);
	cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
	servoRet.write(180); 
	stepperAsc.setAcceleration(AMAX_STEPPER);
	stepperAsc.setMaxSpeed(VMAX_STEPPER);
	stepperAsc.move(6000);
	while(digitalRead(PIN_INT_HAUT_ASC) == 1) { //Tant qu'on est pas en haut
		updateBras();
		stepperAsc.run();
	}
	stepperAsc.setCurrentPosition(HAUTEUR_MAX*H_TO_STEP + MARGE_SECU_TOP);
	topStop();
	//attachInterrupt(INT_ASC_HAUT, topStop, FALLING); //Commenté à cause des micro-interuptions
}

void stopAct() {
	use_act = false;
}

void getTri(long x, long y, int h) {
	block_before_depot = true;
	next_step = true;
	x -= X_BRAS; y -= Y_BRAS;
	double a = atan2(y, x);
	int l = (int)sqrt(x*x + y*y);
	cmdBras(a, l, h);
}

void deposeTri(int dep) {
	block_before_depot = false;
	cmdBras(-1, -1, -1, dep);
}

void updateBras() {
	stepperAsc.run();
	if (call_critical) {
		criticalCmdBras();
	}
	cmdBras();
}

void cmdBras(double angle, int length, int height, int n_depot) {
	//Fonction de traitement
	static int l = 0, h = 0;
	static double a = 0;
	static int depot = n_depot;
	static unsigned long time_end = 0;

	//Nouvel ordre et conditions pour "couper" l'ordre actuel
	if (height >= 0 && step == -1) {
		a = angle; l = length; h = height; depot = n_depot;
		step = 0;
		next_step = true;
	}

	//Mise à jour du depot en cours
	if (n_depot != 0 && step <= 2) {
		depot = n_depot;
	}

	//Temporisation avant etapes 4 et 5
	if (timeMicros() > time_end && time_end != 0) {
		next_step = true;
		time_end = -1;
	}

	if (next_step) {
		next_step = false;
		if (height >= 0 && step != 0) { //Si nouvel ordre avant le dernier : on le vire
			return;
		}
		switch(step) {
			case 0: {
				//Lever asc
				int hauteur = MIN(HAUTEUR_MAX, MAX(getCurrentHauteur() + MARGE_PREHENSION, h + MARGE_PREHENSION));
				cmdAsc(hauteur);
				step++;
				}
				break;
			case 1:
				//ouvrir bras, descendre asc
				cmdBrasServ(a, l);
				cmdAsc(HAUTEUR_MIN);
				pump(true);
				step++;
				break;
			case 2: 
				//Remonter asc
				setLastId(); //Fin de préhension
				if (got_tri) {
					if (!block_before_depot) { //On continue
						int hauteur = MAX(getCurrentHauteur() + MARGE_PREHENSION, abs(depot) + MARGE_DEPOT);
						if (depot < 0) {
							hauteur = HAUTEUR_MAX;
							servoRet.write(180);
						}
						step++;
						hauteur = MIN(hauteur, HAUTEUR_MAX);
						cmdAsc(hauteur);
					} else { //On a un tri mais on attends l'IA
						next_step = true;
					}
				} else { //Pas de triangles
					pump(false);
					step=5;
					cmdAsc(HAUTEUR_MAX);
				}
				break;
			case 3:
				//On rentre le bras
				//Se placer au bon rangement
				if (depot > 0) { //Depot a l'arriere
					cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
					time_end = timeMicros() + (long)DELAY_REPLI_BRAS*1000;
				}
				else {
					cmdBrasServ(ANGLE_DEPOT_RET, LONGUEUR_DEPOT_RET);
					time_end = timeMicros() + (long)(DELAY_REPLI_BRAS+SECU_DELAY_ROT_BRAS)*1000;
				}
				step++;
				break;
			case 4:
				//Lacher pompe
				pump(false);
				if (depot > 0) { //Depot a l'avant
					step = 6;
				} else { //Depot a l'arriere
					step = 5;
				}
				time_end = timeMicros() + (long)DELAY_STOP_PUMP*1000;
				break;
			case 5:
				//Remise du bras au niveau du depot avant
				cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
				time_end = timeMicros() + (long)DELAY_REPLI_BRAS2*1000; 
				step++;
				break;
			case 6:
				got_tri = false;
				setLastId(); //Fin de depot
				if (depot < 0) {
					servoRet.write(165);
				}
				cmdAsc(HAUTEUR_MIN); //On descend le bras pour bloquer les triangles
				step = -1;
				break;
		}
	}
}

void cmdAsc(int h) { //h en mm
	if (h > HAUTEUR_MAX) {
		h = HAUTEUR_MAX;
		digitalWrite(PIN_DEBUG_LED, LOW);
	} else if (h < HAUTEUR_MIN) {
		h = HAUTEUR_MIN;
		digitalWrite(PIN_DEBUG_LED, LOW);
	}
	//TESTS SECU
	goal_hauteur = h * H_TO_STEP;
	stepperAsc.moveTo(goal_hauteur);
	Timer1.attachInterrupt(ascInt, PERIOD_STEPPER);
}

void cmdBrasServ(double a, int l) {
	call_critical = false;
	//COMMANDE
	int d = (l - BRAS_OFFSET_DIST)/ 10.0;
	double alpha = 0.2472*pow(d,4) - 2.759*pow(d,3) + 7.843*pow(d,2) + 6.942*d; //regression polynomiale
	int theta = -a*180.0/M_PI - BRAS_OFFSET_ANGLE;

	//TESTS SECU
	if (theta > ANGLE_ANGLE_MAX) {
		theta = ANGLE_ANGLE_MAX;
		digitalWrite(PIN_DEBUG_LED, LOW);
	} else if (theta < 0) {
		theta = 0;
		digitalWrite(PIN_DEBUG_LED, LOW);
	}
	if (alpha > ANGLE_DIST_MAX) {
		alpha = ANGLE_DIST_MAX;
		digitalWrite(PIN_DEBUG_LED, LOW);
	} else if (alpha < 0) {
		alpha = 0;
		digitalWrite(PIN_DEBUG_LED, LOW);
	}
	if (theta > ANGLE_INSIDE_ROBOT || current_theta > ANGLE_INSIDE_ROBOT) {
		//ATTENTION : on va ou viens de l'interieur du robot
		call_critical = true;
		criticalCmdBras(theta, alpha);
	} else {
		//ORDRE
		servoBrasAngle.write(theta);
		servoBrasDist.write(alpha);
		current_theta = theta;
		current_alpha = alpha;
	}
}

void criticalCmdBras(int n_theta, int n_alpha) {
	static int theta, alpha;
	static int step = 0;
	static long time = 0;
	if (n_theta >= 0) {
		step = 0;
		time = timeMicros();
		theta = n_theta;
		alpha = n_alpha;
	}
	switch (step) {
		case 0: {
			servoBrasDist.write(0);
			current_alpha = 0;
			long new_time = timeMicros();
			if ((new_time - time) > (long)SECU_DELAY_REPLI_BRAS*1000) {
				step++;
				time = new_time;
			}
			}
			break;
		case 1: {
			servoBrasAngle.write(theta);
			current_theta = theta;
			long new_time = timeMicros();
			if ((new_time - time) > (long)SECU_DELAY_ROT_BRAS*1000) {
				step++;
				time = new_time;
			}
			}
			break;
		case 2:
			//Cas spécial : dépot à l'arriere: on a le droit de deployer le bras
			if (theta >= (ANGLE_DEPOT_RET*180/M_PI - BRAS_OFFSET_ANGLE - 10) || theta <= ANGLE_INSIDE_ROBOT) {
				servoBrasDist.write(alpha);
				current_alpha = alpha;
			}
			call_critical = false;
			step = -1;
			break;
		}
}

int getCurrentHauteur() {
	return stepperAsc.currentPosition() / H_TO_STEP;
}

void ascInt() {
	if (stepperAsc.distanceToGo() == 0) {
		if (step == 2) {
			got_tri = false;
		}
		Timer1.detachInterrupt();
		next_step = true;
	}
	if (digitalRead(PIN_INTERRUPT_BRAS) == 0) {
		//On touche un triangle
		if (step == 2 || step == -1) {
			Timer1.detachInterrupt();
			next_step = true;
			got_tri = true;
			stepperAsc.move(0);
		}
	}
}

void pump(bool etat) {
	if (etat) {
		pump_motor.setSpeed(PWM_PUMP);
	} else {
		pump_motor.setSpeed(0);
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

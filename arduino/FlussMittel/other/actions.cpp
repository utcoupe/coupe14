#include "actions.h"
#include "Servo.h"
#include "parameters.h"
#include "serial_switch.h"
#include "AccelStepper.h"
#include "TimerThree.h"

#include <math.h>
#include <Arduino.h>

extern Servo servoRet, servoBrasAngle, servoBrasDist;
extern AccelStepper stepperAsc;

static int goal_hauteur = 0;

static bool last_tri_found = false;
static bool got_tri = false; //True si triangle en suspension


void init_act() {
	//Moteurs :

	servoRet.write(0); 
	servoBrasDist.write(LONGUEUR_DEPOT);
	servoBrasAngle.write(90);
	stepperAsc.setAcceleration(AMAX_STEPPER);
	stepperAsc.setMaxSpeed(VMAX_STEPPER);
	stepperAsc.moveTo(-3000);
	while(digitalRead(PIN_INT_HAUT_ASC) == 1) { //Tant qu'on est pas en haut
		stepperAsc.run();
	}
	attachInterrupt(PIN_INT_HAUT_ASC, topStop, FALLING);
}

void asc_int() {
	if (digitalRead(PIN_INTERRUPT_BRAS) == 0) {
		//On touche un triangle
		//Timer8.detachInterrupt();
		Timer3.detachInterrupt();
		got_tri = true;
	}
	else if (-1 == goal_hauteur) {
		//Timer8.detachInterrupt();
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
				hauteur = MAX(hauteur, ABS(depot) + MARGE_DEPOT);
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
			//Timer8.attachInterrupt(callback).start(300000);
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
	goal_hauteur = h * H_TO_STEP;
	Timer3.attachInterrupt(asc_int, PERIOD_STEPPER);
	//Timer8.attachInterrupt(asc_int).setFrequency(FREQUENCY_STEPPER).start();
}

void cmdBrasServ(double a, int l) {
	int d = (BRAS_OFFSET_DIST + l);
	double alpha = ((L1*L1 - L2*L2 + d*d) / 2*d*L1)*180/M_PI;
	int theta = (a + BRAS_OFFSET_ANGLE)*180/M_PI;
	servoBrasAngle.write(theta);
	servoBrasDist.write(alpha);
}

void pump(bool etat) {
}

void callback() {
	cmdBras(-1,-1,-1,0);
}
void topStop() {
	stepperAsc.stop();
	stepperAsc.runToPosition();
}

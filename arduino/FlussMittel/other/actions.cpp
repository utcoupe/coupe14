#include "actions.h"
#include "Servo.h"
#include "parameters.h"
#include <math.h>
#include <Arduino.h>

extern Servo servoBras, servoRet, servoBrasAngle, servoBrasDist;

static int hauteur_bras = 0; //On conserve la hauteur à tout moment. En step
static int goal_hauteur = hauteur_bras;

static bool last_tri_found = false;
static bool got_tri = false; //True si triangle en suspension


void asc_int() {
	if (digitalRead(PIN_INTERRUPT_BRAS) == 0) {
		//On touche un triangle
		Timer8.detachInterrupt();
		got_tri = true;
	}
	else if (hauteur_bras < goal_hauteur) {
		//MONTER
		hauteur_bras++;
		//TODO : Vérifier sens, verifier step
		digitalWrite(PIN_STEPPER_DIR, LOW);
		digitalWrite(PIN_STEPPER_STEP, HIGH);
		delayMicroseconds(DELAY_STEPPER_CONTROLER);
		digitalWrite(PIN_STEPPER_STEP, LOW);
	}
	else if (hauteur_bras > goal_hauteur) {
		//BAISSER
		hauteur_bras--;
		//TODO : Vérifier sens, verifier step
		digitalWrite(PIN_STEPPER_DIR, HIGH);
		digitalWrite(PIN_STEPPER_STEP, HIGH);
		delayMicroseconds(DELAY_STEPPER_CONTROLER);
		digitalWrite(PIN_STEPPER_STEP, LOW);
	}
	else if (hauteur_bras == goal_hauteur) {
		Timer8.detachInterrupt();
		got_tri = false;
		cmdBras(-1,-1,-1, 0);
	}
}

void cmdBras(double angle, int length, int height, bool n_depot) {

	static int step = 0, l = 0, h = 0;
	static double a = 0;
	static bool depot = n_depot; //True si depot dans la reserve, false si a l'arreire
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
			//TODO ALLUMER POMPE
			step++;
			break;
		case 2:
			//Remonter asc
			cmdAsc(HAUTEUR_MAX);
			step++;
			break;
		case 3:
			//Se placer au bon rangement
			if (depot) {
				cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
				//delayMicroseconds(x); //Si necessaire
				cmdAsc(h); //TODO HAUTEUR DEPOT VARIABLE
			}
			else {
				cmdBrasServ(ANGLE_DEPOT_RET, LONGUEUR_DEPOT_RET);
				//delayMicroseconds(x); //Si necessaire
				cmdAsc(HAUTEUR_DEPOT_RET);
			}
			step++;
			break;
		case 4:
			//Lacher pompe, remonter
			//TODO LACHER POMPE
			//TODO COMPTER TRIANGLES
			cmdAsc(HAUTEUR_MAX);
			step = 0;
			break;
	}
}

void cmdAsc(int h) { //h en mm
	goal_hauteur = h * H_TO_STEP;
	Timer8.attatchInterrupt(asc_int).setFrequency(FREQUENCY_STEPPER).start();
}

void cmdBrasServ(double a, int l) {
	int d = (BRAS_OFFSET_DIST + l);
	double alpha = ((L1*L1 - L2*L2 + d*d) / 2*d*L1)*180/M_PI;
	int theta = (a + BRAS_OFFSET_ANGLE)*180/M_PI;
	servoBrasAngle.write(theta);
	servoBrasDist.write(alpha);
}

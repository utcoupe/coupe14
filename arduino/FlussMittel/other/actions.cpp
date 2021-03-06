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


/* /!\ NE PAS REUTILISER /!\ 
 *
 * Code de bourrin, dévelopé rapidement
 * aucune flexibilité, bourré de hacks */

Servo servoRet, servoBrasAngle, servoBrasDist;
AF_Stepper stepper_motor(200, 2);
AF_DCMotor pump_motor(2, MOTOR12_64KHZ);
AccelStepper stepperAsc(forwardstep, backwardstep);

static int goal_hauteur = 0, step = -1, current_alpha = 0, current_theta = 0, tri_in_depot = 0;
static bool block = false;
static bool call_critical = false;
static enum action action_en_cours = None;

bool use_act = true;
int jack_state = 1;

volatile bool next_step = false; //Blocage entre les etapes
volatile bool got_tri = false; //True si triangle en suspension

void updateAct() {
	if (use_act) {
		updateBras();
		callbackRet();
	}
	updateJackState();
}

void updateJackState() {
	static int last_state = 0;
	int state = digitalRead(PIN_JACK);
	if (state == HIGH && last_state == HIGH) {
		jack_state = 0; //PAS DE JACK
	} else {
		jack_state = 1;
	}
	last_state = state;
}

void initPins(){
	pinMode(PIN_JACK, INPUT_PULLUP);
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
       
	pinMode(PIN_INTERRUPT_BRAS, INPUT_PULLUP);
	pinMode(PIN_INT_HAUT_ASC, INPUT_PULLUP);

	pinMode(PIN_VALVE, OUTPUT);
}

void initAct() {
	//Moteurs :
	pump_motor.run(FORWARD);
	cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
	servoRet.write(150); 
	pump(true);
	stepperAsc.setAcceleration(AMAX_STEPPER);
	stepperAsc.setMaxSpeed(VMAX_STEPPER);
	stepperAsc.move(6000);
	while (digitalRead(PIN_INT_HAUT_ASC) == 1) {
		updateBras();
	}
	topStop();
	pump(false);
	cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
	cmdAsc(HAUTEUR_GARDE_DEPOT);
	while (!next_step)
		stepperAsc.run();
	next_step = true;
	servoRet.write(180); 
}

void callbackRet(int use) {
	if (use_act) {
		static long time_end = 0;
		static bool active = false;
		long now = timeMillis();
		if (use == ACTIVATE) { //Set timer
			time_end = now + DELAY_RET;
			servoRet.write(ANGLE_RET);
			active = true;
		} else if (active) { //update regulier
			if (now >= time_end && use_act) {
				servoRet.write(180);
				setLastId();
				active = false;
			}
		}
	}
}


void stopAct() {
	use_act = false;
}

bool readyForNext() {
	if (action_en_cours == None) 
		return true;
	if (action_en_cours == TriPush && step > 4)
		return true;
	if (action_en_cours == BrasDepot && step > 7)
		return true;
	return false;
}

void getBrasDepot(int x, int y) {
	if (readyForNext()) {
		action_en_cours = BrasDepot;
		step = -1;
		x -= X_BRAS; y -= Y_BRAS;
		double a = atan2(y, x);
		int l = (int)sqrt(x*x + y*y);
		cmdBrasDepot(a, l);
	}
}

void getTriPush() {
	if (readyForNext()) {
		action_en_cours = TriPush;
		step = -1;
		cmdTriPush();
	}
}

void getTriBordure() {
	if (readyForNext()) {
		action_en_cours = TriBordure;
		step = -1;
		block = true;
		cmdTriBordure();
	}
}

void getTriBordureRepliBras() {
	if (action_en_cours == TriBordure && step == 3) {
		block = false;
		next_step = true;
	}
}

void getTri(long x, long y, int h) {
	if (readyForNext()) {
		action_en_cours = BrasVentouse;
		step = -1;
		block = true;
		x -= X_BRAS; y -= Y_BRAS;
		double a = atan2(y, x);
		int l = (int)sqrt(x*x + y*y);
		cmdBrasVentouse(a, l, h);
	}
}

void deposeTri(int dep) {
	next_step = true;
	block = false;
	cmdBrasVentouse(-1, -1, -1, dep);
}

void updateBras() {
	if (false && digitalRead(PIN_INT_HAUT_ASC) == LOW) {
		topStop();
	} else {
		stepperAsc.run();
		if (call_critical) {
			criticalCmdBras();
		}
		switch(action_en_cours) {
			case BrasVentouse:
				cmdBrasVentouse();
				break;
			case TriBordure:
				cmdTriBordure();
				break;
			case TriPush:
				cmdTriPush();
				break;
			case BrasDepot:
				cmdBrasDepot();
				break;
			default:
				break;
		}
	}
}

void cmdBrasDepot(double a, int l) {
	static unsigned long time_end = 0;
	static int hauteur_revele, longueur = 0;
	static double angle = 0;
	if (step == -1) { //Debut
		angle = a;
		longueur = l;
		step = 0;
		next_step = true;
	}
	//Temporisation
	if (timeMicros() > time_end && time_end != 0) {
		next_step = true;
		time_end = 0;
	}
	if (next_step) {
		next_step = false;

		switch(step) {
			case 0:
				cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
				pump(true);
				time_end = timeMicros() + (long)DELAY_REPLI_BRAS2*1000;
				step++;
				break;
			case 1:
				cmdAsc(HAUTEUR_GARDE_DEPOT);
				step++;
				break;
			case 2: {
				hauteur_revele = getCurrentHauteur() + MARGE_PREHENSION; //On remontera toujours par rapport à la position actulle, pour eviter de pousser un triangles (petite perte pour grande securité)
				int hauteur = MIN(HAUTEUR_MAX, hauteur_revele);
				cmdAsc(hauteur);
				step++;
				break;
			}
			case 3:
				cmdBrasServ(ANGLE_REPLI_TRI, LONGUEUR_BRAS_AVANT_DEPOT); //Pas d'attente ici, cela ne devrai pas etre la peine, sinon, implémenter time_end
				step++;
				time_end = timeMicros() + (long)DELAY_REPLI_BRAS2*1000;
				break;
			case 4:
				cmdAsc(HAUTEUR_BRAS_DEPOT);
				step++;
				break;
			case 5:
				cmdBrasServ(angle, longueur); //Pas d'attente ici, cela ne devrai pas etre la peine, sinon, implémenter time_end
				time_end = timeMicros() + (long)DELAY_SERVO_PUSH*1000;
				step++;
				break;
			case 6:
				pump(false);
				tri_in_depot--;
				time_end = timeMicros() + (long)DELAY_STOP_PUMP*1000;
				step++;
				break;
			case 7: {
				int hauteur = MIN(HAUTEUR_MAX, MAX(hauteur_revele - 30, getCurrentHauteur()));
				cmdAsc(hauteur);
				step++;
				setLastId();
				break;
				}
			case 8:
				cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
				cmdAsc(HAUTEUR_GARDE_DEPOT);
				step = -1;
				action_en_cours = None;
				break;
		}
	}
}

void cmdTriPush() {
	static unsigned long time_end = 0;
	static int hauteur_revele;
	if (step == -1) { //Debut
		step = 0;
		next_step = true;
	}
	//Temporisation
	if (timeMicros() > time_end && time_end != 0) {
		next_step = true;
		time_end = 0;
	}
	if (next_step) {
		next_step = false;

		switch(step) {
			case 0: {
				hauteur_revele = getCurrentStockHeight() + MARGE_PREHENSION; //On remontera toujours par rapport à la position actulle, pour eviter de pousser un triangles (petite perte pour grande securité)
				int hauteur = MIN(HAUTEUR_MAX, MAX(hauteur_revele, HAUTEUR_PUSH_TRI));
				cmdAsc(hauteur);
				step++;
				break;
			}
			case 1:
				cmdBrasServ(ANGLE_REPLI_TRI, LONGUEUR_PUSH_TRI); //Pas d'attente ici, cela ne devrai pas etre la peine, sinon, implémenter time_end
				step++;
				next_step = true;
				break;
			case 2:
				cmdAsc(HAUTEUR_TRI_BORDURE);
				step++;
				break;
			case 3:
				//Pour rentrer ici, next_step doit etre mis à true par la fonction getTriBordureRepliBras()
				cmdBrasServ(ANGLE_OUVERT, LONGUEUR_PUSH_TRI);
				time_end = timeMicros() + (long)DELAY_SERVO_PUSH*1000;
				step++;
				break;
			case 4:
				cmdAsc(hauteur_revele);
				cmdBrasServ(ANGLE_REPLI_TRI, LONGUEUR_MIN); //Pas d'attente ici, cela ne devrai pas etre la peine, sinon, implémenter time_end
				step++;
				setLastId(); 
				break;
			case 5: //On abaisse le bras sur les triangles du depot
				cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
				cmdAsc(HAUTEUR_GARDE_DEPOT); //On descend le bras pour bloquer les triangles
				step = -1;
				action_en_cours = None;
				break;
		}
	}
}

void cmdTriBordure() {
	static unsigned long time_end = 0;
	if (step == -1) { //Debut
		step = 0;
		next_step = true;
		block = true;
	}
	//Temporisation
	if (timeMicros() > time_end && time_end != 0) {
		next_step = true;
		time_end = 0;
	}
	if (next_step) {
		next_step = false;

		switch(step) {
			case 0: 
				cmdAsc(HAUTEUR_MAX);
				step++;
				break;
			case 1:
				cmdBrasServ(ANGLE_OUVERT, LONGUEUR_TRI_BORDURE); //Pas d'attente ici, cela ne devrai pas etre la peine, sinon, implémenter time_end
				step++;
				next_step = true;
				break;
			case 2:
				cmdAsc(HAUTEUR_TRI_BORDURE);
				step++;
				break;
			case 3:
				setLastId(); 
				if (!block) {
					//Pour rentrer ici, next_step doit etre mis à true par la fonction getTriBordureRepliBras()
					cmdBrasServ(ANGLE_REPLI_TRI, LONGUEUR_TRI_BORDURE);
					time_end = timeMicros() + (long)DELAY_REPLI_BRAS2*1000;
					step++;
				}
				break;
			case 4:
				cmdAsc(getCurrentStockHeight() + MARGE_PREHENSION);
				step++;
				break;
			case 5: //On abaisse le bras sur les triangles du depot
				setLastId(); //Fin
				cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
				cmdAsc(HAUTEUR_GARDE_DEPOT); //On descend le bras pour bloquer les triangles
				step = -1;
				action_en_cours = None;
				break;
		}
	}
}


void cmdBrasVentouse(double angle, int length, int height, int n_depot) {
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
	if (n_depot != 0 && step <= 3) {
		depot = n_depot;
	}

	//Temporisation avant etapes 4 et 5
	if (timeMicros() > time_end && time_end != 0) {
		next_step = true;
		time_end = 0;
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
				time_end = timeMicros() + (long)(SECU_DELAY_ROT_BRAS)*1000;
				step++;
				break;
			case 2:
				cmdAsc(HAUTEUR_MIN);
				pump(true);
				step++;
				break;
			case 3: 
				//Remonter asc
				if (got_tri) {
					if (!block) { //On continue
						int hauteur = MIN(HAUTEUR_MAX, MAX(MAX(getCurrentHauteur() + MARGE_PREHENSION, h + MARGE_PREHENSION), abs(depot) + MARGE_DEPOT));
						if (depot < 0) {
							hauteur = MAX(hauteur, HAUTEUR_DEPOT_ARRIERE);
							servoRet.write(180);
						}
						step++;
						hauteur = MIN(hauteur, HAUTEUR_MAX);
						cmdAsc(hauteur);
					} else {
						setLastId(); //Fin de préhension
					}
				} else { //Pas de triangles
					pump(false);
					step=7;
					cmdAsc(getCurrentStockHeight() + MARGE_PREHENSION);
				}
				break;
			case 4:
				//On rentre le bras
				//Se placer au bon rangement
				if (depot > 0) { //Depot a l'arriere
					cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
					time_end = timeMicros() + (long)DELAY_REPLI_BRAS_AVANT_POMPE*1000;
				}
				else {
					cmdBrasServ(ANGLE_DEPOT_RET, LONGUEUR_DEPOT_RET);
					time_end = timeMicros() + (long)(DELAY_REPLI_BRAS_ARRIERE_POMPE)*1000;
				}
				step++;
				break;
			case 5:
				if (depot >= 0) {
					cmdAsc(getCurrentStockHeight() + MARGE_PREHENSION);
				} else {
					cmdAsc(HAUTEUR_MAX);
				}
				step++;
				break;
			case 6:
				//Lacher pompe
				pump(false);
				if (depot > 0) { //Depot a l'avant
					tri_in_depot++;
					step = 8;
				} else { //Depot a l'arriere
					step = 7;
				}
				time_end = timeMicros() + (long)DELAY_STOP_PUMP*1000;
				break;
			case 7:
				//Remise du bras au niveau du depot avant
				cmdBrasServ(ANGLE_DEPOT, LONGUEUR_DEPOT);
				time_end = timeMicros() + (long)DELAY_REPLI_BRAS2*1000; 
				step++;
				break;
			case 8:
				got_tri = false;
				setLastId(); //Fin de depot
				cmdAsc(HAUTEUR_GARDE_DEPOT); //On descend le bras pour bloquer les triangles
				action_en_cours = None;
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
	int d = (l - BRAS_OFFSET_DIST);
	double alpha = 1.61e-6*pow(d,4) - 1.79e-4*pow(d,3) + 5.54e-3*pow(d,2) + 5.59e-1*d ; //regression polynomiale
	a += atan2(DECALAGE_VENT_AXE, l);
	int theta = ANGLE_ANGLE_MAX + (a*180.0/M_PI + BRAS_OFFSET_ANGLE);

	//TESTS SECU
	if (theta > ANGLE_ANGLE_MAX) {
		theta = ANGLE_ANGLE_MAX;
		digitalWrite(PIN_DEBUG_LED, LOW);
	} else if (theta < ANGLE_ANGLE_MIN) {
		theta = ANGLE_ANGLE_MIN;
		digitalWrite(PIN_DEBUG_LED, LOW);
	}
	if (alpha < ANGLE_DIST_MAX) {
		alpha = ANGLE_DIST_MAX;
		digitalWrite(PIN_DEBUG_LED, LOW);
	} else if (alpha > ANGLE_DIST_MIN) {
		alpha = ANGLE_DIST_MIN;
		digitalWrite(PIN_DEBUG_LED, LOW);
	}
	if (theta < ANGLE_INSIDE_ROBOT) {
		//ATTENTION : on va ou viens de l'interieur du robot
		call_critical = true;
		criticalCmdBras(theta, alpha, 2);
	} else	if (current_theta < ANGLE_INSIDE_ROBOT) {
		//ATTENTION : on va ou viens de l'interieur du robot
		call_critical = true;
		criticalCmdBras(theta, alpha, 1);
	} else {
		//ORDRE
		servoBrasAngle.write(180-theta);
		servoBrasDist.write(alpha);
		current_theta = theta;
		current_alpha = alpha;
	}
}

//Direction : 1 : int vers ext
// 2: ext ver int
void criticalCmdBras(int n_theta, int n_alpha, int direction) {
	static int theta, alpha;
	static int step = 0;
	static long time = 0;
	if (n_theta >= 0) {
		if (direction == 1) {
			step = 1;
		} else {
			step = 0;
		}
		time = timeMicros();
		theta = n_theta;
		alpha = n_alpha;
	}
	switch (step) {
		case 0: {
			servoBrasDist.write(ANGLE_DIST_MAX);
			current_alpha = 0;
			long new_time = timeMicros();
			if ((new_time - time) > (long)SECU_DELAY_REPLI_BRAS*1000) {
				step++;
				time = new_time;
			}
			}
			break;
		case 1: {
			servoBrasAngle.write(180-theta);
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
			int angle_arriere = ANGLE_ANGLE_MAX + (ANGLE_DEPOT_RET*180.0/M_PI + BRAS_OFFSET_ANGLE + 10);
			if (theta <= angle_arriere || theta >= ANGLE_INSIDE_ROBOT) {
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

int getCurrentStockHeight() {
	return (tri_in_depot * 30) + HAUTEUR_MIN;
}

void ascInt() {
	static long start_time = -1;
	if (!next_step) {
		if (stepperAsc.distanceToGo() == 0) {
			if (step == 3 && action_en_cours == BrasVentouse) {
				if (start_time == -1) {
					start_time = timeMicros();
				} else if (timeMicros() - start_time > (long)500*1000) {
					got_tri = false;
					Timer1.detachInterrupt();
					next_step = true;
					start_time = -1;
				}
			} else {
				Timer1.detachInterrupt();
				next_step = true;
			}
		}
		if (digitalRead(PIN_INTERRUPT_BRAS) == 0) {
			//On touche un triangle
			if ((action_en_cours == BrasVentouse && step == 3)) {
				Timer1.detachInterrupt();
				next_step = true;
				got_tri = true;
				stepperAsc.move(20);
			} else if ((action_en_cours == BrasDepot && step == 1) || (action_en_cours == None && step == -1)) {
				Timer1.detachInterrupt();
				next_step = true;
				stepperAsc.move(0);
			}
		}
	}
}

void pump(bool etat) {
	static bool saved_etat = etat;
	if (etat == PAUSE_PUMP) {
		digitalWrite(PIN_VALVE, HIGH);
		pump_motor.setSpeed(0);
	} else  {
		if (etat == RESUME_PUMP) {
			etat = saved_etat;
		} else {
			saved_etat = etat;
		}
		if (etat) {
			digitalWrite(PIN_VALVE, LOW);
			pump_motor.setSpeed(PWM_PUMP);
		} else {
			digitalWrite(PIN_VALVE, HIGH);
			pump_motor.setSpeed(0);
		}
	}
}

void topStop() {
	stepperAsc.setAcceleration(30000);
	stepperAsc.setCurrentPosition(HAUTEUR_MAX*H_TO_STEP + MARGE_SECU_TOP);
	stepperAsc.moveTo(HAUTEUR_MAX*H_TO_STEP);
	stepperAsc.runToPosition();
	stepperAsc.setAcceleration(AMAX_STEPPER);
}

void forwardstep() {  
	  stepper_motor.onestep(FORWARD, DOUBLE);
}
void backwardstep() {  
	  stepper_motor.onestep(BACKWARD, DOUBLE);
}

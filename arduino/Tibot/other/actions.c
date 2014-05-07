#include "actions.h"
#include "Servo.h"
#include "parameters.h"
#include "compat.h"

static Servo servoFilet, servoBallesL, servoBallesR, servoBalai;

struct servoQueue {
	Servo* servo;
	int pos, delay;
	long start;
};

void retourServo(Servo *servo, int pos, int delay) {
	static servoQueue tab[12];
	static int inQueue = 0;
	if (servo != 0) { //Commande
		if (inQueue > 12) {
			return;
		}
		struct servoQueue s;
		s.servo = servo;
		s.pos = pos;
		s.start = timeMillis();
		s.delay = delay;
		tab[inQueue] = s;
		inQueue++;
	} else { //execution
		int i = 0, j;
		long now = timeMillis();
		while (i < inQueue) {
			if ((now - tab[i].start) > tab[i].delay) { //Retour du servo
				tab[i].servo->write(tab[i].pos);
				for (j=i; j<inQueue-1; j++) { //On supprime de la liste
					tab[j] = tab[j+1];
				}
				inQueue--;
			} else {
				i++;
			}
		}
	}
}

void tirBalles(int nbr) {
	static int tirs = 0;
	tirs += nbr;

	int angle_to_go_R, angle_to_go_L;
	if (tirs < 4) {
		angle_to_go_R = POS_BALLES_R0;
		switch (tirs) {
			case 1:
				angle_to_go_L = POS_BALLES_L1;
				break;
			case 2:
				angle_to_go_L = POS_BALLES_L2;
				break;
			case 3:
				angle_to_go_L = POS_BALLES_L3;
				break;
			default:
				angle_to_go_L = POS_BALLES_L0;
		}
	} else {
		angle_to_go_L = POS_BALLES_L3;
		switch (tirs - 3) {
			case 1:
				angle_to_go_R = POS_BALLES_R1;
				break;
			case 2:
				angle_to_go_R = POS_BALLES_R2;
				break;
			case 3:
				angle_to_go_R = POS_BALLES_R3;
				break;
			default:
				angle_to_go_R = POS_BALLES_R0;
		}
	} 
	servoBallesR.write(angle_to_go_R);
	servoBallesL.write(angle_to_go_L);
	retourServo(&servoBallesR, POS_BALLES_R0);
	retourServo(&servoBallesL, POS_BALLES_L0);
}

void balai(int side) {
	if (side == LEFT) 
		servoBalai.write(POS_BALAI_L);
	else if (side == RIGHT) 
		servoBalai.write(POS_BALAI_R);
	else if (side == MIDDLE) {
		servoBalai.write(POS_BALAI_INIT);
	}
}

void tirFilet() {
	servoFilet.write(POS_TIR_FILET);
	retourServo(&servoFilet, POS_FILET_INIT);
}

void initPins() {
	servoFilet.attach(PIN_SERVO_FILET);
	servoBallesL.attach(PIN_SERVO_BALLES_L);
	servoBallesR.attach(PIN_SERVO_BALLES_R);
	servoBalai.attach(PIN_SERVO_BALAI);
}

void initServos() {
	servoFilet.write(POS_FILET_INIT);
	servoBallesL.write(POS_BALLES_L0);
	servoBallesR.write(POS_BALLES_R0);
	servoBalai.write(POS_BALAI_INIT);
}


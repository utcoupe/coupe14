/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/

//#include "AFMotor.h"

#include <Servo.h>

#include "parameters.h"
#include "serial_switch.h"
#include "serial_defines.h"
#include "serial_types.h"

extern Servo servoBras;
//extern AF_DCMotor motor_ascenseur;
/*
void couper_asc () {
	detachInterrupt(INT_BAS_ASC);
	detachInterrupt(INT_HAUT_ASC);
	motor_ascenseur.setSpeed(0);
}*/


//La fonction renvoit le nombre d'octet dans ret, chaine de caractère de réponse. Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon){ 
	int ret_size = 0;
	switch(ordre){
	case O_BRAS_OUVRIR:
		if (!doublon) {
			//Execution des ordre
			servoBras.write(10);			
		}
		//Formation et envoi d'une réponse
		break;
	case O_BRAS_FERMER:
		if (!doublon) {
			//Execution des ordre
			servoBras.write(170);			
		}
		//Formation et envoi d'une réponse
		break;
/*	case O_MONTER_ASC:
		if (!doublon) {
			motor_ascenseur.setSpeed(255);
			motor_ascenseur.run(FORWARD);
			attachInterrupt(INT_HAUT_ASC, couper_asc, RISING);
		}
		break;
	case O_BAISSER_ASC:
		if (!doublon) {
			motor_ascenseur.setSpeed(255);
			motor_ascenseur.run(BACKWARD);
			attachInterrupt(INT_BAS_ASC, couper_asc, RISING);
		}
		break;*/
	default:
		return -1;//commande inconnue
	}
	return ret_size;
}
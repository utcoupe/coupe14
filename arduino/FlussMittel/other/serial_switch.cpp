/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/

#include "AFMotor_due.h"

#include <Servo.h>
#include <Arduino.h>

#include "parameters.h"
#include "serial_switch.h"
#include "serial_defines.h"
#include "serial_types.h"
#include "actions.h"

extern Servo servoBras, servoRet;
extern AF_DCMotor motor_ascenseur;

void couper_asc () {
	motor_ascenseur.setSpeed(0);
}


//La fonction renvoit le nombre d'octet dans ret, chaine de caractère de réponse. Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon){ 
	static int last_id = 0;
	int ret_size = 0;
	switch(ordre){
	case O_BRAS_OUVRIR:
		if (!doublon) {
			last_id = btoi(argv);
			argv+=2;
			//Execution des ordre
			servoBras.write(10);			
		}
		//Formation et envoi d'une réponse
		break;
	case O_BRAS_FERMER:
		if (!doublon) {
			last_id = btoi(argv);
			argv+=2;
			//Execution des ordre
			servoBras.write(170);			
		}
		//Formation et envoi d'une réponse
		break;
	case O_RET_OUVRIR:
		if (!doublon) {
			last_id = btoi(argv);
			argv+=2;
			servoRet.write(95);
		}
		break;
	case O_RET_FERMER:
		if (!doublon) {
			last_id = btoi(argv);
			argv+=2;
			servoRet.write(0);
		}
		break;
	case O_MONTER_ASC:
		if (!doublon) {
			last_id = btoi(argv);
			argv+=2;
			motor_ascenseur.run(FORWARD);
			motor_ascenseur.setSpeed(255);
		}
		break;
	case O_BAISSER_ASC:
		if (!doublon) {
			last_id = btoi(argv);
			argv+=2;
			motor_ascenseur.run(BACKWARD);
			motor_ascenseur.setSpeed(255);
		}
		break;
	case GET_LAST_ID:
		ret_size = 2;
		itob(last_id, ret);
		break;
	case RESET_ID:
		last_id = 0;
		break;
	default:
		return -1;//commande inconnue
	}
	return ret_size;
}

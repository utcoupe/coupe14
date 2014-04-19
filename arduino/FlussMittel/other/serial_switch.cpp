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

extern Servo servoRet;
extern AF_DCMotor motor_ascenseur;

int last_id = 0;
int next_last_id = 0;

//La fonction renvoit le nombre d'octet dans ret, chaine de caractère de réponse. Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon){ 
	int ret_size = 0;
	switch(ordre){
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
	case O_BRAS_DEPOT:
		if (!doublon) {
			next_last_id = btoi(argv);
			double a = btoi(argv+2) / 100.0;
			int l = btoi(argv+4);
			int h = btoi(argv+6);
			int depot = btoi(argv+8);
			cmdBras(a, l, h, depot);
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

void setLastId() {
	last_id = next_last_id;
}

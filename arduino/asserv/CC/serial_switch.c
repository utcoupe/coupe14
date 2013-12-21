/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/
#include "serial_switch.h"
#include "serial_defines.h"
#include "serial_types.h"
#include "control.h"
#include "compaArduino.h"

extern Control control;

//La fonction renvoit le nombre d'octet dans ret, chaine de caractère de réponse. Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon){ 
	int ret_size = 0;
	switch(ordre){
	case PINGPING:
                if (!doublon) {
			Serial2.print(control.getLenc()->getTicks());
			Serial2.print(control.getRenc()->getTicks());
		//	Serial2.print("coucou");
		}
		break;
	case A_GET_CODER:
		Serial2.println("");
		Serial2.print("X : ");
		Serial2.println(control.getPos().x);
		Serial2.print("Y : ");
		Serial2.println(control.getPos().y);
		Serial2.print("A : ");
		Serial2.println(control.getPos().angle);
		break;
	case A_GOTO:
		if (!doublon) {
			control.pushGoal(0, TYPE_POS, btoi(argv), btoi(argv+2), 0);
		}
		break;
	case A_ROT:
		if (!doublon) {
			control.pushGoal(0, TYPE_ANG, btof(argv), 0, 0);
		}
		break;
	case A_PWM_TEST:
		if (!doublon) {
			control.pushGoal(0, TYPE_PWM, btoi(argv), btoi(argv+2), btoi(argv+4));
		}
		break;
	case A_PIDA:
		if (!doublon) {
			control.setPID_angle(btoi(argv), btoi(argv+2), btoi(argv+3));
		}
		break;
	case A_PIDD:
		if (!doublon) {
			control.setPID_distance(btoi(argv), btoi(argv+2), btoi(argv+3));
		}
		break;
	case A_KILLG:
		if (!doublon) {
			control.nextGoal();
		}
		break;
	case A_CLEANG:
		if (!doublon) {
			control.clearGoals();
		}
		break;

/*	case ORDRE_001:
		if (!doublon) {
			//Execution des ordre
			//Les fonction btoi(), btol() et btof() aident à récupérer les arguments

			// Coder ici les actions à executer
		}
		//Formation et envoi d'une réponse
		//Les fonctions itob(), ltob() et itof() aident à formet les arguments

		//Coder ici la formation des données de retour

		break;*/
	default:
		return -1;//commande inconnue
	}
	return ret_size;
}

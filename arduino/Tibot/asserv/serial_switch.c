/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/
#include "serial_switch.h"
#include "serial_defines.h"
#include "serial_types.h"
#include "control.h"
#include "compat.h"

extern Control control;

//La fonction renvoit le nombre d'octet dans ret, chaine de caractère de réponse. Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon){ 
	int ret_size = 0;
	switch(ordre){
	case PINGPING:
                if (!doublon) {
			PDEBUGLN("PONG (nouveau)");
		}
		else{
			PDEBUGLN("PONG (ancien)");
		}
		break;
	case A_GET_CODER:
                if (!doublon) {
			PDEBUG("Codeur L : ");PDEBUGLN(control.getLenc()->getTicks());
			PDEBUG("Codeur R : ");PDEBUGLN(control.getRenc()->getTicks());
			PDEBUG("Angle pos : ");PDEBUGLN(control.getPos().angle);
                }
		ltob(control.getLenc()->getTicks(), ret);
		ltob(control.getRenc()->getTicks(), ret + 4);
		ret_size = 8;
		break;
	case A_GOTO:
                PDEBUG("Arg 1 : "); PDEBUGLN(btoi(argv));
                PDEBUG("Arg 2 : "); PDEBUGLN(btoi(argv+2));
		if (!doublon) {
			control.pushGoal(0, TYPE_POS, btoi(argv), btoi(argv+2), 0);
		}
		break;
	case A_ROT:
                PDEBUG("Arg : "); PDEBUGLN(btof(argv));
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
			control.setPID_angle(btof(argv), btof(argv+4), btof(argv+8));
		}
		break;
	case A_PIDD:
		if (!doublon) {
			control.setPID_distance(btof(argv), btof(argv+4), btof(argv+8));
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
	case A_RESET_POS:
		if (!doublon) {
			m_pos pos;
			pos.x = 0;
			pos.y = 0;
			pos.angle = 0;
			control.pushPos(pos);
		}
		break;
	case A_ACCMAX:
		if(!doublon) {
			control.setMaxAcc(btof(argv));
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

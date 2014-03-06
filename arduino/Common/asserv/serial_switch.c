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
	int id;
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
		ltob(control.getLenc()->getTicks(), ret);
		ltob(control.getRenc()->getTicks(), ret + 4);
		ret_size = 8;
		break;
	case A_GOTO:
		id = btoi(argv);
		argv += 2;
		if (!doublon) {
			control.pushGoal(id, TYPE_POS, btoi(argv), btoi(argv+2), 0);
		}
		break;
	case A_GOTOA:
		id = btoi(argv);
		argv += 2;
		if (!doublon) {
			control.pushGoal(id, TYPE_POS, btoi(argv), btoi(argv+2), 0);
			control.pushGoal(id, TYPE_ANG, btof(argv+4), 0, 0);
		}
		break;
	case A_ROT:
		id = btoi(argv);
		argv += 2;
		if (!doublon) {
			control.pushGoal(id, TYPE_ANG, btof(argv), 0, 0);
		}
		break;
	case A_PWM:
		id = btoi(argv);
		argv += 2;
		if (!doublon) {
			control.pushGoal(id, TYPE_PWM, btoi(argv), btoi(argv+2), btoi(argv+4));
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
			pos pos;
			pos.x = 0;
			pos.y = 0;
			pos.angle = 0;
			control.pushPos(pos);
		}
		break;
	case A_GET_POS:{
		pos pos = control.getPos();
		int x = pos.x, y = pos.y;
		float a = pos.angle;
		itob(x, ret);
		itob(y, ret+2);
		ftob(a, ret+4);
		ret_size = 8;
		break;
		}
	case A_ACCMAX:
		if(!doublon) {
			control.setMaxAcc(btof(argv));
		}
		break;
	case GET_LAST_ID:
		itob(control.getLastFinishedId(), ret);
		ret_size = 2;
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
	case PINGPING_AUTO:
		break;
	default:
		PDEBUGLN("ORDRE INCONNU");
		return -1;//commande inconnue
	}
	return ret_size;
}

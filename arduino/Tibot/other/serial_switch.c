/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/
#include "Arduino.h"

#include "actions.h"
#include "parameters.h"
#include "serial_switch.h"
#include "serial_defines.h"
#include "serial_types.h"

extern int jack_state;

//La fonction renvoit le nombre d'octet dans ret, chaine de caractère de réponse. Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon){ 
	static int last_id = 0;
	int ret_size = 0;
	switch(ordre){
	case O_TIR_FILET:
		last_id = btoi(argv);
		tirFilet();
		break;
	case O_BALAI: {
		last_id = btoi(argv);
		int side = btoi(argv+2);
		balai(side);
		}
		break;
	case O_TIR_BALLE: {
		last_id = btoi(argv);
		int tirs = btoi(argv+2);
		tirBalles(tirs);
		}
		break;
	case GET_LAST_ID:
		ret_size = 2;
		itob(last_id, ret);
		break;
	case RESET_ID:
		last_id = 0;
		break;
	case O_JACK_STATE:
		ret_size = 2;
		itob(jack_state, ret);
		break;
	default:
		return -1;//commande inconnue
	}
	return ret_size;
}

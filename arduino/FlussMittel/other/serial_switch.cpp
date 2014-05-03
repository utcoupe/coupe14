/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/

#include <Servo.h>
#include <Arduino.h>

#include "parameters.h"
#include "serial_switch.h"
#include "serial_defines.h"
#include "serial_types.h"
#include "actions.h"

extern Servo servoRet;
extern bool got_tri, use_act;

static int last_id = 0;
static int next_last_id = 0;
static const int overflow = 29999;

//La fonction renvoit le nombre d'octet dans ret, chaine de caractère de réponse. Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon){ 
	int ret_size = 0;
	switch(ordre){
	case O_RET_OUVRIR:
		if (!doublon && use_act) {
			last_id = btoi(argv);
			argv+=2;
			servoRet.write(95);
		}
		break;
	case O_RET_FERMER:
		if (!doublon && use_act) {
			last_id = btoi(argv);
			argv+=2;
			servoRet.write(0);
		}
		break;
	case O_GET_TRIANGLE:
		if (!doublon) {
			next_last_id = btoi(argv);
			int x = btoi(argv+2), y = btoi(argv+4), h = btoi(argv+6);
			getTri(x, y, h);
		}
		break;			
	case O_STORE_TRIANGLE:
		if (!doublon) {
			next_last_id = btoi(argv);
			deposeTri(btoi(argv+2));
		}
		break;
	case O_GET_BRAS_STATUS:
		ret_size = 2;
		last_id = btoi(argv);
		itob((int)got_tri,ret);
		break;
	case O_BRAS_OUVRIR:
		if (!doublon) {
			next_last_id = btoi(argv);
			getTriBordure();
		}
		break;
	case O_BRAS_FERMER:
		if (!doublon) {
			next_last_id = btoi(argv);
			getTriBordureRepliBras();
		}
		break;
	case PAUSE:
		use_act = false;
		break;
	case RESUME:
		use_act = true;
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
	if ((next_last_id > last_id) || (last_id - next_last_id > overflow/2)) {
		last_id = next_last_id;
	}
}

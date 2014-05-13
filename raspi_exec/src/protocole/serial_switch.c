/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/
#include "serial_switch.h"
#include "serial_defines.h"
#include "serial_types.h"
#include "../com.h"

#include <time.h>

void pushCamData(struct camData *data, int nbr) {
}

void pushHokData(struct hokData *data, int nbr) {
}

//La fonction renvoit le nombre d'octet dans ret, chaine de caractère de réponse. Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon){ 
	int ret_size = 0;
	switch(ordre){
		case T_GET_HOKUYO: {
			break;
			}
		case T_GET_CAM: {
			break;
			}
		default:
			return -1;//commande inconnue
	}
	return ret_size;
}

/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/
#include "serial_switch.h"
#include "serial_defines.h"
#include "serial_types.h"

#include <pthread.h>

static int red, yellow;
extern pthread_mutex_t mutex;

void pushData(int p_red, int p_yellow) {
	pthread_mutex_lock(&mutex);
	red = p_red;
	yellow = p_yellow;
	pthread_mutex_unlock(&mutex);
}

//La fonction renvoit le nombre d'octet dans ret, chaine de caractère de réponse. Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon){ 
	int ret_size = 0;
	switch(ordre){
	case GET_CAM: {
		pthread_mutex_lock(&mutex);
		itob(red, ret);
		itob(yellow, ret+2);
		pthread_mutex_unlock(&mutex);
		ret_size = 4;
		break;
	}
	default:
		return -1;//commande inconnue
	}
	return ret_size;
}

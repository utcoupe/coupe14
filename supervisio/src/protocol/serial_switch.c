/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/
#include "serial_switch.h"
#include "serial_defines.h"
#include "serial_types.h"

#include <pthread.h>

static visio_data data;
pthread_mutex_t mutex;

void pushData(visio_data pushed_data) {
	pthread_mutex_lock(&mutex);
	data = pushed_data;
	pthread_mutex_unlock(&mutex);
}

//La fonction renvoit le nombre d'octet dans ret, chaine de caractère de réponse. Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon){ 
	int ret_size = 0;
	switch(ordre){
	case GET_CAM: {
		pthread_mutex_lock(&mutex);
		pthread_mutex_unlock(&mutex);
		ret_size = 0;
		break;
	}
	default:
		return -1;//commande inconnue
	}
	return ret_size;
}

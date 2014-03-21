/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/
#include "serial_switch.h"
#include "serial_defines.h"
#include "serial_types.h"

#include <pthread.h>
#include <time.h>

static struct coord robots[MAX_ROBOTS];
static int number_robots;
static long data_time = 0;
extern pthread_mutex_t mutex;

void pushCoords(struct coord *n_robots, int n, long timestamp) {
	pthread_mutex_lock(&mutex); int i;
	for (i=0; i<n; i++){
		robots[i] = n_robots[i];
	}
	number_robots = n;
	data_time = timestamp;
	pthread_mutex_unlock(&mutex);
}

//La fonction renvoit le nombre d'octet dans ret, chaine de caractère de réponse. Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon){ 
	int ret_size = 0;
	switch(ordre){
	case GET_HOKUYO: {
		int i;
		pthread_mutex_lock(&mutex);
		for (i=0; i< number_robots ; i++) {
			itob(robots[i].x, ret+4*i);
			itob(robots[i].y, ret+4*i+2);
		}
		pthread_mutex_unlock(&mutex);
		for (; i < 4; i++) {
			itob(-1, ret+4*i);
			itob(-1, ret+4*i+2);
		}
		itob(data_time, ret+16);
		ret_size = 20;
		break;
		}
	default:
		return -1;//commande inconnue
	}
	return ret_size;
}

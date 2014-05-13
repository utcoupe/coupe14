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
#include <string.h>
#include <pthread.h>
#include <stdlib.h>

static struct camData lastCamData[MAX_TRI];
static struct hokData lastHokData[NBR_ROBOTS];
static int last_cam_nbr = 0;
static long last_hok_timestamp = 0;

static pthread_mutex_t mutexCam, mutexHok;


void pushCamData(struct camData *data, int nbr) {
	pthread_mutex_lock(&mutexCam);
	last_cam_nbr = nbr;
	memcpy(lastCamData, data, nbr*sizeof(struct camData));
	pthread_mutex_unlock(&mutexCam);
}

void pushHokData(struct hokData *data, long timestamp) {
	pthread_mutex_lock(&mutexHok);
	last_hok_timestamp = timestamp;
	memcpy(lastHokData, data, NBR_ROBOTS*sizeof(struct hokData));
	pthread_mutex_unlock(&mutexHok);
}

//La fonction renvoit le nombre d'octet dans ret, chaine de caractère de réponse. Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon){ 
	int ret_size = 0;
	switch(ordre){
		case T_GET_HOKUYO: {
			struct hokData data[NBR_ROBOTS];
			int i;
			long timestamp = 0;
			pthread_mutex_lock(&mutexHok);
			memcpy(data, lastHokData, NBR_ROBOTS*sizeof(struct hokData));
			timestamp = last_hok_timestamp;
			pthread_mutex_unlock(&mutexHok);

			ltob(timestamp, ret);
			ret+=4;
			for (i=0; i<NBR_ROBOTS; i++) {
				itob(data[i].x, ret+2*(2*i));
				itob(data[i].y, ret+2*((2*i)+1));
			}
			ret_size = 20;
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

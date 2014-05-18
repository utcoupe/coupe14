#include "hokuyoUrg.h"

#include <stdlib.h>
#include <stdio.h>
#include <urg_ctrl.h>
#include "global.h"


void*
initHokuyoUrg(char* device, double angleMin, double angleMax){
	urg_t *urg;
	urg = malloc(sizeof(urg_t));
	if( urg == NULL ) exit(EXIT_FAILURE);

	int error = urg_connect(urg, device, BAUDRATE_HOKUYOURG);

	if(error < 0){
		urg_disconnect(urg);
		fprintf(stderr, "%sconnection failed on %s\n",PREFIX, device);
		exit(EXIT_FAILURE);
	}
	
	printf("%sConnection établie à %s\n", PREFIX, device);

	printf("%sHokuyo init from %f to %f\n", PREFIX, angleMin*180/PI, angleMax*180/PI);
	urg_setCaptureTimes(urg, UrgInfinityTimes);
    error = urg_requestData(urg, URG_MD, urg_rad2index(urg, angleMin), urg_rad2index(urg, angleMax));//scan en continu, on ne garde que les point entre angleMin et angleMax
	
	printf("%sParameters set #1\n", PREFIX);

	if(error < 0){
		urg_disconnect(urg);
		fprintf(stderr, "%sconnection failed on starting on %s\n", PREFIX, device);
		exit(EXIT_FAILURE);
	}
	
	return urg;
}

void
resetHokuyoUrg(urg_t* urg, char *device, double angleMin, double angleMax){
	printf("%sHokuyo reinit from %f to %f\n", PREFIX, angleMin*180/PI, angleMax*180/PI);
	urg_disconnect(urg);
	urg_connect(urg, device, BAUDRATE_HOKUYOURG);
	urg_setCaptureTimes(urg, UrgInfinityTimes);
    int error = urg_requestData(urg, URG_MD, urg_rad2index(urg, angleMin), urg_rad2index(urg, angleMax));//scan en continu, on ne garde que les point entre angleMin et angleMax
	printf("%sParameters set #2\n", PREFIX);
	if(error < 0){
		urg_disconnect(urg);
		fprintf(stderr, "%sconnection failed on resetting\n", PREFIX);
		exit(EXIT_FAILURE);
	}
}

int
getnPointsHokuyoUrg(urg_t* urg){
	long int temp[MAX_DATA];
	return  urg_receiveData(urg, temp, MAX_DATA);
}

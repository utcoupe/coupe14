#include "hokuyoUrg.h"

#include <stdlib.h>
#include <stdio.h>
#include <urg_sensor.h>
#include <urg_serial_utils.h>
#include "global.h"


void*
initHokuyoUrg(char* device, double angleMin, double angleMax){
	urg_t *urg;
	urg = malloc(sizeof(urg_t));
	if( urg == NULL ) exit(EXIT_FAILURE);

	int error = urg_open(urg, URG_SERIAL, device, BAUDRATE_HOKUYOURG);

	if(error < 0){
		urg_close(urg);
		fprintf(stderr, "%s%s :: %s\n", PREFIX, "connection failed on open", urg_error(urg));
		exit(EXIT_FAILURE);
	}
	
	printf("%sConnection établie à %s\n", PREFIX, device);

	//printf("Hokuyo init from %f to %f\n", -angleMax*180/PI, -angleMin*180/PI);
    urg_set_scanning_parameter(urg, urg_rad2step(urg, -angleMax), urg_rad2step(urg, -angleMin), 0);//scan en continu, on ne garde que les point entre angleMin et angleMax
	
	printf("%sParameters set #1\n", PREFIX);

	error = urg_start_measurement(urg, URG_DISTANCE, URG_SCAN_INFINITY, 0);

	if(error < 0){
		urg_close(urg);
		fprintf(stderr, "%s%s :: %s\n", "connection failed on starting", PREFIX, urg_error(urg));
		exit(EXIT_FAILURE);
	}
	
	return urg;
}

void
resetHokuyoUrg(void* urg, double angleMin, double angleMax){
	urg_stop_measurement((urg_t*)urg);
	printf("%sHokuyo reinit from %f to %f\n", PREFIX, -angleMax*180/PI, -angleMin*180/PI);
	urg_set_scanning_parameter((urg_t*)urg, urg_rad2step(urg, -angleMax), urg_rad2step(urg, -angleMin), 0);
	printf("%sParameters set #2\n", PREFIX);

	int error = urg_start_measurement((urg_t*)urg, URG_DISTANCE, URG_SCAN_INFINITY, 0);
	if(error < 0){
		urg_close(urg);
		fprintf(stderr, "%s%s :: %s\n", "connection failed on restarting", PREFIX, urg_error((urg_t*)urg));
		exit(EXIT_FAILURE);
	}
}

int
getnPointsHokuyoUrg(void* urg){
	return urg_get_distance((urg_t*)urg, NULL, NULL);
}

double
getAngleFromIndexHokuyoUrg(void* urg, int index){
	return -urg_index2rad((urg_t*)urg, index);
}

void
getDistancesHokuyoUrg(void* urg, long* buffer){
	urg_get_distance((urg_t*)urg, buffer, NULL);
}



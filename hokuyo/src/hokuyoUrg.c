#include "hokuyoUrg.h"

#include <stdlib.h>
#include <stdio.h>
#include <urg_sensor.h>
#include <urg_serial_utils.h>



void*
initHokuyoUrg(char* device, double angleMin, double angleMax){
	urg_t *urg;
	urg = malloc(sizeof(urg_t));
	if( urg == NULL ) exit(EXIT_FAILURE);

	int error = urg_open(urg, URG_SERIAL, device, BAUDRATE_HOKUYOURG);

	if(error < 0){
		urg_close(urg);
		fprintf(stderr, "%s :: %s\n", "connection failed", urg_error(urg));
		exit(EXIT_FAILURE);
	}
	
	printf("Connection établie à %s\n", device);

    urg_set_scanning_parameter(urg, urg_rad2step(urg, angleMin), urg_rad2step(urg, angleMax), 0);//scan en continu, on ne garde que les point entre angleMin et angleMax
	
	printf("Parameters set\n");

	error = urg_start_measurement(urg, URG_DISTANCE, URG_SCAN_INFINITY, 0);

	if(error < 0){
		urg_close(urg);
		fprintf(stderr, "%s :: %s\n", "connection failed", urg_error(urg));
		exit(EXIT_FAILURE);
	}
	
	return urg;
}

int
getnPointsHokuyoUrg(void* urg){
	return urg_get_distance((urg_t*)urg, NULL, NULL);
}

double
getAngleFromIndexHokuyoUrg(void* urg, int index){
	return urg_index2rad((urg_t*)urg, index);
}

void
getDistancesHokuyoUrg(void* urg, long* buffer){
	urg_get_distance((urg_t*)urg, buffer, NULL);
}



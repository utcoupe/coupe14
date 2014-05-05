#include "hokuyoUrg.h"

#include <stdlib.h>
#include <stdio.h>
#include <urg_sensor.h>
#include <urg_serial_utils.h>
#include "global.h"


urg_t*
initHokuyoUrg(char* device, double angleMin, double angleMax){
	urg_t *urg;
	urg = malloc(sizeof(urg_t));
	if( urg == NULL ) exit(EXIT_FAILURE);

	int error = urg_open(urg, URG_SERIAL, device, BAUDRATE_HOKUYOURG);

	if(error < 0){
		urg_close(urg);
		fprintf(stderr, "%s%s :: %s on %s\n", PREFIX, "connection failed on open", urg_error(urg), device);
		exit(EXIT_FAILURE);
	}
	
	printf("%sConnection établie à %s\n", PREFIX, device);

	printf("Hokuyo init from %f to %f\n", angleMin*180/PI, angleMax*180/PI);
    urg_set_scanning_parameter(urg, urg_rad2step(urg, angleMin), urg_rad2step(urg, angleMax), 0);//scan en continu, on ne garde que les point entre angleMin et angleMax
	
	printf("%sParameters set #1\n", PREFIX);

	if (!CAPTURE_EACH_TIME) {
		error = urg_start_measurement(urg, URG_DISTANCE, URG_SCAN_INFINITY, 0);

		if(error < 0){
			urg_close(urg);
			fprintf(stderr, "%s%s :: %s on %s\n", "connection failed on starting", PREFIX, urg_error(urg), device);
			exit(EXIT_FAILURE);
		}
	}
	
	return urg;
}

void
resetHokuyoUrg(urg_t* urg, double angleMin, double angleMax){
	urg_stop_measurement(urg);
	printf("%sHokuyo reinit from %f to %f\n", PREFIX, angleMin*180/PI, angleMax*180/PI);
	urg_set_scanning_parameter(urg, urg_rad2step(urg, angleMin), urg_rad2step(urg, angleMax), 0);
	printf("%sParameters set #2\n", PREFIX);

	if (!CAPTURE_EACH_TIME) {
		int error = urg_start_measurement(urg, URG_DISTANCE, URG_SCAN_INFINITY, 0);
		if(error < 0){
			urg_close(urg);
			fprintf(stderr, "%s%s :: %s\n", "connection failed on resetting", PREFIX, urg_error(urg));
			exit(EXIT_FAILURE);
		}
	}
}

void
closeHokuyoUrg(urg_t* urg){
	urg_close(urg);
}
/*
void
restartHokuyoUrg(urg_t* urg){
	if (!CAPTURE_EACH_TIME) {
		int error = urg_start_measurement(urg, URG_DISTANCE, URG_SCAN_INFINITY, 0);
		if(error < 0){
			urg_close(urg);
			fprintf(stderr, "%s%s :: %s\n", "connection failed on restarting", PREFIX, urg_error(urg));
			exit(EXIT_FAILURE);
		}
	}
	printf("%sHokuyo succesfully restarted !\n", PREFIX);
}
*/
int
getnPointsHokuyoUrg(urg_t* urg){
	return urg_get_distance(urg, NULL, NULL);
}

double
getAngleFromIndexHokuyoUrg(urg_t* urg, int index){
	return urg_index2rad(urg, index);
}

void
getDistancesHokuyoUrg(urg_t* urg, long* buffer){
	if (CAPTURE_EACH_TIME) {
		int error = urg_start_measurement(urg, URG_DISTANCE, 1, 0);
		if(error < 0){
			urg_close(urg);
			fprintf(stderr, "start_measurement failed\n");
			exit(EXIT_FAILURE);
		}
		urg_get_distance(urg, buffer, NULL);
	} else {
		urg_get_distance(urg, buffer, NULL);
	}
}



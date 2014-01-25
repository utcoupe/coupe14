#include "lidar.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <urg_utils.h>
#include "hokuyoUrg.h"
#include "global.h"


struct lidar
initLidar(enum lidarModel model, char* device, struct coord position, double orientation, double angleMin, double angleMax){
	struct lidar l;
	l.model = model;
	l.pos = position;
	l.orientation = orientation;

	if(model == hokuyo_urg){

		l.lidarObject = initHokuyoUrg(device, angleMin, angleMax);

		int nAngles = getnPointsHokuyoUrg(l.lidarObject);
		double *angles = malloc(sizeof(double)*nAngles);
		if(angles == NULL) exit(EXIT_FAILURE);
		for(int i=0; i<nAngles; i++){
			angles[i] = getAngleFromIndexHokuyoUrg(l.lidarObject, i) + orientation;
		}

		l.fm = initFastmath( nAngles, angles );

		free(angles);
	}
	
	l.points = malloc(sizeof(struct coord)*l.fm.n);
	if(l.points == NULL) exit(EXIT_FAILURE);	

	return l;
}

struct coord*
getPoints(struct lidar* l){
	long* buffer = malloc(sizeof(long)*l->fm.n);
	getDistancesHokuyoUrg(l->lidarObject, buffer);
	for(int i=0; i<l->fm.n; i++){
		//hokuyo scans in indirect direction, buffer is reversed
		l->points[i].x = fastCos(l->fm, i)*buffer[l->fm.n-i] + l->pos.x;
		l->points[i].y = fastSin(l->fm, i)*buffer[l->fm.n-i] + l->pos.y;		
	}
	/*
	for(int i=0; i<l->fm.n; i++){
		printf("%i\t%ld\t%i\t%i\n", i, buffer[l->fm.n-i], l->points[i].x, l->points[i].y);
	}*/
	free(buffer);
	return l->points;
}











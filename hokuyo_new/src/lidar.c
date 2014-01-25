#include "lidar.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <urg_utils.h>
#include <math.h>
#include "hokuyoUrg.h"
#include "global.h"

static long maxDistance;

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

	maxDistance = MAX_DISTANCE;

	return l;
}

char
invalidDistance(long d){
	if(d > maxDistance) return 1;
	return 0;
}

char
invalidPoint(struct coord p){	
	if(p.x < DISTANCE_TO_EDGE_MIN || p.x > TAILLE_TABLE_X-DISTANCE_TO_EDGE_MIN
		|| p.y < DISTANCE_TO_EDGE_MIN || p.y > TAILLE_TABLE_Y-DISTANCE_TO_EDGE_MIN){
		return 1;
	}
	return 0;
}

struct coord*
getPoints(struct lidar* l){
	long* buffer = malloc(sizeof(long)*l->fm.n);
	getDistancesHokuyoUrg(l->lidarObject, buffer);
	for(int i=0; i<l->fm.n; i++){
		//hokuyo scans in indirect direction, buffer is reversed

		#ifndef DEBUG_DO_NOT_REMOVE_POINTS
		if(invalidDistance(buffer[l->fm.n-i])){
			l->points[i].x = 0;
			l->points[i].y = 0;
			continue;
		}
		#endif 

		l->points[i].x = fastCos(l->fm, i)*buffer[l->fm.n-i] + l->pos.x;
		l->points[i].y = fastSin(l->fm, i)*buffer[l->fm.n-i] + l->pos.y;

		#ifndef DEBUG_DO_NOT_REMOVE_POINTS
		if(invalidPoint(l->points[i])){
			l->points[i].x = 0;
			l->points[i].y = 0;
			continue;
		}
		#endif 
	}
	/*
	for(int i=0; i<l->fm.n; i++){
		printf("%i\t%ld\t%i\t%i\n", i, buffer[l->fm.n-i], l->points[i].x, l->points[i].y);
	}*/
	free(buffer);
	return l->points;
}












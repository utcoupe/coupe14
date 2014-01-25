#include "lidar.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <urg_utils.h>
#include "hokuyoUrg.h"
#include "global.h"

static int preSmoothingValues[] = PRESMOOTHINGSTEPS;

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
		l.preSmoothingIndex = 0;

		free(angles);
	}
	
	l.points = malloc(sizeof(struct coord)*l.fm.n);
	if(l.points == NULL) exit(EXIT_FAILURE);

	for(int i=0; i<PRESMOOTHING; i++){
		l.realPoints[i] = malloc(sizeof(int)*l.fm.n);
		if(l.realPoints[i] == NULL) exit(EXIT_FAILURE);
		memset(l.realPoints[i], 0, sizeof(int)*l.fm.n);
	}		

	return l;
}

struct coord*
getPoints(struct lidar* l){
	long* buffer = malloc(sizeof(long)*l->fm.n);
	getDistancesHokuyoUrg(l->lidarObject, buffer);
	for(int i=0; i<l->fm.n; i++){
		//hokuyo scans in indirect direction, buffer is reversed
		l->realPoints[l->preSmoothingIndex][i] = buffer[l->fm.n-i];

		long sum = 0;
		for(int j=0; j<PRESMOOTHING; j++){
			sum += l->realPoints[ (l->preSmoothingIndex+3-j)%3 ][i] * preSmoothingValues[(l->preSmoothingIndex+j)%3]; 
		}
		sum /= 100;

		l->points[i].x = fastCos(l->fm, i)*sum + l->pos.x;
		l->points[i].y = fastSin(l->fm, i)*sum + l->pos.y;		
	}
	/*
	for(int i=0; i<l->fm.n; i++){
		printf("%i\t%ld\t%i\t%i\n", i, buffer[l->fm.n-i], l->points[i].x, l->points[i].y);
	}*/
	free(buffer);
	l->preSmoothingIndex = (l->preSmoothingIndex+1) % PRESMOOTHING;
	return l->points;
}











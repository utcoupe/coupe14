#include "lidar.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <err.h>
#include <urg_ctrl.h>
#include "hokuyoUrg.h"
#include "global.h"
#include "robot.h"
#include "fast_math.h"

static long maxDistance;
static long distanceThMin, distanceThMax;

double
theta(struct coord lidar, struct coord marker){
	struct coord delta;
	delta.x = marker.x - lidar.x;
	delta.y = marker.y - lidar.y;

	return modTwoPi(atan2(delta.y, delta.x));
}



struct coord* getPointsCalibrate(struct lidar* l, char calibration);

struct lidar
initLidarAndCalibrate(char* device, struct coord position, double orientation, double angleMin, double angleMax){
	angleMax = modTwoPi(angleMax);
	angleMin = modTwoPi(angleMin);
	orientation = modTwoPi(orientation);

	struct coord markerPos;
	markerPos.x = MARKER_R_POS_X;
	markerPos.y = MARKER_R_POS_Y;
	distanceThMin = dist_squared(position, markerPos);
	distanceThMax = pow(sqrt(distanceThMin)+MARKER_DETECTION_ZONE_SIZE/2,2);
	distanceThMin = pow(sqrt(distanceThMin)-MARKER_DETECTION_ZONE_SIZE/2,2);
	//double thetaTh = (angleMax+angleMin)/2.0;
	double thetaTh = theta(position, markerPos);
	printf("%sthetha TH:%f  -> %f\n", PREFIX, thetaTh, thetaTh*180/PI);
	
	struct lidar l = initLidar(device, position, orientation, thetaTh-MARKER_DETECTION_ANGLE, thetaTh+MARKER_DETECTION_ANGLE);

	long sumMarkerPos_x = 0, sumMarkerPos_y = 0;
	int nbClustersFound = 0;
	for(int i=0; i<MARKER_DETECTION_STEPS; i++){
		getPointsCalibrate(&l, 1);
		struct coord clusters[MAX_ROBOTS];
		int nClusters = getRobots(l.points, l.fm.n, clusters);
		if(nClusters != 1){
			printf("%scould not calibrate !!! (%i clusters found in zone on iteration %i)\n", PREFIX, nClusters, i);
		}else{
			sumMarkerPos_x += clusters[0].x;
			sumMarkerPos_y += clusters[0].y;
			nbClustersFound++;
		}
	}
	if(nbClustersFound < MARKER_DETECTION_STEPS/2){
		printf("%sCalibration could not be done !\nexiting...\n", PREFIX);
		exit(EXIT_SUCCESS);
	}
	struct coord markerRPos;
	markerRPos.x = sumMarkerPos_x / nbClustersFound;
	markerRPos.y = sumMarkerPos_y / nbClustersFound;

	double thetaR = theta(position, markerRPos);
	printf("%sthetha R:%f  -> %f\tcalculated on %i iterations\n", PREFIX, thetaR, thetaR*180/PI, nbClustersFound);
	l.orientation += thetaTh - thetaR;
	printf("%snew orientation:%f\n", PREFIX, l.orientation*180/PI);

	///////
	resetHokuyoUrg(l.lidarObject, device, modTwoPi(angleMin-l.orientation), modTwoPi(angleMax-l.orientation));
	int nAngles = getnPointsHokuyoUrg(l.lidarObject);
	double *angles = malloc(sizeof(double)*nAngles);
	if(angles == NULL) exit(EXIT_FAILURE);
	for(int i=0; i<nAngles; i++){
		angles[i] = urg_index2rad(l.lidarObject, i) + l.orientation;
	}
	freeFastmath(l.fm);
	l.fm = initFastmath( nAngles, angles );

	free(l.points);
	l.points = malloc(sizeof(struct coord)*l.fm.n);
	if(l.points == NULL) exit(EXIT_FAILURE);

	free(angles);



	return l;
}

struct lidar
initLidar(char* device, struct coord position, double orientation, double angleMin, double angleMax){
	angleMax = modTwoPi(angleMax);
	angleMin = modTwoPi(angleMin);
	orientation = modTwoPi(orientation);
	struct lidar l;
	l.pos = position;
	l.orientation = orientation;

	printf("%sorientation:%f\n", PREFIX, orientation*180/PI);

	l.lidarObject = initHokuyoUrg(device, angleMin - orientation, angleMax - orientation);

	int nAngles = getnPointsHokuyoUrg(l.lidarObject);
	double *angles = malloc(sizeof(double)*nAngles);
	if(angles == NULL) exit(EXIT_FAILURE);
	for(int i=0; i<nAngles; i++){
		angles[i] = urg_index2rad(l.lidarObject, i) + l.orientation;
	}

	l.fm = initFastmath( nAngles, angles );

	free(angles);
	
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

char
invalidPointCalibration(struct coord lidar, struct coord p){
	long dist = dist_squared(lidar, p);
	//printf("validCalibrationPoint?:%f\tin [%f\t,\t%f]\n", sqrt(dist), sqrt(distanceThMin), sqrt(distanceThMax));
	if(dist < distanceThMin || dist > distanceThMax)
		return 1;
	/*if(p.x < MARKER_R_POS_X-MARKER_DETECTION_ZONE_SIZE/2 || p.x > MARKER_R_POS_X+MARKER_DETECTION_ZONE_SIZE/2
		|| p.y < MARKER_R_POS_Y-MARKER_DETECTION_ZONE_SIZE/2 || p.y > MARKER_R_POS_Y+MARKER_DETECTION_ZONE_SIZE/2)
		return 1;*/
	return 0;
}


struct coord*
getPointsCalibrate(struct lidar* l, char calibration){
	long* buffer = malloc(sizeof(long)*l->fm.n);
	if( buffer == NULL ){
		err(1, "buffer malloc");
	}


	urg_receiveData(l->lidarObject, buffer, MAX_DATA);
	for(int i=0; i<(l->fm.n); i++){

		#ifndef DEBUG_DO_NOT_REMOVE_POINTS
		if(invalidDistance(buffer[i])){
			//printf("invalidDistance[%i]\t%li\n", i, buffer[i]);
			l->points[i].x = 0;
			l->points[i].y = 0;
			continue;
		}
		#endif 

		l->points[i].x = fastCos(l->fm, i)*buffer[i] + l->pos.x;
		l->points[i].y = fastSin(l->fm, i)*buffer[i] + l->pos.y;

		if(calibration){
			if(invalidPointCalibration(l->pos, l->points[i])){
				l->points[i].x = 0;
				l->points[i].y = 0;
				continue;
			}
		}else{
			#ifndef DEBUG_DO_NOT_REMOVE_POINTS
			if(invalidPoint(l->points[i])){
				//printf("invalidPoint[%i]\t%li\t(%i,%i)\n", i, buffer[i], l->points[i].x, l->points[i].y);
				l->points[i].x = 0;
				l->points[i].y = 0;
				continue;
			}
			//printf("validPoint[%i]\t%li\t(%i,%i)\n", i, buffer[i], l->points[i].x, l->points[i].y);
			#endif
		}
	}
	
	/*
	for(int i=0; i<l->fm.n; i++){
		printf("%i\t%ld\t%i\t%i\n", i, buffer[i], l->points[i].x, l->points[i].y);
	}//*/
	free(buffer);
	return l->points;
}

struct coord*
getPoints(struct lidar* l){
	return getPointsCalibrate(l, 0);
}












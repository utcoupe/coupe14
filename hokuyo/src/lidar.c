#include "lidar.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <urg_utils.h>
#include <math.h>
#include <err.h>
#include "hokuyoUrg.h"
#include "global.h"
#include "robot.h"

static long maxDistance;
static long distanceThMin, distanceThMax;

double
theta(struct coord lidar, struct coord marker){
	struct coord delta;
	delta.x = lidar.x - marker.x;
	delta.y = lidar.y - marker.y;

	//printf("dx=%i\tdy=%i\n", delta.x, delta.y);
	if(delta.x == 0) return PI/2;

	return atan((double)delta.y / (double)delta.x); // -(-) -> +
}



struct coord* getPointsCalibrate(struct lidar* l, char calibration);

struct lidar
initLidarAndCalibrate(enum lidarModel model, char* device, struct coord position, double orientation, double angleMin, double angleMax){
	struct coord markerPos;
	markerPos.x = MARKER_R_POS_X;
	markerPos.y = MARKER_R_POS_Y;
	distanceThMin = dist_squared(position, markerPos);
	distanceThMax = pow(sqrt(distanceThMin)+MARKER_DETECTION_ZONE_SIZE/2,2);
	distanceThMin = pow(sqrt(distanceThMin)-MARKER_DETECTION_ZONE_SIZE/2,2);
	double thetaTh = theta(position, markerPos);
	printf("%sthetha TH:%f  -> %f\n", PREFIX, thetaTh, thetaTh*180/PI);
	//printf("detectionMinAngle:%f\tdetectionMaxAngle%f\n", (thetaTh-MARKER_DETECTION_ANGLE/2)*180/PI, (thetaTh+MARKER_DETECTION_ANGLE/2)*180/PI );
	
	struct lidar l = initLidar(model, device, position, orientation, thetaTh-MARKER_DETECTION_ANGLE/2, thetaTh+MARKER_DETECTION_ANGLE);

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
	resetHokuyoUrg(l.lidarObject, angleMin-l.orientation, angleMax-l.orientation);
	int nAngles = getnPointsHokuyoUrg(l.lidarObject);
	double *angles = malloc(sizeof(double)*nAngles);
	if(angles == NULL) exit(EXIT_FAILURE);
	for(int i=0; i<nAngles; i++){
		angles[i] = getAngleFromIndexHokuyoUrg(l.lidarObject, i) + l.orientation;
		//printf("angleFromhokuyo:%f\tangle[%i]:%f\n", getAngleFromIndexHokuyoUrg(l.lidarObject, i)*180/PI, i, angles[i]*180/PI);
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
initLidar(enum lidarModel model, char* device, struct coord position, double orientation, double angleMin, double angleMax){
	struct lidar l;
	l.model = model;
	l.pos = position;
	l.orientation = orientation;

	printf("%sorientation:%f\n", PREFIX, orientation*180/PI);

	if(model == hokuyo_urg){

		l.lidarObject = initHokuyoUrg(device, angleMin - orientation, angleMax - orientation);

		int nAngles = getnPointsHokuyoUrg(l.lidarObject);
		double *angles = malloc(sizeof(double)*nAngles);
		if(angles == NULL) exit(EXIT_FAILURE);
		for(int i=0; i<nAngles; i++){
			angles[i] = getAngleFromIndexHokuyoUrg(l.lidarObject, i) + orientation;
			//printf("angleFromhokuyo:%f\tangle[%i]:%f\n", getAngleFromIndexHokuyoUrg(l.lidarObject, i)*180/PI, i, angles[i]*180/PI);
		}

		l.fm = initFastmath( nAngles, angles );

		free(angles);
	}
	
	l.points = malloc(sizeof(struct coord)*l.fm.n);
	if(l.points == NULL) exit(EXIT_FAILURE);	

	maxDistance = MAX_DISTANCE;

	return l;
}

void closeLidar(struct lidar * l){
	if(l->model == hokuyo_urg){
		closeHokuyoUrg(l->lidarObject);
	}
}

/*
void restartLidar(struct lidar * l){
	if(l->model == hokuyo_urg){
		restartHokuyoUrg(l->lidarObject);
	}
}*/

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


	getDistancesHokuyoUrg(l->lidarObject, buffer);
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
	}*/
	free(buffer);
	return l->points;
}

struct coord*
getPoints(struct lidar* l){
	return getPointsCalibrate(l, 0);
}












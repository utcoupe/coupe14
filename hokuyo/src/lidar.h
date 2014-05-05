#ifndef LIDAR_H
#define LIDAR_H

#include "fast_math.h"
#include "global.h"

enum lidarModel {
	hokuyo_urg
};



struct lidar {
	enum lidarModel model;
	void *lidarObject;

	struct coord pos;
	double orientation;
	struct fastmathTrigo fm;

	struct coord *points;
};



struct lidar initLidar(enum lidarModel model, char* device, struct coord position, double orientation, double angleMin, double angleMax);
struct lidar initLidarAndCalibrate(enum lidarModel model, char* device, struct coord position, double orientation, double angleMin, double angleMax);

//void restartLidar(struct lidar * l);
void closeLidar(struct lidar * l);

struct coord* getPoints(struct lidar* l);




#endif

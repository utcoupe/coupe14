#ifndef LIDAR_H
#define LIDAR_H

#include "fast_math.h"

enum lidarModel {
	hokuyo_urg
};

struct lidar {
	enum lidarModel model;
	void *lidarObject;

	struct coord pos;
	double orientation;
	struct fastmathTrigo fm;

	struct coord* points;
};



struct lidar initLidar(enum lidarModel model, char* device, struct coord position, double orientation, double angleMin, double angleMax);


struct coord* getPoints(struct lidar* l);




#endif
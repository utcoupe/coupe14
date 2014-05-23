#ifndef LIDAR_H
#define LIDAR_H

#include "fast_math.h"
#include "global.h"

struct lidar {
	void *lidarObject;

	struct coord pos;
	double orientation;
	struct fastmathTrigo fm;

	struct coord *points;
};

struct coordList_t {
	struct coord *points;
	int n;
};


struct lidar initLidar(char* device, struct coord position, double orientation, double angleMin, double angleMax);
struct lidar initLidarAndCalibrate(char* device, struct coord position, double orientation, double angleMin, double angleMax);

struct coord* getPoints(struct lidar* l);




#endif

#ifndef ROBOT_H
#define ROBOT_H

#include <math.h>
#include "fast_math.h"
#include "global.h"


struct robot {
	struct coord pt;
	int size;
};


int getRobots(struct coord *points, int n, struct robot *robots);
int mergeRobots(struct robot *r1, int n1, struct robot *r2, int n2, struct robot *result);
int isIn(int e, int *tab, int tab_size);









#endif


#ifndef ROBOT_H
#define ROBOT_H

#include <math.h>
#include "fast_math.h"
#include "global.h"




int getRobots(struct coord *points, int n, struct coord *robots);
int mergeRobots(struct coord *r1, int n1, struct coord *r2, int n2, struct coord *result);
int isIn(int e, int *tab, int tab_size);









#endif


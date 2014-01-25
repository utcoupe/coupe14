#ifndef ROBOT_H
#define ROBOT_H

#include <math.h>
#include "fast_math.h"
#include "global.h"

#define MAX_CLUSTERS 100 /*Ceux apres 100 seront abandonnés !*/
#define MAX_AB_POINTS 15 /*Nombre de points abberants consecutifs max*/

#define MAX_MIN_DIST 100	/*mm, distance max entre 2 points les plus proches dans un groupe*/


int getRobots(struct coord *points, int n, struct coord *robots);









#endif


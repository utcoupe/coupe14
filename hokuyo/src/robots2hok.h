#ifndef ROBOTS2HOK_H
#define ROBOTS2HOK_H

#include "lidar.h"

struct coordList_t mergePoints(struct lidar l1, struct lidar l2);
int cluterizeUnordered (struct coordList_t p, int *group, int *nbPtsGroup, int dmax);

#endif

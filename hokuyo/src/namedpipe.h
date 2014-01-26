#ifndef NAMEDPIPE_H
#define NAMEDPIPE_H
#include "fast_math.h"

#define PIPENAME "/tmp/lidarPipe"


void initNamedPipe();

void printRobots(struct coord *r, int nRobots);


#endif




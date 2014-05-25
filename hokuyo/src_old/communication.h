#ifndef COMMUNICATION_H
#define COMMUNICATION_H

#include "fast_math.h"
#include "robot.h"

void init_protocol();
void pushResults(struct robot *coords, int nbr, long timestamp);

#endif

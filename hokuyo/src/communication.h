#ifndef COMMUNICATION_H
#define COMMUNICATION_H

#include "fast_math.h"

void init_protocol();
void pushResults(struct coord *coords, int nbr, long timestamp);

#endif

#ifndef HOKUYOURG_H
#define HOKUYOURG_H


#define BAUDRATE_HOKUYOURG 115200
#define MAX_DATA 1024

#include <urg_ctrl.h>



void* initHokuyoUrg(char* device, double angleMin, double angleMax);
void resetHokuyoUrg(urg_t* urg, double angleMin, double angleMax);
int getnPointsHokuyoUrg(urg_t* urg);


#endif

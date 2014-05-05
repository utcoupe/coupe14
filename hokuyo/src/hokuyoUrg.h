#ifndef HOKUYOURG_H
#define HOKUYOURG_H


#define BAUDRATE_HOKUYOURG 115200

#include <urg_utils.h>



void* initHokuyoUrg(char* device, double angleMin, double angleMax);
void resetHokuyoUrg(void* urg, double angleMin, double angleMax);

//void restartHokuyoUrg(void* urg);
void closeHokuyoUrg(void* urg);


int getnPointsHokuyoUrg(void* urg);
double getAngleFromIndexHokuyoUrg(void* urg, int index);

void getDistancesHokuyoUrg(void* urg, long* buffer);



#endif

#ifndef HOKUYOURG_H
#define HOKUYOURG_H


#define BAUDRATE_HOKUYOURG 115200

#include <urg_utils.h>



urg_t* initHokuyoUrg(char* device, double angleMin, double angleMax);
void resetHokuyoUrg(urg_t* urg, double angleMin, double angleMax);

void restartHokuyoUrg(urg_t* urg);
void closeHokuyoUrg(urg_t* urg);


int getnPointsHokuyoUrg(urg_t* urg);
double getAngleFromIndexHokuyoUrg(urg_t* urg, int index);

void getDistancesHokuyoUrg(urg_t* urg, long* buffer);



#endif

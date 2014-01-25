#ifndef GUI_H
#define GUI_H

#include "global.h"
#include "fast_math.h"

struct color {
	int r, g, b;
};

struct color newColor(int r, int g, int b);

void initSDL();
void blitMap();
void blitLidar(struct coord positionLidar, struct color c);
void blitPoints(struct coord *points, int nPoints, struct color c);
void waitScreen();



//Display parameters, pretty useless
#define GUI_WINDOW_RESOLUTION_X 1050 
#define GUI_WINDOW_RESOLUTION_Y 700

#define BORDER_PADDING 50 /*mm*/
#define LIDAR_SIZE 50 /*mm*/
#define GUI_POINT_SIZE 3 /*px*/



#endif
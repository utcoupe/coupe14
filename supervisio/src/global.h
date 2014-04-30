// Visio UTCoupe 2014
// Par Quentin CHATEAU

#ifndef GLOBAL_H
#define GLOBAL_H

#ifndef TIMEBENCH
#define TIMEBENCH false
#endif

#define MIN_SIZE 500 //Attention, ici ce n'est pas la taille reelle mais la taille sur image originale
#define USE_MASK false

#define RESIZE false 
#define RESIZEW 320
#define RESIZEH 240

#define EPSILON_POLY 0.04
#define MAX_DIFF_TRI_EDGE 50

#define YEL_HUE_MIN 20
#define YEL_HUE_MAX 40
#define YEL_SAT_MIN 35
#define YEL_SAT_MAX 255
#define YEL_VAL_MIN 60
#define YEL_VAL_MAX 255

#define RED_HUE_MIN 170
#define RED_HUE_MAX 10
#define RED_SAT_MIN 80
#define RED_SAT_MAX 255
#define RED_VAL_MIN 60
#define RED_VAL_MAX 255

#define ENABLE_BLK 0
#define BLK_HUE_MIN 0
#define BLK_HUE_MAX 180
#define BLK_SAT_MIN 0
#define BLK_SAT_MAX 255
#define BLK_VAL_MIN 0
#define BLK_VAL_MAX 60

#endif

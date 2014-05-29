#ifndef HOKUYO_CONFIG_H
#define HOKUYO_CONFIG_H

#include "fast_math.h"
#include <urg_ctrl.h>

typedef struct Hokuyo {
	urg_t* urg;
	Pt_t pt;
	double orientation, cone; //Scanne dans ori-cone;ori+cone
	int imin, imax, nb_data;
	const char *path;
	double error;
	struct fastmathTrigo fm;
} Hok_t;

Hok_t initHokuyo(const char *path, double ori, double cone, Pt_t pt);
int calibrate(Hok_t *hok, float cone);
Hok_t applySymetry(Hok_t hok);

#endif

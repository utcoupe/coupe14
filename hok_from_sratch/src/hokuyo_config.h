#ifndef HOKUYO_CONFIG_H
#define HOKUYO_CONFIG_H

typedef struct Pt {
	int x, y;
} Pt_t;

typedef struct Hokuyo {
	urg_t* urg;
	Pt_t pt;
	double orientation, cone; //Scanne dans ori-cone;ori+cone
	int imin, imax;
	const char *path;
} Hok_t;

typedef struct Calib {
	double error;
} Calib_t;

Hok_t initHokuyo(const char *path, double ori, double cone, Pt_t pt);
Hok_t getCalibParams(Hok_t hok);
Calib_t calibrate(Hok_t hok);
Hok_t correctFromResults(Hok_t hok, Calib_t res);
Hok_t applySymetry(Hok_t hok);

#endif

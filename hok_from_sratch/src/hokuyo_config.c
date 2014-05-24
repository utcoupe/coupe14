#include "hokuyo_config.h"
#include <urg_ctrl.h>

Hok_t initHokuyo(const char *path, double ori, double cone, Pt_t pt) {
	int error;
	Hok_t hok;
	hok.urg = malloc(sizeof(urg_t));
	hok.path = path;
	hok.orientation = ori;
	hok.pt = pt;

	error = urg_connect(hok.urg, path, 115200);
	if (error < 0) {
		urg_disconnect(urg);
		fprintf(stderr, "%sConnection failed on %s\n",PREFIX, path);
		exit(EXIT_FAILURE);
	}
	printf("%sConnection to %s ok\n", PREFIX, path);

	hok.imin = urg_rad2index(hok.urg, hok.orientation - hok.cone);
	hok.imax = urg_rad2index(hok.urg, hok.orientation + hok.cone);
	urg_setCaptureTimes(hok.urg, UrgInfinityTimes);
    error = urg_requestData(urg, URG_MD, hok.imin, hok.imax);
	if (error < 0) {
		urg_disconnect(urg);
		fprintf(stderr, "%sRequesting data failed on %s\n",PREFIX, path);
		exit(EXIT_FAILURE);
	}
	printf("%sRequesting data from %s OK\n", PREFIX, path);

	return hok;	
}

Hok_t getCalibParams(Hok_t hok) {
	Hok_t calib_hok = hok;
	calib_hok.amin = calib_hok.orientation - CONE_CALIB;
	calib_hok.amax = calib_hok.orientation + CONE_CALIB;
	calib_hok.imin = urg_rad2index(hok.urg, hok.amin);
	calib_hok.imax = urg_rad2index(hok.urg, hok.amax);
	return calib_hok;
}

Calib_t calibrate(Hok_t hok) {
}

Hok_t correctFromResults(Hok_t hok, Calib_t res) {
	hok.orientation += error;
	hok.imin = urg_rad2index(hok.urg, hok.orientation - hok.cone);
	hok.imax = urg_rad2index(hok.urg, hok.orientation + hok.cone);
	return hok;
}

Hok_t applySymetry(Hok_t hok) {
	hok.pt = (Pt_t) {TABLE_X - hok.pt.x, TABLE_Y - hok.pt.y};
	hok.orientation = M_PI - orientation;
	hok.imin = urg_rad2index(hok.urg, hok.orientation - hok.cone);
	hok.imax = urg_rad2index(hok.urg, hok.orientation + hok.cone);
}

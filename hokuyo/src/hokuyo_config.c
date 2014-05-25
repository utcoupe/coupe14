#include "hokuyo_config.h"
#include "utils.h"
#include "fast_math.h"

#include <urg_ctrl.h>
#include <stdlib.h>
#include <stdio.h>


Hok_t initHokuyo(const char *path, double ori, double cone, Pt_t pt) {
	int error, i;
	Hok_t hok;
	hok.urg = malloc(sizeof(urg_t));
	hok.path = path;
	hok.orientation = ori;
	hok.pt = pt;
	hok.cone = cone;
	hok.error = 0;

	error = urg_connect(hok.urg, path, 115200);
	if (error < 0) {
		urg_disconnect(hok.urg);
		fprintf(stderr, "%sConnection failed on %s\n",PREFIX, path);
		exit(EXIT_FAILURE);
	}
	printf("%sConnection to %s ok\n", PREFIX, path);

	hok.imin = urg_rad2index(hok.urg, -hok.cone);
	hok.imax = urg_rad2index(hok.urg, hok.cone);
	urg_setCaptureTimes(hok.urg, UrgInfinityTimes);
    error = urg_requestData(hok.urg, URG_MD, hok.imin, hok.imax);
	if (error < 0) {
		urg_disconnect(hok.urg);
		fprintf(stderr, "%sRequesting data failed on %s\n",PREFIX, path);
		exit(EXIT_FAILURE);
	}
	printf("%sRequesting data on indexes %d to %d from %s OK\n", PREFIX, hok.imin, hok.imax, path);

	hok.nb_data = urg_dataMax(hok.urg);
	double *angles = malloc(hok.nb_data * sizeof(double));
	for (i=0; i<hok.nb_data; i++) {
		angles[i] = modTwoPi(urg_index2rad(hok.urg, i) + hok.orientation);
	}
	hok.fm = initFastmath(hok.nb_data, angles);
	free(angles);
	
	printf("%sCalculted sin/cos data for %s\n", PREFIX, path);

	return hok;	
}

int calibrate(Hok_t *hok) {
	hok->imin = urg_rad2index(hok->urg, -CONE_CALIB);
	hok->imax = urg_rad2index(hok->urg, CONE_CALIB);

	Pt_t points[MAX_DATA], detected;
	Cluster_t clusters[MAX_CLUSTERS];
	int i, count = 0;
	long sumx = 0, sumy = 0;

	for (i=0; i<CALIB_MEASURES; i++) {
		int n = getPoints(*hok, points);
		int nb_cluster = getClustersFromPts(points, n, clusters);

		if (nb_cluster == 1) {
			sumx += clusters[0].center.x;
			sumy += clusters[0].center.y;
			count++;
		} else {
			printf("%sCan't calibrate : got %d clusters on %s\n", PREFIX, nb_cluster, hok->path);
		}
	}
	
	if (count > CALIB_MEASURES/2) {
		detected = (Pt_t) { sumx/count, sumy/count };
		printf("%sDetected calib point on %d:%d for %s\n", PREFIX, detected.x, detected.y, hok->path);

		double a_theo, a_real;
		a_theo = angle(hok->pt, CALIB_PT);
		a_real = angle(hok->pt, detected);
		hok->error = modTwoPi(a_theo - a_real);
		printf("%sTH = %f, REAL = %f, E = %f on %s\n", PREFIX, a_theo, a_real, hok->error, hok->path);

		hok->orientation += hok->error;
		hok->imin = urg_rad2index(hok->urg, - hok->cone + hok->error);
		hok->imax = urg_rad2index(hok->urg, hok->cone + hok->error);

		hok->nb_data = urg_dataMax(hok->urg);
		double *angles = malloc(hok->nb_data * sizeof(double));
		for (i=0; i<hok->nb_data; i++) {
			angles[i] = modTwoPi(urg_index2rad(hok->urg, i) + hok->orientation);
		}
		hok->fm = initFastmath(hok->nb_data, angles);
		free(angles);

		return 0;
	} else {
		return -1;
	}
}

Hok_t applySymetry(Hok_t hok) {
	hok.pt = (Pt_t) {TABLE_X - hok.pt.x, TABLE_Y - hok.pt.y};
	hok.orientation = M_PI - hok.orientation;
	hok.imin = urg_rad2index(hok.urg, hok.orientation - hok.cone);
	hok.imax = urg_rad2index(hok.urg, hok.orientation + hok.cone);
}

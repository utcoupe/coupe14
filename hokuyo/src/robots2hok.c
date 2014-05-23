#include "robots2hok.h"
#include "lidar.h"

#include <stdlib.h>
#include <string.h>
#include <limits.h>

struct coordList_t mergePoints(struct lidar l1, struct lidar l2) {
	struct coordList_t p;
	p.points = malloc((l1.fm.n + l2.fm.n) * sizeof(struct coord));
	memcpy(p.points, l1.points, l1.fm.n*sizeof(struct coord));
	memcpy(p.points+l1.fm.n, l2.points, l2.fm.n*sizeof(struct coord));
	return p;
}

/* README
 *
 * Attention, cet algo n'est pas générique, il n'assure qu'un nuage de points
 * sera représenté par un seul cluster que si TOUT les points sont a moins de
 * MAX_MIN_DIST les uns des autres. */

int cluterizeUnordered (struct coordList_t p, int *group, int *nbPtsGroup, int dmax) {
	int i, j, nbGroup;
	struct dist_t {
		int dist, index;
	} d_min;

	//Init premier groupe (gagne un peu de temps dans la boucle)
	group[0] = 0;
	nbPtsGroup[0] = 1;
	nbGroup = 1;

	for (i=0; i<p.n; i++) { //Parcours de tout les points
		d_min.dist = INT_MAX;
		for(j=0; j<i; j++) { //Parcours de tout les points deja traités pour trouver le plus proche
			int d;
			if ((d = dist_squared(p.points[i], p.points[j])) < d_min.dist) {
				d_min.dist = d;
				d_min.index = j;
			}
		}
		if (d_min.dist < MAX_MIN_DIST*MAX_MIN_DIST) { //Le plus près est assez près pour etre dans le meme groupe
			group[i] = group[d_min.index];
			nbPtsGroup[group[i]]++;
		} else { //Nouveau groupe
			group[i] = nbGroup;
			nbPtsGroup[nbGroup]++;
			nbGroup++;
		}
	}
	return nbGroup;
}


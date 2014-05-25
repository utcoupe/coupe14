#include "utils.h"
#include "fast_math.h"
#include <urg_ctrl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define max(a, b) a>b?a:b
#define min(a, b) a<b?a:b


int getPoints(Hok_t hok, Pt_t* pt_list) {
	long data[MAX_DATA];
	int n = urg_receiveData(hok.urg, data, MAX_DATA);
	int i, j=0;
	for (i=hok.imin; i<hok.imax; i++) {
		Pt_t pt = (Pt_t) { hok.pt.x + data[i]*fastCos(hok.fm, i), hok.pt.y + data[i]*fastSin(hok.fm, i) };
		if (pt.x > TABLE_X - BORDER_MARGIN || pt.x < BORDER_MARGIN || pt.y > TABLE_Y - BORDER_MARGIN || pt.y < BORDER_MARGIN) {
			pt_list[j++] = (Pt_t) { -1, -1 };
		} else {
			pt_list[j++] = pt;
		}
	}
	return hok.imax-hok.imin;
}

int getClustersFromPts(Pt_t *pt_list, int nb_pts, Cluster_t* clusters) {
	int i, j, nbCluster = 0;
	if (nb_pts > 0) {
		int *clusters_index = malloc(nb_pts*sizeof(int));
		clusters_index[0] = 0;
		for (i=0; i<nb_pts; i++) {
			if (pt_list[i].x == -1 && pt_list[i].y == -1) {
				clusters_index[i] = -1;
				continue;
			}

			int j = max(0, i - CLUSTER_POINTS_BACKWARDS);
			for (j; j<i; j++) {
				if (dist_squared(pt_list[j], pt_list[i]) < MAX_DIST*MAX_DIST) {
					clusters_index[i] = clusters_index[j];
					break;
				}
			}
			if (j == i) {
				clusters_index[i] = nbCluster;
				nbCluster++;

				if (nbCluster > MAX_CLUSTERS) {
					printf("%sToo many clusters\n", PREFIX);
				}
			}
		}

		for (i=0; i<nbCluster; i++) {
			clusters[i].nb = 0;
		}
		for (i=0; i<nb_pts; i++) {
			int index = clusters_index[i];
			if (index >= 0) {
				clusters[index].pts[clusters[index].nb++] = pt_list[i];
			}
		}

		i = 0;
		while (i < nbCluster) {
			if (clusters[i].nb < NB_PTS_MIN) {
				for (j=i+1; j<nbCluster; j++) {
					clusters[j-1] = clusters[j];
				}
				nbCluster--;
			} else {
				i++;
			}
		}


		for (i=0; i<nbCluster; i++) {
			clusters[i].size = sqrt(dist_squared(clusters[i].pts[0], clusters[i].pts[clusters[i].nb-1]));
			long sumx = 0, sumy = 0;
			int j = 0;
			for (j=0; j<clusters[i].nb; j++) {
				sumx += clusters[i].pts[j].x;
				sumy += clusters[i].pts[j].y;
			}
			if (clusters[i].nb > 0) {
				clusters[i].center = (Pt_t) { sumx/clusters[i].nb, sumy/clusters[i].nb };
			}
		}
	}
	return nbCluster;
}

int sortAndSelectRobots(int n, Cluster_t *robots){
	int i, nbr_robots = min(n, MAX_ROBOTS);
	Cluster_t *r = malloc(n*sizeof(Cluster_t));
	memcpy(r, robots, n*sizeof(Cluster_t));
	for(i=0; i<nbr_robots; i++){
		int maxSize = 0, maxId = 0;
		for(int j=0; j<n; j++){
			if(r[j].size > maxSize){
				maxSize = r[j].size;
				maxId = j;
			}
		}
		robots[i].center = r[maxId].center;
		robots[i].size = r[maxId].size;
		r[maxId].size = 0;
	}
	return i;
}

int mergeRobots(Cluster_t *r1, int n1, Cluster_t *r2, int n2, Cluster_t *result) {
	struct corres { //permet d'établir des correspondances entre les index
		int r1;
		int r2;
	};
	//Brute force ici, on aura max 4 robots de chaque hokuyo, 4x4 = 16 cas, ca reste peu
	//Calcul de la distance entre chaque combinaison de coords
	int distR1R2[MAX_ROBOTS][MAX_ROBOTS], i, j;
	struct corres dist_indexes[MAX_ROBOTS*MAX_ROBOTS]; //Tableau d'index de distR1R2, sert a trier les distances
	struct corres merged[MAX_ROBOTS]; //Correspondances finales et retenues
	int changed = 0;

	//Calcul des distaces
	for (i=0; i<n1; i++) {
		for (j=0; j<n2; j++) {
			distR1R2[i][j] = dist_squared(r1[i].center, r2[j].center);
		}
	}

	for (i=0; i<n1*n2; i++) {
		dist_indexes[i] = (struct corres){ i/n2, i%n2 };
	}

	do {
		changed = 0;
		for (i=1; i<n1*n2; i++) {
			if (distR1R2[dist_indexes[i-1].r1][dist_indexes[i-1].r2] > distR1R2[dist_indexes[i].r1][dist_indexes[i].r2]) {
				struct corres temp = dist_indexes[i];
				dist_indexes[i] = dist_indexes[i-1];
				dist_indexes[i-1] = temp;
				changed = 1;
			}
		}
	} while (changed);

	printf("Distances \n");
	for (i=0; i<n1*n2; i++) {
		int ind1 = dist_indexes[i].r1;
		int ind2 = dist_indexes[i].r2;
		printf("%d ", distR1R2[ind1][ind2]);
	}
	printf("\n");


	//Choix des correspondances en prenant la premiere qui vientdu plus petit au plus grand
	int used_R1_index[MAX_ROBOTS], used_R2_index[MAX_ROBOTS], nbr_found = 0;
	for (i=0; i<MAX_ROBOTS; i++) {
		used_R1_index[i] = -1;
		used_R2_index[i] = -1;
	}
	for (i=0; i<n1*n2; i++) {
		struct corres c = dist_indexes[i];

		if (distR1R2[c.r1][c.r2] > MAX_SIZE_TO_MERGE*MAX_SIZE_TO_MERGE) {
			break;
		}

		if (!isIn(c.r1, used_R1_index, n1) && //Aucun des deux robots n'est deja selectionné
			!isIn(c.r2, used_R2_index, n2)) { //On ajout la correspondace

			merged[nbr_found] = c;
			used_R1_index[nbr_found] = c.r1;
			used_R2_index[nbr_found] = c.r2;
			nbr_found++;
		}
	}
	printf("used: \n");
	for (i=0; i<nbr_found; i++) {
		printf("r1:%d r2:%d\n", used_R1_index[i], used_R2_index[i]);
	}

	for (i=0; i<nbr_found; i++) {
		struct corres c = merged[i];
		Cluster_t clu;
		clu.nb = 0;
		clu.center = (Pt_t) {(r1[c.r1].center.x + r2[c.r2].center.x) / 2, (r1[c.r1].center.y + r2[c.r2].center.y) / 2 };
		clu.size = (r1[c.r1].size + r2[c.r2].size) / 2;
		result[i] = clu;
	}
	printf("Found %d pairs\n", nbr_found);

	int nbr_left = n1 + n2 - 2*nbr_found, clust_counter = 0;
	Cluster_t clust_left[MAX_ROBOTS*MAX_ROBOTS];
	for (i=0; i<n1; i++) {
		if (!isIn(i, used_R1_index, nbr_found)) {
			clust_left[clust_counter++] = r1[i];
		}
	}
	clust_counter = 0;
	for (i=0; i<n2; i++) {
		if (!isIn(i, used_R2_index, nbr_found)) {
			clust_left[clust_counter++] = r2[i];
		}
	}

	for (i=n1*n2-1; i>=0; i--) {
		struct corres c = dist_indexes[i];

		if (!isIn(c.r1, used_R1_index, nbr_found)) { 
			result[nbr_found] = r1[c.r1];
			used_R1_index[nbr_found] = c.r1;
			nbr_found++;
		}
		
		if (!isIn(c.r2, used_R2_index, nbr_found)) {
			result[nbr_found] = r2[c.r2];
			used_R2_index[nbr_found] = c.r2;
			nbr_found++;
		}
	}
	printf("used: \n");
	for (i=0; i<nbr_found; i++) {
		printf("r1:%d r2:%d\n", used_R1_index[i], used_R2_index[i]);
	}
	printf("Found %d in the end\n", nbr_found);

	nbr_found = sortAndSelectRobots(nbr_found, result);
	return nbr_found;
}

int isIn(int e, int *tab, int tab_size) {
	int i, ret = 0;
	for (i=0; i<tab_size; i++) {
		if (tab[i] == e) {
			ret = 1; //Found
			break;
		}
	}
	return ret;
}

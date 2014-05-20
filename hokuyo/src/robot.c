#include "robot.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int
clusterize(struct coord *points, int n, int *group, int *groupNbPoints){
	for(int i=0; i<n; i++){
		group[i] = -1; 
	}
	int nbGroup = 0;
	for(int i=MAX_AB_POINTS; i<n; i++) {
		//#ifndef DEBUG_DO_NOT_REMOVE_POINTS
		if( points[i].x == 0 && points[i].y == 0) continue;
		//#endif

		int dmin = 35000, jmin = 0;
		unsigned long d[MAX_AB_POINTS];
		for(int j=1; j<=MAX_AB_POINTS; j++){
			#ifndef DEBUG_DO_NOT_REMOVE_POINTS
			if( points[i-j].x == 0 && points[i-j].y == 0) continue;
			#endif
			d[j-1] = pow(points[i].x-points[i-j].x, 2) + pow(points[i].y-points[i-j].y, 2);
			if(d[j-1] < dmin){
				dmin = d[j-1];
				jmin = j;
			}
		}
		//printf("i:%i\n", i);
		if(dmin < MAX_MIN_DIST*MAX_MIN_DIST){
			//printf("i-jmin:%i\n", i-jmin);
			if(group[i-jmin] == -1){
				//printf("group[%i]==%i, nbGroup==%i\n", i-jmin, group[i-jmin], nbGroup);
				if(nbGroup+1 >= MAX_CLUSTERS) return MAX_CLUSTERS;				
				groupNbPoints[nbGroup] = 0;
				group[i-jmin] = nbGroup;
				nbGroup++;
			}
			group[i] = group[i-jmin];
			groupNbPoints[group[i-jmin]]++;
			//printf("group= %i <- point[ %i ]; group_size= %i\n", group[i-jmin], i, groupNbPoints[group[i-jmin]]);
		}
	}
	return nbGroup;
}

void
bestClusters(int nbClusters, int *clustersNbPoints, int *bestClusters){
	//printf("bestClusters(%i,,)", nbClusters);
	for(int i=0; i<MAX_ROBOTS; i++){
		int currentMax = 1, currentMaxId = 0;
		for(int j=0; j<nbClusters; j++){
			if(clustersNbPoints[j] > currentMax){
				currentMax = clustersNbPoints[j];
				currentMaxId = j;
			}
		}
		//printf("BestGroup %i %i\n", currentMaxId, clustersNbPoints[currentMaxId]);
		clustersNbPoints[currentMaxId] = 0;
		bestClusters[i] = currentMaxId;
	}
}

struct coord
robotCenter(int * sizeSquarred, struct coord *points, int n, int *clusters, int clusterId){
	int first = -1, second = -1, blast = 0, last = 0;
	for(int i=0; i<n; i++){
		if(clusters[i] != clusterId) continue;
		
		if(first < 0) first = i;
		else if(second < 0) second = i;

		blast = last;
		last = i;
	}
	/*printf("group %i\tfirst %i :\tx:%i\ty:%i\n", clusterId, first, points[first].x, points[first].y);
	printf("group %i\tlast  %i :\tx:%i\ty:%i\n", clusterId, last, points[last].x, points[last].y);*/
	struct coord pos;
	pos.x = ( points[first].x + points[second].x + points[blast].x + points[last].x ) / 4;
	pos.y = ( points[first].y + points[second].y + points[blast].y + points[last].y ) / 4;
	*sizeSquarred = pow(points[last].x-points[first].x, 2) + pow(points[last].y-points[first].y, 2); 
	return pos;
}

void
sortRobots(int n, int * sizes, struct coord * positions, struct coord *robots){
	//tri très optimisé ^^
	for(int i=0; i<n; i++){
		int maxSize = 0, maxId = 0;
		for(int j=0; j<n; j++){
			if(sizes[j] > maxSize){
				maxSize = sizes[j];
				maxId = j;
			}
		}
		sizes[maxId] = 0;
		robots[i] = positions[maxId];
		//printf("%sbiggest cluster:(%i, %i) size=%i\n", PREFIX, robots[i].x, robots[i].y, maxSize);
	}
}

int
getRobots(struct coord *points, int n, struct coord *robots){
	int clustersNbPoints[MAX_CLUSTERS];
	int *clusters = malloc(sizeof(int)*n);
	if(clusters == NULL) exit(EXIT_FAILURE);

	//printf("%s---------\n", PREFIX);


	int nbClusters = clusterize(points, n, clusters, clustersNbPoints);
	
	int bestClustersId[MAX_ROBOTS];
	if(nbClusters > MAX_ROBOTS){
		bestClusters(nbClusters, clustersNbPoints, bestClustersId);
		nbClusters = MAX_ROBOTS;
	}
	else{
		for(int i=0; i<nbClusters; i++){
			bestClustersId[i] = i;
			//printf("clusters[%i], nbPoints:%i\n", i, clustersNbPoints[bestClustersId[i]]);
		}
	}

	//calcul du centre du robot et de sa taille
	int size[MAX_ROBOTS];
	struct coord positions[MAX_ROBOTS];

	for(int i=0; i<nbClusters; i++){
		positions[i] = robotCenter(&(size[i]), points, n, clusters, bestClustersId[i]);
		//printf("%sCluster[%i] (%i,%i) size:%i\n", PREFIX, i, positions[i].x, positions[i].y, size[i]);
	}
	//printf("%sSort... nbClusters=%i\n", PREFIX, nbClusters);
	sortRobots(nbClusters, size, positions, robots);


	free(clusters);
	clusters = 0;
	return nbClusters;
}


int mergeRobots(struct coord *r1, int n1, struct coord *r2, int n2, struct coord *result) {
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
			distR1R2[i][j] = dist_squared(r1[i], r2[j]);
		}
	}

	//Tri du tableau de correspondance des distances par ordre croissant
	//TODO verifier le fonctionnement
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

	//Choix des correspondances en prenant la premiere qui vientdu plus petit au plus grand
	int used_R1_index[MAX_ROBOTS], used_R2_index[MAX_ROBOTS], nbr_found = 0;
	for (i=1; i<n1*n2; i++) {
		struct corres c = dist_indexes[i];
		if (!isIn(c.r1, used_R1_index, MAX_ROBOTS) && //Aucun des deux robots n'est deja selectionné
			!isIn(c.r2, used_R2_index, MAX_ROBOTS)) { //On ajout la correspondace

			merged[nbr_found] = c;
			used_R1_index[nbr_found] = c.r1;
			used_R2_index[nbr_found] = c.r2;
			nbr_found++;
		}
	}

	for (i=0; i<nbr_found; i++) {
		struct corres c = merged[i];
		result[i] = (struct coord) {(r1[c.r1].x + r2[c.r2].x) / 2, (r1[c.r1].y + r2[c.r2].y) / 2 };
	}

	int diff = n1 - n2; //Si on a des robots detectés par un hokuyo mais pas par l'autre
	if (diff > 0) { //Plus de r1 que de r2
		for (i=n2; i<n1; i++) {
			result[nbr_found++] = r1[i];
		}
	} else if (diff < 0) { //Plus de r2 que de r1
		for (i=n1; i<n2; i++) {
			result[nbr_found++] = r2[i];
		}
	}
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

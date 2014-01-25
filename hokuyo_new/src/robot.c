#include "robot.h"
#include <stdio.h>
#include <stdlib.h>

int
clusterize(struct coord *points, int n, int *group, int *groupNbPoints){
	/*#ifndef DEBUG_DO_NOT_REMOVE_POINTS
	if( points[i].x == 0 && points[i].y == 0) continue;
	#endif*/
	int nbGroup = 0;
	for(int i=MAX_AB_POINTS; i<n; i++) {
		int dmin = 35000, jmin = 0;
		unsigned long d[MAX_AB_POINTS];
		for(int j=1; j<=MAX_AB_POINTS; j++){
			d[j-1] = pow(points[i].x-points[i-j].x, 2) + pow(points[i].y-points[i-j].y, 2);
			if(d[j-1] < dmin){
				dmin = d[j-1];
				jmin = j;
			}
		}
		//printf("i:%i\n", i);
		if(dmin < MAX_MIN_DIST*MAX_MIN_DIST){
			//printf("i-jmin:%i\n", i-jmin);
			if(group[i-jmin] == 0){
				nbGroup++;
				if(nbGroup >= MAX_CLUSTERS) return MAX_CLUSTERS;
				groupNbPoints[i-jmin] = 0;
				group[i-jmin] = nbGroup;
			}
			group[i] = group[i-jmin];
			groupNbPoints[i-jmin]++;
			//printf("done\n");
		}
	}
	return nbGroup;
}

void
bestClusters(int nbClusters, int *clustersNbPoints, int *bestClusters){
	for(int i=0; i<MAX_ROBOTS; i++){
		int currentMax = 1, currentMaxId = 0;
		for(int j=0; j<nbClusters; j++){
			if(clustersNbPoints[j] > currentMax){
				currentMax = clustersNbPoints[j];
				currentMaxId = j;
			}
		}
		clustersNbPoints[currentMaxId] = 0;
		bestClusters[i] = currentMaxId;
	}
}

struct coord robotCenter(struct coord *points, int n, int *clusters, int clusterId){
	int first = -1, last = 0;
	for(int i=0; i<n; i++){
		if(clusters[i] != clusterId) continue;
		if(first < 0) first = i;
		last = i;
	}
	struct coord pos;
	pos.x = ( points[first].x + points[last].x ) / 2;
	pos.y = ( points[first].y + points[last].y ) / 2;
	return pos;
}

int
getRobots(struct coord *points, int n, struct coord *robots){
	int clustersNbPoints[MAX_CLUSTERS];
	int *clusters = malloc(sizeof(int)*n);
	if(clusters == NULL) exit(EXIT_FAILURE);

	int nbClusters = clusterize(points, n, clusters, clustersNbPoints);
	/*
	int bestClustersId[MAX_ROBOTS];
	if(nbClusters > MAX_ROBOTS){
		bestClusters(nbClusters, clustersNbPoints, bestClustersId);
		nbClusters = MAX_ROBOTS;
	}
	else{
		for(int i=0; i<nbClusters; i++) bestClustersId[i] = i+1;
	}

	//calcul du centre du robot
	for(int i=0; i<nbClusters; i++){
		robots[i] = robotCenter(points, nbClusters, clusters, bestClustersId[i]);
	}	*/


	free(clusters);
	return 0;//nbClusters;
}









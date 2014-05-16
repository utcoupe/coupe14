#include "robot.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>


int
clusterize(struct coord *points, int n, int *group, int *groupNbPoints){
	int nbGroup = 0;
	for(int i=1; i<n; i++) {
		group[i] = -1;
		//#ifndef DEBUG_DO_NOT_REMOVE_POINTS
		if( points[i].x == 0 && points[i].y == 0) continue;
		//#endif

		int dmin = 35000, jmin = 0;
		unsigned long d[MAX_AB_POINTS];
		for(int j=0; j<i; j++){
			#ifndef DEBUG_DO_NOT_REMOVE_POINTS
			if( points[j].x == 0 && points[j].y == 0) continue;
			#endif
			unsigned long d = pow(points[i].x-points[j].x, 2) + pow(points[i].y-points[j].y, 2);
			if(d < dmin){
				dmin = d;
				jmin = j;
			}
		}
		//printf("i:%i\n", i);
		if(dmin < MAX_MIN_DIST*MAX_MIN_DIST){
			//printf("i-jmin:%i\n", i-jmin);
			if(group[jmin] == -1){
				//printf("group[%i]==%i, nbGroup==%i\n", i-jmin, group[i-jmin], nbGroup);
				if(nbGroup+1 >= MAX_CLUSTERS) return MAX_CLUSTERS;				
				groupNbPoints[nbGroup] = 0;
				group[jmin] = nbGroup;
				nbGroup++;
			}
			group[i] = group[jmin];
			groupNbPoints[group[i]]++;
			//printf("group= %i <- point[ %i ]; group_size= %i\n", group[i], i, groupNbPoints[group[i]]);
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
		clustersNbPoints[currentMaxId] = -clustersNbPoints[currentMaxId];
		bestClusters[i] = currentMaxId;
	}
	for(int i=0; i<MAX_ROBOTS; i++){
		clustersNbPoints[bestClusters[i]] = -clustersNbPoints[bestClusters[i]]; //needed, used by robotCenter
	}
}

struct coord
robotCenter(int * sizeSquarred, struct coord *points, int n, int *clusters, int clusterId, int *clustersNbPoints){
	struct coord center;
	center.x = 0;
	center.y = 0;
	for(int i=0; i<n; i++){		
		//printf("robot.c clusters[%i]=%i, clusterId=%i\n", i, clusters[i], clusterId);
		if(clusters[i] != clusterId) continue;
		center.x += points[i].x;
		center.y += points[i].y;
	}
	//printf("robotCenter clustersNbPoints[%i]=%i\n", clusterId, clustersNbPoints[clusterId]);
	center.x /= clustersNbPoints[clusterId];
	center.y /= clustersNbPoints[clusterId];
	unsigned long averageD = 0;
	for(int i=0; i<n; i++){
		if(clusters[i] != clusterId) continue;
		averageD += dist_squared(center, points[i]);
	}
	averageD /= clustersNbPoints[clusterId];
	*sizeSquarred = averageD;
	if(averageD > INT_MAX) printf("ERROR: OVERFLOW\n");
	
	return center;
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
	//printf("robot.c malloc:%i\t%i\n", n, sizeof(int)*n);
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
		positions[i] = robotCenter(&(size[i]), points, n, clusters, bestClustersId[i], clustersNbPoints);
		//printf("%sCluster[%i] (%i,%i) size:%i\n", PREFIX, i, positions[i].x, positions[i].y, size[i]);
	}
	//printf("%sSort... nbClusters=%i\n", PREFIX, nbClusters);
	sortRobots(nbClusters, size, positions, robots);


	free(clusters);
	return nbClusters;
}









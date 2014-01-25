#include "robot.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int
clusterize(struct coord *points, int n, int *group, int *groupNbPoints){
	/*#ifndef DEBUG_DO_NOT_REMOVE_POINTS
	if( points[i].x == 0 && points[i].y == 0) continue;
	#endif*/
	for(int i=0; i<n; i++){
		group[i] = -1; 
	}
	int nbGroup = 0;
	for(int i=MAX_AB_POINTS; i<n; i++) {
		#ifndef DEBUG_DO_NOT_REMOVE_POINTS
		if( points[i].x == 0 && points[i].y == 0) continue;
		#endif

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
			printf("group= %i <- point[ %i ]; group_size= %i\n", group[i-jmin], i, groupNbPoints[group[i-jmin]]);
		}
	}
	return nbGroup;
}

void
bestClusters(int nbClusters, int *clustersNbPoints, int *bestClusters){
	printf("bestClusters(%i,,)", nbClusters);
	for(int i=0; i<MAX_ROBOTS; i++){
		int currentMax = 1, currentMaxId = 0;
		for(int j=0; j<nbClusters; j++){
			if(clustersNbPoints[j] > currentMax){
				currentMax = clustersNbPoints[j];
				currentMaxId = j;
			}
		}
		printf("BestGroup %i %i\n", currentMaxId, clustersNbPoints[currentMaxId]);
		clustersNbPoints[currentMaxId] = 0;
		bestClusters[i] = currentMaxId;
	}
}

struct coord robotCenter(struct coord *points, int n, int *clusters, int clusterId){
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
	return pos;
}

int
getRobots(struct coord *points, int n, struct coord *robots){
	int clustersNbPoints[MAX_CLUSTERS];
	int *clusters = malloc(sizeof(int)*n);
	if(clusters == NULL) exit(EXIT_FAILURE);


	int nbClusters = clusterize(points, n, clusters, clustersNbPoints);
	
	int bestClustersId[MAX_ROBOTS];
	if(nbClusters > MAX_ROBOTS){
		bestClusters(nbClusters, clustersNbPoints, bestClustersId);
		nbClusters = MAX_ROBOTS;
	}
	else{
		for(int i=0; i<nbClusters; i++){
			bestClustersId[i] = i;
			printf("clusters[%i], nbPoints:%i\n", i, clustersNbPoints[bestClustersId[i]]);
		}
	}

	//calcul du centre du robot
	for(int i=0; i<nbClusters; i++){
		robots[i] = robotCenter(points, n, clusters, bestClustersId[i]);
	}	


	free(clusters);
	return nbClusters;
}









#ifndef GLOBAL_H
#define GLOBAL_H

#define SDL

#define PREFIX "[C-HK]  "

#define TAILLE_TABLE_X 3000
#define TAILLE_TABLE_Y 2000
#define PI 3.14159265358979323846264338327950288

#define MARKER_R_POS_X (TAILLE_TABLE_X/2)
#define MARKER_R_POS_Y (TAILLE_TABLE_Y/2)
#define MARKER_DETECTION_ANGLE 30*PI/180
#define MARKER_DETECTION_ZONE_SIZE 500/*mm*/
#define MARKER_DETECTION_STEPS 20

#define MAX_CLUSTERS 100 /*Ceux apres 100 seront abandonnés !*/
#define MAX_AB_POINTS 15 /*Nombre de points abberants consecutifs max*/

#define MAX_MIN_DIST 100	/*mm, distance max entre 2 points les plus proches dans un groupe*/

#define MERGE_POINTS_BEFORE_CLUSTERIZING true

/*
#define HOK1_X 3025
#define HOK1_Y -25
#define HOK1_A (3*PI/4)
#define HOK1_AMIN (PI/2)
#define HOK1_AMAX PI

#define HOK2_X 25
#define HOK2_Y 1000
#define HOK2_A 0
#define HOK2_AMIN (-PI/2)
#define HOK2_AMAX (PI/2)
*/

#define HOK1_X -25
#define HOK1_Y -25
#define HOK1_A (PI/4)
#define HOK1_AMIN 0
#define HOK1_AMAX (PI/2)

#define HOK2_X 3025
#define HOK2_Y 1000
#define HOK2_A PI
#define HOK2_AMIN (PI/2)
#define HOK2_AMAX (-PI/2)

//#define DEBUG_DO_NOT_REMOVE_POINTS
#define MAX_DISTANCE sqrt(TAILLE_TABLE_X*TAILLE_TABLE_X + TAILLE_TABLE_Y*TAILLE_TABLE_Y)
#define DISTANCE_TO_EDGE_MIN 80 /*mm*/

#define MAX_ROBOTS 4

#endif

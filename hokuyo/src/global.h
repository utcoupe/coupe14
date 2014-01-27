#ifndef GLOBAL_H
#define GLOBAL_H


#define TAILLE_TABLE_X 3000
#define TAILLE_TABLE_Y 2000
#define PI 3.14159265358979323846264338327950288

#define MARKER_R_POS_X (TAILLE_TABLE_X/2)
#define MARKER_R_POS_Y (TAILLE_TABLE_Y/2)
#define MARKER_DETECTION_ANGLE PI/8
#define MARKER_DETECTION_ZONE_SIZE 500/*mm*/
#define MARKER_DETECTION_STEPS 20


#define MAX_CLUSTERS 100 /*Ceux apres 100 seront abandonnés !*/
#define MAX_AB_POINTS 15 /*Nombre de points abberants consecutifs max*/

#define MAX_MIN_DIST 100	/*mm, distance max entre 2 points les plus proches dans un groupe*/


//#define DEBUG_DO_NOT_REMOVE_POINTS
#define MAX_DISTANCE sqrt(TAILLE_TABLE_X*TAILLE_TABLE_X + TAILLE_TABLE_Y*TAILLE_TABLE_Y)
#define DISTANCE_TO_EDGE_MIN 80 /*mm*/

#define MAX_ROBOTS 4







#endif
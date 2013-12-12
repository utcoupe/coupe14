/*******************************
* Quentin CHATEAU pour UTCOUPE *
* quentin.chateau@gmail.com    *
* Last edition : 17/11/2013    *
*******************************/
#include <stdlib.h>
#include <stdio.h>
#include <urg_sensor.h>
#include <urg_utils.h>
#include <urg_serial_utils.h>
#include <math.h>

#include "analyzer.h"
#include "fast_math.h"
#include "global.h"
#include "exceptions.h"

int init(urg_t *urg){
	char *device = "/dev/ttyACM0";
	int error;
	int i;

	//SERIAL PORT DETECTION
	printf("List of serial ports :\n");
	int found_port_size = urg_serial_find_port();
	if (found_port_size == 0) {
		printf("could not found serial ports.\n");
		exit(EXIT_FAILURE);
	}
	for (i = 0; i < found_port_size; ++i) {
		printf("%s", (char *)urg_serial_port_name(i));
		if (urg_serial_is_urg_port(i)) {
			device = (char *)urg_serial_port_name(i);
			printf(" [URG]");
		}
		printf("\n");
	}
	printf("\n");

	printf("Connection à %s\n", device);
	error = urg_open(urg, URG_SERIAL, device, BAUDRATE);
	if(error < 0){
		error_func(urg, "connection failed");
	}
	else{
		printf("Connection établie à %s\n", device);
		urg_set_scanning_parameter(urg, urg_rad2step(urg, ANGLE_MIN), urg_rad2step(urg, ANGLE_MAX), 0);//scan en continu, on ne garde que les point entre -PI/2 et PI/2
		printf("Parameters set\n");
		error = urg_start_measurement(urg, URG_DISTANCE, URG_SCAN_INFINITY, 0);
		if(error < 0){
			error_func(urg, "failed to start measurement");
		}
	}
	get_val(calc, 0, urg);//calcule les tables de cos/sin à l'avance
	return error;
}

int get_points_2d(struct urg_params urg, struct coord *points){
	int data_max, n, i;
	long *data;

	data_max = urg_max_data_size(urg.ptr);//aquisition du nombre de points
	data = (long*)malloc(sizeof(long) * data_max);
	if(data == NULL){
		fprintf(stderr, "data malloc error\n");
		exit(1);
	}
	if(points == NULL){
		fprintf(stderr, "get_points_2d : points non alloué\n");
		exit(1);
	}

	n = urg_get_distance(urg.ptr, data, NULL);

	// CONVERSION EN COORDONNEES
	for(i=0; i<n; i++){
		/*
		double rad = urg_index2rad(urg.ptr, i);
		points[i].x = data[i]*cos(rad) - urg.x; //x
		points[i].y = data[i]*sin(rad) - urg.y; //y
		*/
		points[i].x = data[i]*get_val(cosinus, i, urg.ptr) - urg.x; //x
		points[i].y = data[i]*get_val(sinus, i, urg.ptr) - urg.y; //y

		if(urg.side == BLUE_SIDE){//si blue side, symétrie centrale
			points[i].x = LX - points[i].x;
			points[i].y = LY - points[i].y;
		}
	}
	free(data);//free raw datas

	return n;
}

int get_robots_2d(struct coord *robot_pos, struct coord *points, int n){
	//***************
	// DECLARATIONS *
	//***************
	int groups_counter = 0, group_index;//groups_counter initialisé à 0 si il n'y a pas de groupes
	int valid_groups_counter = 0;//pas de groupes valides initialement
	int i, j;
	struct points_group points_group[MAX_GROUPS];
	struct coord *groups_pos = NULL;
	group_index = groups_counter-1;

	//********************************
	// CREATION DE GROUPES DE POINTS *
	//********************************

	for(i=0; i<n; i++){//analyse des points
		if(!ignore(points[i])){//si le point n'est pas à ignorer
			while(group_index>=0 && dist(points[i], points_group[group_index].last) > DIST_DIFF_GROUP) group_index--; //On parcourt les groupes
			if(group_index >= 0){ //Si le point apartient à un groupe
				points_group[group_index].last = points[i];//on remplace le deuxième point par le dernier point détecté
				points_group[group_index].size++; //il y un point de plus dans le groupe
				group_index = groups_counter-1;
			}
			else{ //Sinon on cree un nouveau groupe
				groups_counter++; //un groupe de plus
				group_index = groups_counter-1;
				points_group[group_index].first = points_group[group_index].last = points[i]; //on stocke le point dans un nouveau groupe de points
				points_group[group_index].size = 1;//1 point dans ce groupe
				points_group[group_index].valid = 0; //invalide par défaut
			}
		}
	}

	//*************************
	// CALCUL DES COORDONNEES *
	//*************************

	for(i=0; i<groups_counter; i++){
		points_group[i].coord.x = (points_group[i].first.x + points_group[i].last.x)/2;//X du robot
		points_group[i].coord.y = (points_group[i].first.y + points_group[i].last.y)/2;//Y du robot
	}
		
	//*************************
	// TRAITEMENT DES GROUPES *
	//*************************
	for(i=0; i<groups_counter;i++){
		if(!group_exception(points_group[i])){
			points_group[i].valid = 1;//si le point passe toutes les exceptions, il est valide
			valid_groups_counter++;//un groupe valide de plus
		}
	}

	//*************************
	// COPIE DES GROUPES TEMP *
	//*************************

	groups_pos = (struct coord*)malloc(sizeof(struct coord) * valid_groups_counter); //il y aura une coordonnée par groupe valide
	if(groups_pos == NULL){
		fprintf(stderr, "groups_pos : malloc error");
		exit(1);
	}

	j = 0;
	for(i=0; i<groups_counter; i++){
		if(points_group[i].valid == 1){//si le groupe est valide, on calcule ses coordonées
			groups_pos[j] = points_group[i].coord;
			j++;
		}
	}
		
	//***************************************
	// SUPPRESSION DES GROUPES EN TROP 	*
	// On supprime les groupes les plus 	*
	// près du bord 			*
	// Ne devrait jamais arriver 		*
	//***************************************
	
	while(valid_groups_counter > DETECTABLE_ROBOTS) //si on a plus de groupe de point que de robots
	{
		int dist_min = LX, index_to_delete = 0;
		for(i=0; i<valid_groups_counter; i++){//on repère quel group est le plus proche du bord
			int dist = dist_to_edge(groups_pos[i]);
			if(dist_min > dist){
				dist_min = dist;
				index_to_delete = i;
			}
		}
		for(i=index_to_delete; i<valid_groups_counter ; i++){//on le supprime
			groups_pos[i] = groups_pos[i+1];
		}
		valid_groups_counter--;//on enlève un groupe
	}

	//*****************************
	// Copie des groupes finaux   *
	//*****************************
	for(i=0; i<valid_groups_counter; i++){
		robot_pos[i] = groups_pos[i];
	}

	return valid_groups_counter;
}

void error_func(urg_t *urg, const char *message){
	urg_close(urg);
	fprintf(stderr, "%s :: %s\n", message, urg_error(urg)); //print le message d'erreur perso et celui issu de l'hokuyo
}

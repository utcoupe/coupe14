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

int init(urg_t *urg, int n_hokuyo){
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
                if(n_hokuyo == 0)
        		urg_set_scanning_parameter(urg, urg_rad2step(urg, ANGLE_MIN0), urg_rad2step(urg, ANGLE_MAX0), 0);//scan en continu, on ne garde que les point entre -PI/2 et PI/2
                else
        		urg_set_scanning_parameter(urg, urg_rad2step(urg, ANGLE_MIN1), urg_rad2step(urg, ANGLE_MAX1), 0);//scan en continu, on ne garde que les point entre -PI/2 et PI/2
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

int get_robots_2d(struct coord *points, int n, struct coord *robot_pos, char *group, char *nbGroup){

	#define K 15	//nombre max de points abberrants consecutifs (angulairement) au milieu d'un groupe
	#define D 200	//mm, distance max entre 2 points les plus proches dans un groupe
	#define R 7		//nombre de points mini pour un robot

	char groupNbPoints[DETECTABLE_ROBOTS], _nbGroup = 0;
	
	if(group == NULL){
		group = (char*) malloc(sizeof(char) * n);
		if(group == NULL){
			fprintf(stderr, "data malloc error (%i)\n", n);
			exit(1);
		}		
	}
	if(points == NULL){
			fprintf(stderr, "get_points_2d : points non alloués\n");
			exit(1);
		}

	//Groupes 
	int i;
	printf("%d points\n", n);
	for(i=K; i<n; i++) {
		printf("%d ", n);
		int dmin = 35000, j, jmin = 0;
		unsigned long d[K];
		for(j=1; j<=K; j++){			
			d[j-1] = pow(points[i].x-points[i-j].x, 2) + pow(points[i].y-points[i-j].y, 2);
			if(d[j-1] < dmin){
				dmin = d[j-1];
				jmin = j;
			}
		}

		if(dmin < D*D){
			if(group[i-jmin] == 0){
				_nbGroup++;
				groupNbPoints[i-jmin] = 0;
				group[i-jmin] = _nbGroup;
			}				
			group[i] = group[i-jmin];
			groupNbPoints[i-jmin]++;
		}
	}
	printf("fin boucle\n");
	//if(nbGroup != NULL) *nbGroup = _nbGroup;
	//robots

	return 0;

}

void error_func(urg_t *urg, const char *message){
	urg_close(urg);
	fprintf(stderr, "%s :: %s\n", message, urg_error(urg)); //print le message d'erreur perso et celui issu de l'hokuyo
}

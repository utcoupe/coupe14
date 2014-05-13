#include "com.h"
#include "protocole/serial_switch.h"
#include "protocole/compat.h"
#include "protocole/protocole_serial.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void com_loop(const char* cam_pipe, const char* hok_pipe) {
	FILE *cam = 0, *hok = 0;

	printf("[MAIN]  Opening pipe : %s\n", cam_pipe);
	cam = fopen(cam_pipe, "r");
	if (cam == 0) {
		printf("[MAIN]  Failed to open camera pipe\n");
		exit(EXIT_FAILURE);
	} else {
		printf("[MAIN]  Pipe opened with cameras\n");
	}

	printf("[MAIN]  Opening pipe : %s\n", hok_pipe);
	hok = fopen(hok_pipe, "r");
	if (hok == 0) {
		printf("[MAIN]  Failed to open hokuyo pipe\n");
		exit(EXIT_FAILURE);
	} else {
		printf("[MAIN]  Pipe opened with hokuyo\n");
	}

	init_protocol_thread();

	while (1) {
		const int max_length = 255;
		char line_camera[max_length], line_hokuyo[max_length];
		int i_cam = 0, i_hok = 0, ignore_cam = 0, ignore_hok = 0, c = 0;

		//Parse char cameras
		c = fgetc(cam);
		if (i_cam < max_length && c != EOF) {
			line_camera[i_cam] = c;
			i_cam++;
		} else if (!ignore_cam) { //Affiche une message d'erreur, une seule fois
			ignore_cam = 1;
			printf("[MAIN]  Error : camera line too long for buffer, dropping line max=%d\n", max_length);
		} 

		//Parse une ligne camera
		if (c == '\n') {
			if (!ignore_cam) {
				parseCamera(line_camera);
			} else {
				ignore_cam = 0;
			}
			i_cam = 0;
		}

		//Parse char hokuyo
		c = fgetc(hok);
		if (i_hok < max_length && c != EOF) {
			line_hokuyo[i_hok] = c;
			i_hok++;
		} else if (!ignore_hok) { //Affiche une message d'erreur, une seule fois
			ignore_hok = 1;
			printf("[MAIN]  Error : hokuyo line too long for buffer, dropping line max=%d\n", max_length);
		} 

		//Parse une ligne camera
		if (c == '\n') {
			if (!ignore_hok) {
				parseHokuyo(line_hokuyo);
			} else {
				ignore_hok = 0;
			}
			i_hok = 0;
		}
		/*
		char buffer[255];
		fread(buffer, sizeof(char), 20, cam);
		printf("%s", buffer);
		fflush(stdout);
		fread(buffer, sizeof(char), 20, hok);
		printf("%s", buffer);
		fflush(stdout);*/
	}
	fclose(cam);
	fclose(hok);
}

void parseCamera(char *line) {
	static int ready = 0, nbr_tri = 0;
	static struct camData triangles[MAX_TRI];
	if (!ready) {
		if (strcmp(line, "READY\n") == 0) {
			ready = 1;
		} else {
			printf("%s", line); //Ecrire stdou tant qu'on est pas pret
		}
	} else if (strcmp(line, "END\n") == 0) { //Fin de frame
		pushCamData(triangles, nbr_tri);
		nbr_tri = 0;
	} else {
		char arg[50];
		char c = 0;
		int i = 0, j = 0;
		enum camArgs arg_type = x;

		while (c != '\n') { //Jusqua la fin de la ligne
			while (c != ' ' && c != '\n') { //Jusqua la fin de l'arg
				c = *(line++);
				arg[i++] = c;
			}
			i = 0;
			switch (arg_type) {
				case x:
					triangles[nbr_tri].x = atoi(arg);
					break;
				case y:
					triangles[nbr_tri].y = atoi(arg);
					break;
				case a:
					triangles[nbr_tri].a = atof(arg);
					break;
				case size:
					triangles[nbr_tri].size = atoi(arg);
					break;
				case color:
					triangles[nbr_tri].color = atoi(arg);
					break;
				case isDown:
					triangles[nbr_tri].isDown = atoi(arg);
					break;
				default:
					break;
			}
			arg_type++; //Next arg
		}
		if (arg_type == end) { //On a le bon nombre d'args : ok
			nbr_tri++;
		} else {
			printf("[MAIN]  Failed to parse camera data, expected %d args, got %d\n", end, arg_type);
		}
	}
}

void parseHokuyo(char *line) {
}

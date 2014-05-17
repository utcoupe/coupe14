#include "com.h"
#include "protocole/serial_switch.h"
#include "protocole/compat.h"
#include "protocole/protocole_serial.h"
#include "global.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

void setNonBlocking(FILE *f) {
	int fd = fileno(f);
	int flags;
	flags = fcntl(fd, F_GETFL, 0);
	flags |= O_NONBLOCK;
	fcntl(fd, F_SETFL, flags);
}

void com_loop(const char* cam_pipe, const char* hok_pipe) {
	FILE *cam = 0, *hok = 0;

	if (ENABLE_HOK) {
		printf("[MAIN]  Opening pipe : %s\n", hok_pipe);
		hok = fopen(hok_pipe, "r");
		setNonBlocking(hok);
		if (hok == 0) {
			perror("[MAIN]  Failed to open hokuyo pipe\n");
			exit(EXIT_FAILURE);
		} else {
			printf("[MAIN]  Pipe opened with hokuyo\n");
		}
	}

	if (ENABLE_CAM) {
		printf("[MAIN]  Opening pipe : %s\n", cam_pipe);
		cam = fopen(cam_pipe, "r");
		setNonBlocking(cam);
		if (cam == 0) {
			perror("[MAIN]  Failed to open camera pipe\n");
			exit(EXIT_FAILURE);
		} else {
			printf("[MAIN]  Pipe opened with cameras\n");
		}
	}

	printf("[MAIN]  Starting protocol thread\n");
	init_protocol_thread();

	printf("[MAIN]  Init done, beginning broadcast\n");
	const int max_length = 255;
	char line_camera[max_length], line_hokuyo[max_length];
	int i_cam = 0, i_hok = 0, ignore_cam = 0, ignore_hok = 0, c = 0;
	while (1) {
		//Parse char cameras
		if (ENABLE_CAM) {
			do {
				c = fgetc(cam);
				if (c != EOF) {
					if (i_cam < max_length) {
						line_camera[i_cam] = c;
						i_cam++;
					} else if (!ignore_cam) { //Affiche une message d'erreur, une seule fois
						ignore_cam = 1;
						printf("[MAIN]  Error : camera line too long for buffer, dropping line max=%d\n", max_length);
					} 
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
			} while (c != EOF);
		}
		
		if (ENABLE_HOK) {
			//Parse char hokuyo
			do {
				c = fgetc(hok);
				if (c != EOF) {
					if (i_hok < max_length) {
						line_hokuyo[i_hok] = c;
						i_hok++;
					} else if (!ignore_hok) { //Affiche une message d'erreur, une seule fois
						ignore_hok = 1;
						printf("[MAIN]  Error : hokuyo line too long for buffer, dropping line max=%d\n", max_length);
					} 
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
			} while (c != EOF);
		}
		usleep(50000); //Pause
	}
	fclose(cam);
	fclose(hok);
}


//Une ligne par triangle, chaque set finit par END\n
//x y a size color isdown
//x y a size color isdown
//x y a size color isdown
//END\n
void parseCamera(char *ori_line) {
	char *line = ori_line;
	char end_test[5];
	strncpy(end_test, line, 4);
	end_test[4] = '\0';
	static int nbr_tri = 0;
	static struct camData triangles[MAX_TRI];
	if (strcmp(end_test, "END\n") == 0) { //Fin de frame
		pushCamData(triangles, nbr_tri);
		printf("[MAIN]  New cam data : %d triangles\n", nbr_tri);
		nbr_tri = 0;
	} else {
		char arg[50];
		char c = 0;
		int i = 0, j = 0;
		enum camArgs arg_type = x;

		while (c != '\n') { //Jusqua la fin de la ligne
			do {
				c = line[j++];
				arg[i++] = c;
			} while (c != ' ' && c != '\n'); //Jusqua la fin de l'arg
			i = 0;
			switch (arg_type) {
				case x:
					triangles[nbr_tri].x = atoi(arg);
					arg_type = y;
					break;
				case y:
					triangles[nbr_tri].y = atoi(arg);
					arg_type = a;
					break;
				case a:
					triangles[nbr_tri].a = atof(arg);
					arg_type = size;
					break;
				case size:
					triangles[nbr_tri].size = atoi(arg);
					arg_type = color;
					break;
				case color:
					triangles[nbr_tri].color = atoi(arg);
					arg_type = isDown;
					break;
				case isDown:
					triangles[nbr_tri].isDown = atoi(arg);
					arg_type = end;
					break;
				default:
					break;
			}
		}
		if (arg_type == end) { //On a le bon nombre d'args : ok
			nbr_tri++;
		} else {
			printf("[MAIN]  Failed to parse camera data, expected %d args, got %d\n", end, arg_type);
		}
	}
}


// Une ligne par set de data :
// timestamp nbr_coords x1 y1 x2 y2 x3 y3
void parseHokuyo(char *ori_line) {
	char * line = ori_line;
	int nbr_robots = 0, nbr_robots_to_parse = 0;
	long timestamp = 0;
	struct hokData robots[NBR_ROBOTS];
	char arg[50];
	char c = 0;
	int i = 0, j = 0, arg_nbr = 0, ignore = 0, coord_index = 0;

	while (c != '\n') { //Jusqua la fin de la ligne
		do {
			c = line[j++];
			arg[i++] = c;
		} while (c != ' ' && c != '\n'); //Jusqua la fin de l'arg
		i = 0;

		coord_index = (arg_nbr-1) / 2;

		if (arg_nbr == 0) {
			timestamp = atol(arg);
		} else if (coord_index < NBR_ROBOTS) { //On attend encore des coords
			if ((arg_nbr+1) % 2 == 0) { //X
				robots[coord_index].x = atoi(arg);
			} else { //Y
				robots[coord_index].y = atoi(arg);
				nbr_robots++;
			}
		} else { //Trop d'arguments !
			ignore = 1;
		}
		arg_nbr++;
	}
	if (coord_index != NBR_ROBOTS-1) {
		ignore = 1;
	}
	if (!ignore) {
		pushHokData(robots, timestamp);
	} else {
		printf("[MAIN]  Failed to parse hokuyo data, got %d args\n", arg_nbr);
		printf("[MAIN]  %s", ori_line);
	}
}

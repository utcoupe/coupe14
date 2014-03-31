#include "lidar.h"
#include "global.h"
#include "robot.h"
#include "compat.h"
#include "protocole_serial.h"
#include "serial_switch.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>


#ifdef SDL
#include "gui.h"
#endif





void frame();


static int use_protocol = 0;
static struct lidar l1;
#ifdef SDL
static struct color l1Color;
#endif

long startTime;
static struct coord robots[MAX_ROBOTS];


int main(int argc, char **argv){
	
	if(argc <= 1 || ( strcmp(argv[1], "red") != 0 && strcmp(argv[1], "blue") ) ){
		fprintf(stderr, "usage: hokuyo {red|blue} [protocol]\n");
		return EXIT_FAILURE;
	}

	struct coord pos1;
	if( strcmp(argv[1], "red") == 0 ){
		pos1.x = -25;		
	}else{
		pos1.x = TAILLE_TABLE_X+25;
	}

	pos1.y = -25;

	if (argc == 3 && strcmp(argv[2], "protocol") == 0) {
		printf("Utilisation du protcole\n");
		use_protocol = 1;
	}

	l1 = initLidarAndCalibrate( hokuyo_urg, "/dev/ttyACM0", pos1, PI/2, 0, PI/2);
	//l1 = initLidar( hokuyo_urg, "/dev/ttyACM0", pos1, 0, 0, PI/2);


	#ifdef SDL
	l1Color = newColor(255, 0, 0);
	initSDL();
	#endif

	if (use_protocol) {
		printf("Lancement du thread protocole\n");
		init_protocol_thread();
	}

	startTime = timeMillis();
	printf("%sRunning ! ...\n", PREFIX);
	while(1){
		frame();
	}
	
}

void frame(){
	long timestamp;
	getPoints(&l1);
	timestamp = timeMillis() - startTime;
	//printf("nPoints:%i\n", l1.fm.n);
	int nRobots = getRobots(l1.points, l1.fm.n, robots);
	#ifdef SDL
	blitMap();
	blitLidar(l1.pos, l1Color);
	blitRobots(robots, nRobots);
	blitPoints(l1.points, l1.fm.n, l1Color);
	waitScreen();
	#endif
	if (use_protocol){
		pushCoords(robots, nRobots, timestamp);
	}
	else{
		printf("%s%li;%i", PREFIX, timestamp, nRobots);
		for(int i=0; i<nRobots; i++){
			printf(";%i:%i", robots[i].x, robots[i].y);
		}
		printf("\n");
	}
}


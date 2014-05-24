#include <urg_ctrl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>

#include "hokuyo_config.h"

#ifdef SDL
#include "gui.h"
#endif

void frame();

static Hok_t hok1, hok2;
static int use_protocol = 0;

void exit_handler() {
	printf("\n%sClosing lidar(s), please wait...\n", PREFIX);
	if (hok1.urg != 0)
		urg_disconnect(hok1.urg);
	if (hok2.urg != 0)
		urg_disconnect(hok2.urg);
	printf("%sExitting\n", PREFIX);
	//kill(getppid(), SIGUSR1); //Erreur envoyee au pere
}

static void catch_SIGINT(int signal){
	exit(EXIT_FAILURE);
}

int main(int argc, char **argv){
	bool nocalib = false;
	char *path = 0;

	atexit(exit_handler);
	
	if(argc <= 1 || ( strcmp(argv[1], "red") != 0 && strcmp(argv[1], "yellow") ) ){
		fprintf(stderr, "usage: hokuyo {red|yellow} [path_pipe]\n");
		exit(EXIT_FAILURE);
	}

	if (signal(SIGINT, catch_SIGINT) == SIG_ERR) {
        fpritnf(stderr, "An error occurred while setting a signal handler for SIGINT.\n");
		exit(EXIT_FAILURE);
    }

	if (argc >= 3) {
		path = argv[2];
		if (strcmp(path, "nocalib") == 0) {
			nocalib = true;
		} else {
			use_protocol = 1;
		}
	}

	/*
	if (nocalib) {
		l1 = initLidar("/dev/ttyACM0", posl1, angle1, a1min, a1max);
		l2 = initLidar("/dev/ttyACM1", posl2, angle2, a2min, a2max);
	} else {
		l1 = initLidarAndCalibrate("/dev/ttyACM0", posl1, angle1, a1min, a1max);
		l2 = initLidarAndCalibrate("/dev/ttyACM1", posl2, angle2, a2min, a2max);
	}*/


	#ifdef SDL
	struct color l1Color = {255, 0, 255}, l2Color = {0, 0, 255}, lColor {255, 0, 255};
	initSDL();
	#endif

	if (use_protocol) {
		init_protocol(path);
	}

	startTime = timeMillis();
	printf("%sRunning ! ...\n", PREFIX);
	while(1){
		frame();
	}
	exit(EXIT_SUCCESS);
}

void frame(){
	long timestamp;
	timestamp = timeMillis() - startTime;
	/*
	getPoints(&l1);
	getPoints(&l2);
	printf("%sDuration1 : %lims\n", PREFIX, timestamp-lastTime);
	timestamp = timeMillis() - startTime;
	printf("%sDuration2 : %lims\n", PREFIX, timestamp-lastTime);
	int nRobots1 = getRobots(l1.points, l1.fm.n, robots1);
	int nRobots2 = getRobots(l2.points, l2.fm.n, robots2);
	int nRobots = mergeRobots(robots1, nRobots1, robots2, nRobots2, robots);
	#ifdef SDL
	blitMap();
	blitLidar(l1.pos, l1Color);
	blitLidar(l2.pos, l2Color);
	blitRobots(robots1, nRobots1, l1Color);
	blitRobots(robots2, nRobots2, l2Color);
	blitRobots(robots, nRobots, lColor);
	blitPoints(l1.points, l1.fm.n, l1Color);
	blitPoints(l2.points, l2.fm.n, l2Color);
	waitScreen();
	#endif
	if (use_protocol){
		pushResults(robots, nRobots, timestamp);
	}
	else{
		printf("%sHOK1 - %li;%i", PREFIX, timestamp, nRobots1);
		for(int i=0; i<nRobots1; i++){
			printf(";%i:%i -- %i", robots1[i].pt.x, robots1[i].pt.y, robots1[i].size);
		}
		printf("\n");
		printf("%sHOK2 - %li;%i", PREFIX, timestamp, nRobots2);
		for(int i=0; i<nRobots2; i++){
			printf(";%i:%i -- %i", robots2[i].pt.x, robots2[i].pt.y, robots2[i].size);
		}
		printf("\n");
		printf("%sALL  - %li;%i", PREFIX, timestamp, nRobots);
		for(int i=0; i<nRobots; i++){
			printf(";%i:%i -- %i", robots[i].pt.x, robots[i].pt.y, robots[i].size);
		}
		printf("\n");
	}
	*/
	lastTime = timestamp;
}


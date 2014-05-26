#include <urg_ctrl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>

#include "hokuyo_config.h"
#include "utils.h"
#include "compat.h"
#include "communication.h"

#ifdef SDL
#include "gui.h"
#endif

void frame();

static Hok_t hok1, hok2;
static int use_protocol = 0;
static long timeStart = 0;

void exit_handler() {
	printf("\n%sClosing lidar(s), please wait...\n", PREFIX);
	if (hok1.urg != 0)
		urg_disconnect(hok1.urg);
	if (hok2.urg != 0)
		urg_disconnect(hok2.urg);
	printf("%sExitting\n", PREFIX);
	kill(getppid(), SIGUSR1); //Erreur envoyee au pere
}

static void catch_SIGINT(int signal){
	exit(EXIT_FAILURE);
}

int main(int argc, char **argv){
	int calib = 1, symetry = 0;
	char *path = 0;
	hok1.urg = 0;
	hok2.urg = 0;

	atexit(exit_handler);
	
	if(argc <= 1 || ( strcmp(argv[1], "red") != 0 && strcmp(argv[1], "yellow") ) ){
		fprintf(stderr, "usage: hokuyo {red|yellow} [path_pipe]\n");
		exit(EXIT_FAILURE);
	}

	if (signal(SIGINT, catch_SIGINT) == SIG_ERR) {
        fprintf(stderr, "An error occurred while setting a signal handler for SIGINT.\n");
		exit(EXIT_FAILURE);
    }
	
	if (strcmp(argv[1], "yellow") == 0) {
		symetry = 1;
	}

	if (argc >= 3) {
		path = argv[2];
		if (strcmp(path, "nocalib") == 0) {
			calib = 0;
		} else {
			use_protocol = 1;
		}
	}

	hok1 = initHokuyo("/dev/ttyACM0", HOK1_A, HOK1_CONE, (Pt_t){HOK1_X, HOK1_Y} );
	hok2 = initHokuyo("/dev/ttyACM1", HOK2_A, HOK2_CONE, (Pt_t){HOK2_X, HOK2_Y} );
	if (symetry) {
		hok1 = applySymetry(hok1);
		hok2 = applySymetry(hok2);
	}
	
	if (calib) {
		int error = 0;
		do {
			error = calibrate(&hok1);
		} while (error < 0);
		do {
			error = calibrate(&hok2);
		} while (error < 0);
	}

	#ifdef SDL
	initSDL();
	#endif

	if (use_protocol) {
		init_protocol(path);
	}

	printf("%sRunning ! ...\n", PREFIX);
	timeStart = timeMillis();
	while(1){
		frame();
		sleep(10);
	}
	exit(EXIT_SUCCESS);
}

void frame(){
	long timestamp;
	static long lastTime = 0;
	Pt_t pts1[MAX_DATA], pts2[MAX_DATA];
	Cluster_t robots1[MAX_CLUSTERS], robots2[MAX_CLUSTERS], robots[MAX_ROBOTS];
	int nPts1, nPts2, nRobots1 = 0, nRobots2 = 0, nRobots;

	printf("%sGetting points\n", PREFIX);

	nPts1 = getPoints(hok1, pts1);
	nPts2 = getPoints(hok2, pts2);

	printf("%sGot %d and %d points\n", PREFIX, nPts1, nPts2);

	
	timestamp = timeMillis() - timeStart;
	printf("%sDuration : %lims\n", PREFIX, timestamp-lastTime);

	nRobots1 = getClustersFromPts(pts1, nPts1, robots1);
	nRobots2 = getClustersFromPts(pts2, nPts2, robots2);

	printf("%sCalculated %d and %d clusters\n", PREFIX, nRobots1, nRobots2);

	nRobots1 = sortAndSelectRobots(nRobots1, robots1);
	nRobots2 = sortAndSelectRobots(nRobots2, robots2);

	nRobots = mergeRobots(robots1, nRobots1, robots2, nRobots2, robots);
	printf("%sGot %d robots\n", PREFIX, nRobots);
	
	#ifdef SDL
	struct color l1Color = {255, 0, 0}, l2Color = {0, 0, 255}, lColor = {255, 0, 255};
	blitMap();
	blitLidar(hok1.pt, l1Color);
	blitLidar(hok2.pt, l2Color);
	blitRobots(robots1, nRobots1, l1Color);
	blitRobots(robots2, nRobots2, l2Color);
	blitRobots(robots, nRobots, lColor);
	blitPoints(pts1, nPts1, l1Color);
	blitPoints(pts2, nPts2, l2Color);
	waitScreen();
	#endif

	if (use_protocol){
		//pushResults(robots, nRobots, timestamp);
	}
	//else{
		printf("%sHOK2 - %li;%i\n", PREFIX, timestamp, nRobots2);
		for(int i=0; i<nRobots2; i++){
			printf(";;%i:%i", robots2[i].center.x, robots2[i].center.y);
		}
		printf("\n");
		printf("%sHOK1 - %li;%i\n", PREFIX, timestamp, nRobots1);
		for(int i=0; i<nRobots1; i++){
			printf(";;%i:%i", robots1[i].center.x, robots1[i].center.y);
		}
		printf("\n");
		printf("%sALL  - %li;%i\n", PREFIX, timestamp, nRobots);
		for(int i=0; i<nRobots; i++){
			printf(";;%i:%i", robots[i].center.x, robots[i].center.y);
		}
		printf("\n");
	//	}
	lastTime = timestamp;
}


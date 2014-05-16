#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <sys/time.h>
#include <unistd.h>

#include "global.h"
#include "communication.h"
#include "compat.h"
#include "lidar.h"
#include "robot.h"

#ifdef SDL
#include "gui.h"
#endif

void frame();

static int use_protocol = 0;
static struct lidar l1, l2;
#ifdef SDL
static struct color l1Color, l2Color;
#endif

long startTime, lastTime = 0;
static struct coord robots[MAX_ROBOTS];

void exit_handler() {
	printf("\n%sClosing lidar(s), please wait...\n", PREFIX);

	struct itimerval it_val; //removing timer
	it_val.it_value.tv_sec = 0;
	it_val.it_value.tv_usec = 0;	
	it_val.it_interval.tv_sec = 0;
	it_val.it_interval.tv_usec = 0;
	if (setitimer(ITIMER_REAL, &it_val, NULL) == -1) {
		perror("error calling setitimer()");
	}

	closeLidar(&l1);
	closeLidar(&l2);
	printf("%sExitting\n", PREFIX);
	//kill(getppid(), SIGUSR1); //Erreur envoyee au pere
}

static void catch_SIGINT(int signal){
	exit(EXIT_FAILURE);
}

static void catch_SIGALRM(int signal){
	printf("Restarting Lidars...\n");
	restartLidar(&l1);
	restartLidar(&l2);
}

void resetTimer(){
	struct itimerval it_val;
	it_val.it_value.tv_sec = HOKUYO_WATCHDOG/1000;
	it_val.it_value.tv_usec = (HOKUYO_WATCHDOG*1000) % 1000000;	
	it_val.it_interval.tv_sec = 0;
	it_val.it_interval.tv_usec = 0;
	if (setitimer(ITIMER_REAL, &it_val, NULL) == -1) {
		perror("error calling setitimer()");
		exit(1);
	}
}

int main(int argc, char **argv){	
	if(argc <= 1 || ( strcmp(argv[1], "red") != 0 && strcmp(argv[1], "yellow") ) ){
		fprintf(stderr, "usage: hokuyo {red|yellow} [path_pipe]\n");
		exit(EXIT_FAILURE);
	}

	atexit(exit_handler);

    if (signal(SIGALRM, catch_SIGALRM) == SIG_ERR) {
        fputs("An error occurred while setting a signal handler for SIGALRM.\n", stderr);
        return EXIT_FAILURE;
    }

    if (signal(SIGINT, catch_SIGINT) == SIG_ERR) {
        fputs("An error occurred while setting a signal handler for SIGINT.\n", stderr);
        return EXIT_FAILURE;
    }

	struct coord posl1, posl2;
	posl1.y = -25;
	posl2.y = -25;
	if( strcmp(argv[1], "red") == 0 ){
		posl1.x = -25;	
		//posl2.y = TAILLE_TABLE_X+25;
		posl2.x = 1000;
	}else{
		posl1.x = TAILLE_TABLE_X+25;
		posl2.x = -25;
	}

	char *path = 0;
	if (argc == 3) {
		path = argv[2];
		use_protocol = 1;
	}

	//l1 = initLidarAndCalibrate( hokuyo_urg, "/dev/ttyACM0", posl1, PI/2, 0, PI/2);
	//l2 = initLidarAndCalibrate( hokuyo_urg, "/dev/ttyACM1", posl2, PI/2, 0, PI);
	l1 = initLidar( hokuyo_urg, "/dev/ttyACM0", posl1, PI/2, 0, PI/2);
	l2 = initLidar( hokuyo_urg, "/dev/ttyACM1", posl2, PI/2, 0, PI);


	#ifdef SDL
	l1Color = newColor(255, 0, 0);
	l2Color = newColor(0, 0, 255);
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

int getRobotsMerged(struct coord *points1, int n1, struct coord *points2, int n2, struct coord *robots){
	int size1 = sizeof(struct coord)*n1, size2 = sizeof(struct coord)*n2;

	struct coord *tmpPoints = malloc(size1+size2);
	if(tmpPoints == NULL) exit(EXIT_FAILURE);

	printf("getRobotMerged(): size1:%i, size2:%i\n", n1, n2);
	memcpy( tmpPoints, points1, size1 );
	memcpy( tmpPoints+n1, points2, size2 );
	int r = getRobots(tmpPoints, n1+n2, robots);
	free( tmpPoints );

	return r;
}

void frame(){
	resetTimer();
	long timestamp;
	getPoints(&l1);
	getPoints(&l2);
	timestamp = timeMillis() - startTime;
	//printf("%sDuration : %lims\n", PREFIX, timestamp-lastTime);
	if(lastTime != 0 && timestamp-lastTime > HOKUYO_WATCHDOG){
		printf("%s WatchDog exceeded: %li > %li\n", PREFIX, timestamp-lastTime, (long int)HOKUYO_WATCHDOG);
		restartLidar(&l1);
		restartLidar(&l2);
		return ;
	}
	//printf("nPoints:%i\n", l1.fm.n);
	int nRobots = getRobotsMerged(l1.points, l1.fm.n, l2.points, l2.fm.n, robots);
	#ifdef SDL
	blitMap();
	blitLidar(l1.pos, l1Color);
	blitLidar(l2.pos, l2Color);
	blitRobots(robots, nRobots);
	blitPoints(l1.points, l1.fm.n, l1Color);
	blitPoints(l2.points, l2.fm.n, l2Color);
	waitScreen();
	#endif
	fflush(stdout);
	if (use_protocol){
		pushResults(robots, nRobots, timestamp);
	} else {
		printf("%s%li;%i", PREFIX, timestamp, nRobots);
		for(int i=0; i<nRobots; i++){
			printf(";%i:%i", robots[i].x, robots[i].y);
		}
		printf("\n");
	}
	lastTime = timestamp;
}


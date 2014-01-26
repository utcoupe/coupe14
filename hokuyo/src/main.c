#include "lidar.h"
#include "global.h"
#include "robot.h"
#include "namedpipe.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>


#ifdef SDL
#include "gui.h"
#endif
/*
       +-------------------------------------------------------------------------------------+-> X
       |                    x                                                                |
       |                    x                                                                |
       |                   x                                                                 |
       |                  x                                                                  |
       |                 x                                                                   |
       |                x                                                                    |
       |   x         xxx                                                                     |
       |  x     xxxxx                                                                        |
       | xxxxxxx             |                                                               |
       |  x                --+--                                                             |
       |   x                 |                                                               |
       |                                                                                     |
       |                                                                                     |
       |                                                                                     |
       |                                                                                     |
       |   x                                                                                 |
       |  x                                                                                  |
       | xxxxx                                                                               |
       |  x   xx                                                                             |
       |   x    x                                                                            |
       |         x                                                                           |
  /||\ |         x                                                                           |
   ||  +-------------------------------------------------------------------------------------+
  +--+ |
  |l1| v
  +--+ Y

 */

void frame();


static int pipeactivated = 0;
static struct lidar l1;
#ifdef SDL
static struct color l1Color;
#endif

static struct coord robots[MAX_ROBOTS];


static void catch_SIGPIPE(int signo) {
    printf("Broken Pipe !!! exiting...\n");
    exit(EXIT_SUCCESS);
}

int main(int argc, char **argv){
  
  if(argc <= 1 || ( strcmp(argv[1], "red") != 0 && strcmp(argv[1], "blue") ) ){
    fprintf(stderr, "usage: hokuyo [red|blue] [pipe]\n");
    return EXIT_FAILURE;
  }

  if(argc == 3 && strcmp(argv[2], "pipe") == 0 ) pipeactivated = 1;

	struct coord pos1;
  if( strcmp(argv[1], "red") == 0 ){
  	pos1.x = -25;  	
  }else{
    pos1.x = TAILLE_TABLE_Y+25;
  }

  pos1.y = TAILLE_TABLE_Y+25;

	l1 = initLidar( hokuyo_urg, "/dev/ttyACM0", pos1, 0, -PI/2, 0);

  #ifdef SDL
	l1Color = newColor(255, 0, 0);
	initSDL();
  #endif

  if(pipeactivated){
    if (signal(SIGPIPE, catch_SIGPIPE) == SIGPIPE) {
        fputs("An error occurred while setting a SIGPIPE signal handler.\n", stderr);
        return EXIT_FAILURE;
    }
    initNamedPipe();
  } else printf("pipe desactivated !!!\n");

  printf("Running ! ...\n");
	while(1){
		frame();
	}
	
}

void frame(){
	getPoints(&l1);
  //printf("nPoints:%i\n", l1.fm.n);
  int nRobots = getRobots(l1.points, l1.fm.n, robots);
  #ifdef SDL
  blitMap();
	blitLidar(l1.pos, l1Color);
  blitRobots(robots, nRobots);
	blitPoints(l1.points, l1.fm.n, l1Color);
	waitScreen();
  #endif
  if(pipeactivated) printRobots(robots, nRobots);
  else{
    printf("%i", nRobots);
    for(int i=0; i<nRobots; i++){
      printf(";%i:%i", robots[i].x, robots[i].y);
    }
    printf("\n");
  }
}


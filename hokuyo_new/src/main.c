#include "lidar.h"
#include "global.h"
#include "gui.h"
#include "robot.h"
#include <stdio.h>
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



static struct lidar l1;
static struct color l1Color;

static struct coord robots[MAX_ROBOTS];

int main(int argc, char **argv){
	struct coord pos1;
	pos1.x = 25;
	pos1.y = TAILLE_TABLE_Y-25;

	l1 = initLidar( hokuyo_urg, "/dev/ttyACM0", pos1, 0, -PI/2, 0);
	l1Color = newColor(255, 0, 0);

	initSDL();

	while(1){
		frame();
	}
	
}

void frame(){
	getPoints(&l1);
  printf("nPoints:%i\n", l1.fm.n);
  int nRobots = getRobots(l1.points, l1.fm.n, robots);
	printf("robots\n");
  blitMap();
	blitLidar(l1.pos, l1Color);
  //blitRobots(robots, nRobots);
	blitPoints(l1.points, l1.fm.n, l1Color);
	waitScreen();
}


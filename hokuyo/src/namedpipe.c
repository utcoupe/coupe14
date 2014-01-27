#include "namedpipe.h"

#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include "global.h"


static FILE* pipefile = NULL;

void
initNamedPipe(){
	if(pipefile != NULL) exit(EXIT_FAILURE);

	printf("named pipe opening at %s\n", PIPENAME);

	if( ( pipefile = fopen(PIPENAME, "w") ) == NULL ){
		perror("named pipe closed, exiting\n");
		exit(EXIT_FAILURE);
	}
	printf("named pipe openened !\n");

	fprintf(pipefile, "Hi!\n");

	printf("named pipe connected !\n");
}

void
printRobots(struct coord *r, int nRobots){
	if(pipefile == NULL){
		fprintf(stderr, "Pipe disconnected !, exiting\n");
		exit(EXIT_FAILURE);
	}

	fprintf(pipefile, "%i", nRobots);
	for(int i=0; i<nRobots; i++){
		fprintf(pipefile, ";%i:%i", r[i].x, TAILLE_TABLE_Y-r[i].y);
	}
	fprintf(pipefile, "\n");
	fflush(pipefile);
}






























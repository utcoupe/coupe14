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

	printf("%snamed pipe opening at %s\n", PREFIX, PIPENAME);

	if( ( pipefile = fopen(PIPENAME, "w") ) == NULL ){
		fprintf(stderr, "%snamed pipe closed, exiting\n", PREFIX);
		exit(EXIT_FAILURE);
	}
	printf("%snamed pipe openened !\n", PREFIX);

	fprintf(pipefile, "Hi!\n");

	printf("%snamed pipe connected !\n", PREFIX);
}

void
printRobots(struct coord *r, int nRobots){
	if(pipefile == NULL){
		fprintf(stderr, "%sPipe disconnected !, exiting\n", PREFIX);
		exit(EXIT_FAILURE);
	}

	fprintf(pipefile, "%i", nRobots);
	for(int i=0; i<nRobots; i++){
		fprintf(pipefile, ";%i:%i", r[i].x, TAILLE_TABLE_Y-r[i].y);
	}
	fprintf(pipefile, "\n");
	fflush(pipefile);
}






























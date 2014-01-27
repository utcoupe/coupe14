#include "pipe.h"

#include <stdlib.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>


static FILE* pipefile = NULL;

void initPipe(){
	if(pipefile != NULL) {
		perror ("Initialisation d'un fipe deja existant\n");
		exit(EXIT_FAILURE);
	}

	printf("Ouverture d'un pipe %s\n", PIPENAME);

	if( ( pipefile = fopen(PIPENAME, "w") ) == NULL ){
		perror("Echec d'ouverture\n");
		exit(EXIT_FAILURE);
	}
	printf("Pipe ouvert\n");

	fprintf(pipefile, "START\n");

	printf("Pipe initialise\n");
}

void writePipe(int red, int yellow){
	if(pipefile == NULL){
		perror ("Pas de pipe\n");
		exit(EXIT_FAILURE);
	}

	fprintf(pipefile, "%5d;%5d\n", red, yellow);
	fflush(pipefile);
}














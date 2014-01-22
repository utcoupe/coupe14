/*******************************
* Quentin CHATEAU pour UTCOUPE *
* quentin.chateau@gmail.com    *
* Last edition : 30/09/2013    *
*******************************/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "global.h"
#include "fast_math.h"
#include "analyzer.h"

#ifdef SDL
#include "sdl.h"
#endif

int main(int argc, char **argv){
	//INITIALISATION
	struct urg_params hokuyo[NUMBER_HOKUYO];
	urg_t urg[NUMBER_HOKUYO];
        int error[NUMBER_HOKUYO];

	hokuyo[0].ptr = &urg[0];
	hokuyo[0].x = HOKUYO0_X;
	hokuyo[0].y = HOKUYO0_Y;
	error[0] = init(hokuyo[0].ptr, 0);

        if(NUMBER_HOKUYO == 2){
		hokuyo[1].ptr = &urg[1];
		hokuyo[1].x = HOKUYO1_X;
		hokuyo[1].y = HOKUYO1_Y;
		error[1] = init(hokuyo[1].ptr, 1);
        }

	if(error[0] < 0 || (error[1] < 0 && NUMBER_HOKUYO == 2)){
		fprintf(stderr, "Erreur de connection\n");
		exit(EXIT_FAILURE);
	}

	//On initialise la structure hokuyo avec ses paramètres de side et de position
	if(argc >= 2){
		if(strcmp(argv[1], "blue") == 0)
			hokuyo[0].side = BLUE_SIDE;
                        if(NUMBER_HOKUYO == 2){
			        hokuyo[1].side = BLUE_SIDE;
                        }
		else if(strcmp(argv[1], "red") == 0)
			hokuyo[0].side = RED_SIDE;
                        if(NUMBER_HOKUYO == 2){
			        hokuyo[1].side = RED_SIDE;
                        }
	}
	else{
		fprintf(stderr, "Préciser un side (blue/red)\n");
		exit(EXIT_FAILURE);
	}

	printf("Hokuyos initialized\n");

#ifdef SDL
	affichage_sdl(hokuyo);
#endif
	return 0;
}

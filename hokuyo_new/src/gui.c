#include "gui.h"
#include <SDL.h>
#include "stdio.h"

struct GUI_data{
	SDL_Surface *ecran, *terrain, *lidar, *point;
	SDL_Rect posTerrain, posLidar;
};
static struct GUI_data gui;

//Do NOT modify
#define GUI_WINDOW_REAL_SIZE_X (TAILLE_TABLE_X+2*BORDER_PADDING)
#define GUI_WINDOW_REAL_SIZE_Y (TAILLE_TABLE_Y+2*BORDER_PADDING)

#define GUI_TERRAIN_SIZE_X GUI_WINDOW_RESOLUTION_X*TAILLE_TABLE_X / GUI_WINDOW_REAL_SIZE_X
#define GUI_TERRAIN_SIZE_Y GUI_WINDOW_RESOLUTION_Y*TAILLE_TABLE_Y / GUI_WINDOW_REAL_SIZE_Y

#define GUI_LIDAR_SIZE_X GUI_WINDOW_RESOLUTION_X*LIDAR_SIZE / GUI_WINDOW_REAL_SIZE_X
#define GUI_LIDAR_SIZE_Y GUI_WINDOW_RESOLUTION_Y*LIDAR_SIZE / GUI_WINDOW_REAL_SIZE_Y

SDL_Rect
getPixelCoord(int x, int y){
	SDL_Rect p;
	p.x = (BORDER_PADDING+(float)x) * GUI_WINDOW_RESOLUTION_X / GUI_WINDOW_REAL_SIZE_X;
	p.y = (BORDER_PADDING+(float)y) * GUI_WINDOW_RESOLUTION_Y / GUI_WINDOW_REAL_SIZE_Y;
	return p;
}

void
initSDL(struct coord positionLidar){

	gui.ecran = SDL_SetVideoMode(GUI_WINDOW_RESOLUTION_X, GUI_WINDOW_RESOLUTION_Y, 32, SDL_HWSURFACE);
	if(gui.ecran == NULL) exit(EXIT_FAILURE);

	gui.terrain = SDL_CreateRGBSurface(SDL_HWSURFACE, GUI_TERRAIN_SIZE_X, GUI_TERRAIN_SIZE_Y, 32, 0, 0, 0, 0);
	SDL_FillRect(gui.terrain, NULL, SDL_MapRGB(gui.ecran->format, 200, 255, 200));
	gui.posTerrain = getPixelCoord(0, 0);

	gui.lidar = SDL_CreateRGBSurface(SDL_HWSURFACE, GUI_LIDAR_SIZE_X, GUI_LIDAR_SIZE_Y, 32, 0, 0, 0, 0);
	SDL_FillRect(gui.lidar, NULL, SDL_MapRGB(gui.ecran->format, 255, 0, 0));
	gui.posLidar = getPixelCoord(positionLidar.x-LIDAR_SIZE/2, positionLidar.y-LIDAR_SIZE/2);
	printf("Lidar\tx:%i\ty:%i\tsx:%i\tsy:%i\n", gui.posLidar.x, gui.posLidar.y, GUI_LIDAR_SIZE_X, GUI_LIDAR_SIZE_Y);

	gui.point = SDL_CreateRGBSurface(SDL_HWSURFACE, GUI_POINT_SIZE, GUI_POINT_SIZE, 32, 0, 0, 0, 0);
	SDL_FillRect(gui.point, NULL, SDL_MapRGB(gui.ecran->format, 255, 0, 0));

}

void
blit(struct coord *points, int nPoints){
	SDL_Event event;
	while( SDL_PollEvent(&event) ){ // On doit utiliser PollEvent car il ne faut pas attendre d'évènement de l'utilisateur pour mettre à jour la fenêtre
		switch(event.type) {
			case SDL_QUIT:
				exit(EXIT_SUCCESS);
				break;
			case SDL_KEYDOWN:
		        if(event.key.keysym.sym == SDLK_ESCAPE) exit(EXIT_SUCCESS);
		        break;
		}

	}
	SDL_FillRect(gui.ecran, NULL, SDL_MapRGB(gui.ecran->format, 255, 255, 255));

	SDL_BlitSurface(gui.terrain, NULL, gui.ecran, &(gui.posTerrain));
	SDL_BlitSurface(gui.lidar, NULL, gui.ecran, &(gui.posLidar));

	for(int i=0; i<nPoints; i++){
		SDL_Rect p = getPixelCoord(points[i].x, points[i].y);
		SDL_BlitSurface(gui.point, NULL, gui.ecran, &p );
	}

	while(SDL_Flip(gui.ecran)!=0){
        SDL_Delay(1);
    }
}



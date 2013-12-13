#include "Arduino.h"
#include "defines.h"

// Taille des ordres en nombres d'octets pris par ses paramètres, ordre codés sur 6 bits dont taille limité à 64
byte ordreSize[64];

void initSize()
{
	int i;
	//on l'initialise à une valeur aberrante, ainsi detectera si une taille n'a pas été initialisé
	for(i=0;i<64;i++)
		ordreSize[i]=255;

	//DEBUTPARSE
	ordreSize[PINGPING]=0;
	ordreSize[PONG]=0;
	ordreSize[A_GOTOA]=8;
	ordreSize[A_GOTO]=4;
	ordreSize[A_GOTOAR]=8;
	ordreSize[A_GOTOR]=4;
	ordreSize[A_ROT]=4;
	ordreSize[A_ROTR]=4;
	ordreSize[A_KILLG]=0;
	ordreSize[A_CLEANG]=0;
	ordreSize[A_PIDA]=6;
	ordreSize[A_PIDD]=6;
	//FINPARSE
}

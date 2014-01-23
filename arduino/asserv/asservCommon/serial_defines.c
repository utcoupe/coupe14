#include "serial_defines.h"

// Taille des ordres en nombres d'octets pris par ses paramètres, ordre codés sur 6 bits dont taille limité à 64
unsigned char ordreSize[MAX_ORDRES];

void initSize()
{
	int i;
	//on l'initialise à une valeur aberrante, ainsi detectera si une taille n'a pas été initialisé
	for(i=0;i<MAX_ORDRES;i++)
		ordreSize[i]=SIZE_ERROR;

	//DEBUTPARSE
	ordreSize[PINGPING]=0;
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
	ordreSize[A_PWM_TEST]=6;
	ordreSize[A_GET_CODER]=0;
	//FINPARSE
}

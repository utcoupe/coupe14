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
	ordreSize[O_BRAS_OUVRIR]=0;
	ordreSize[O_BRAS_OUVRIR]=0;
	//FINPARSE
}

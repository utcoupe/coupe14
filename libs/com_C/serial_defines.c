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
	ordreSize[PINGPING_AUTO]=0;
	ordreSize[PINGPING]=0;
	//ASSERV
	ordreSize[A_GOTOA]=10;
	ordreSize[A_GOTO]=6;
	ordreSize[A_ROT]=6;
	ordreSize[A_KILLG]=0;
	ordreSize[A_CLEANG]=0;
	ordreSize[A_PIDA]=12;
	ordreSize[A_PIDD]=12;
	ordreSize[A_PWM]=8;
	ordreSize[A_GET_CODER]=0;
	ordreSize[A_ACCMAX]=8;
	ordreSize[A_SET_POS]=8;
	ordreSize[A_GET_POS]=0;
	ordreSize[A_GET_POS_ID]=0;

	//OTHERS
	//FM
	ordreSize[O_RET_OUVRIR]=2;
	ordreSize[O_RET_FERMER]=2;
	ordreSize[O_GET_TRIANGLE]=8;
	ordreSize[O_STORE_TRIANGLE]=4;
	ordreSize[O_GET_BRAS_STATUS]=2;
	ordreSize[O_BRAS_OUVRIR]=2;
	ordreSize[O_BRAS_FERMER]=2;
	//TIBOT
	ordreSize[O_TIR_FILET]=2;
	ordreSize[O_TIR_BALLE]=4; //Combien de balles ?
	ordreSize[O_BALAI]=4; //Quel coté ?

	//GENERAL
	ordreSize[GET_CAM]=0;
	ordreSize[GET_HOKUYO]=0;
	ordreSize[GET_LAST_ID]=0;

	ordreSize[PAUSE]=0;
	ordreSize[RESUME]=0;
	ordreSize[RESET_ID]=0;
	//FINPARSE
}

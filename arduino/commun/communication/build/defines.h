#ifndef DEFINE_DEFINES
#define DEFINE_DEFINES


/* 
Fichier de define commun aux 4 arduinos
Les ordres sont commun à toutes les arduinos
Tous les ordres sont codées sur 6 bits, le bit de poids fort est toujours réservé au protocole
Le parseur python prend ce qu'il y a entre //DEBUTPARSE et //FINPARSE
*/


//Toutes les transmissions passent par l'IA donc on ne met que l'adresse du second périfierique concerné
enum address{
	//l'adresse 0 est réservé au protocole donc on commence à 1

	//DEBUTPARSE
	ADDR_FLUSSMITTEL_OTHER=1,
	ADDR_FLUSSMITTEL_ASSERV,
	ADDR_TIBOT_OTHER,
	ADDR_TIBOT_ASSERV,
	ADDR_HOKUYO
	//FINPARSE
};


//Codes des ordres (sur 6 bits)
enum ordre {
	//DEBUTPARSE
	PINGPING,
	PONG,
	A_GOTOA,
	A_GOTO,
	A_GOTOAR,
	A_GOTOR,
	A_ROT,
	A_ROTR,
	A_KILLG,
	A_CLEANG,
	A_PIDA,
	A_PIDD
	//FINPARSE
};

#endif

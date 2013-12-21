#ifndef DEFINE_DEFINES
#define DEFINE_DEFINES

#define SIZE_ERROR 255
#define MAX_ORDRES 64

#define INVALID_MESSAGE 0xC0
#define PROTOCOL_BIT 0x80
#define END 0x80

void initSize();

/* 
Fichier de define commun aux 4 arduinos
Les ordres sont commun à toutes les arduinos
Tous les ordres sont codées sur 6 bits, le bit de poids fort est toujours réservé au protocole
Le parseur python prend ce qu'il y a entre les balises de parse, ne pas les écrirent ailleurs
Si vous voulez commentez une enumération, il faut le faire sur la même ligne et après la virgule
Il faut toujours mettre un espace entre une enumération et le commentaire qui suit
*/


//Toutes les transmissions passent par l'IA donc on ne met que l'adresse du second périfierique concerné
enum address{
	//l'adresse 0 est réservé au protocole donc on commence à 1

	//DEBUTPARSE
	ADDR_FLUSSMITTEL_OTHER= 1,
	ADDR_FLUSSMITTEL_ASSERV,
	ADDR_TIBOT_OTHER,
	ADDR_TIBOT_ASSERV,
	ADDR_HOKUYO,
	ORDRE_NON_PARSE
	//FINPARSE
};


//Codes des ordres (sur 6 bits)
enum ordre {
	//DEBUTPARSE
	PINGPING, 
	PONG, 
	A_GOTOA, //@int @int @float
	A_GOTO, //@int @int
	A_GOTOAR, //@int @int @float
	A_GOTOR, //@int @int
	A_ROT, //@float
	A_ROTR, //@float
	A_KILLG, 
	A_CLEANG,
	A_PIDA, //@int @int @int
	A_PIDD, //@int @int @int
	A_PWM_TEST, //@int @int @int
	A_GET_CODER,
	ORDRE_NON_PARSE
	//FINPARSE
};

#endif

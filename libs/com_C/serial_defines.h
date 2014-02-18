#ifndef DEFINE_DEFINES
#define DEFINE_DEFINES

#define SIZE_ERROR 255
#define MAX_ORDRES 64
#define ID_MAX 63

#define INVALID_MESSAGE 0x40
#define PROTOCOL_BIT 0x80
#define END 0x80
#define RESET 0xC0
#define RESET_CONF 0xE0

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
	ADDR_FLUSSMITTEL_CAM,
	ADDR_TIBOT_OTHER,
	ADDR_TIBOT_ASSERV,
	ADDR_HOKUYO,
	ADRESSE_NON_PARSE
	//FINPARSE
};


//Codes des ordres (sur 6 bits)
enum ordre {
	//DEBUTPARSE
	PINGPING_AUTO,
	PINGPING, 	
	A_GOTOA, 	//@int @int @float
	A_GOTO, 	//@int @int
	A_GOTOAR, 	//@int @int @float
	A_GOTOR, 	//@int @int
	A_ROT, 		//@float
	A_ROTR, 	//@float
	A_KILLG, 
	A_CLEANG,
	A_PIDA, 	//@float @float @float
	A_PIDD, 	//@float @float @float
	A_GET_CODER, 	//#long #long
	A_PWM_TEST, 	//@int @int @int
	A_ACCMAX,	//@float
	A_RESET_POS,
	A_GET_POS,	//#int #int #float

	O_BRAS_OUVRIR,
	O_BRAS_FERMER,
	O_RET_OUVRIR,
	O_RET_FERMER,
	O_MONTER_ASC,	
	O_BAISSER_ASC,

	GET_CAM,	//#int #int
	GET_HOKUYO,	//#int #int #int #int #int #int #int #int #int
	ORDRE_NON_PARSE
	//FINPARSE
};

#endif

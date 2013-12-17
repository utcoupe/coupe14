// DEFINES DE PROTOCOLE SERIAL
// DESCRIPTION DES BITS :
// [0-2] : address
// [3-7] : order
//
// Description du protocole :
//
// Envoyer -> Recepteur
// [1B] adresse + ordre
// [xB] x octets de paramètres

#define MAX_DATA_SIZE 10

//////////////////////////////////
// 				//
// 	ADDRESSES 		//
// L'adresse 0b000xxxxx est réservée au broadcast
//////////////////////////////////

#define BROADCAST_ADDR 		0b00000000

#define FLUSSMITTEL_ASSERV_ADDR	0b00100000
#define FLUSSMITTEL_OTHERS_ADDR	0b01000000
#define FLUSSMITTEL_RASPI_ADDR 	0b01100000

#define TIBOT_ASSERV_ADDR 	0b10000000
#define TIBOT_OTHERS_ADDR 	0b10100000

#define HOKUYO_ADDR 		0b11000000

#define IA_ADDR 		0b11100000


//////////////////////////////////
// 				//
// 	All 			//
// Ordres à tout les robots 	//
// 				//
//////////////////////////////////

// PING-PONG
// L'IA peut ping un ou l'ensemble des robots
// Le(s) robot concerné répond par un pong non adressé

// PING
#define O_PING 			0b00011111
#define O_PING_SIZE 0
// none

// PONG
#define O_PONG 			0b00011110
#define O_PONG_SIZE 0
// none


//////////////////////////////////
// 				//
// 	      Asserv  		//
// Flussmittel ET Tibot ont les //
// 	 meme commandes 	//
// 				//
//////////////////////////////////

// GOTOA - Aller à une position dans un certain angle
#define A_GOTOA 		0b00000001
#define A_GOTOA_SIZE 8
// int16 int16 float

// GOTO - Aller à une position sans contrainte d'angle
#define A_GOTO 			0b00000010
#define A_GOTO_SIZE 4
// int16 int16

// GOTOA - Aller à une position dans un certain angle en relatif
#define A_GOTOAR 		0b00000011
#define A_GOTOAR_SIZE 8
// int16 int16 float

// GOTO - Aller à une position sans contrainte d'angle en relatif
#define A_GOTOR			0b00000100
#define A_GOTOR_SIZE 4
// int16 int16

// ROT - Se positionner en angle
#define A_ROT 			0b00000101
#define A_ROT_SIZE 4
// float

// ROTR - Se positionner en angle en relatif
#define A_ROTR 			0b00000110
#define A_ROTR_SIZE 4
// float

// KILLG - Kill le goal actuel
#define A_KILLG 		0b00000111
#define A_KILLG_SIZE 0
// none

// CLEANG - Vide la file de goals
#define A_CLEANG 		0b00001000
#define A_CLEANG_SIZE 0
//none

// PIDA - Réglade PID angle
#define A_PIDA 			0b00001001
#define A_PIDA_SIZE 6
//int16 int16 int16

// PIDD - Réglade PID distance
#define A_PIDD 			0b00001010
#define A_PIDD_SIZE 6
//int16 int16 int16

//////////////////////////////////
// 				//
// 	FlussMittel asserv 	//
// 				//
//////////////////////////////////

#define AFM_GOTOA 		A_GOTOA 	+FLUSSMITTEL_ASSERV_ADDR
#define AFM_GOTO 		A_GOTO 		+FLUSSMITTEL_ASSERV_ADDR
#define AFM_GOTOAR 		A_GOTOAR 	+FLUSSMITTEL_ASSERV_ADDR
#define AFM_GOTOR		A_GOTOR 	+FLUSSMITTEL_ASSERV_ADDR
#define AFM_ROT 		A_ROT 		+FLUSSMITTEL_ASSERV_ADDR
#define AFM_ROTR 		A_ROTR 		+FLUSSMITTEL_ASSERV_ADDR
#define AFM_KILLG 		A_KILLG 	+FLUSSMITTEL_ASSERV_ADDR
#define AFM_CLEANG 		A_CLEANG 	+FLUSSMITTEL_ASSERV_ADDR
#define AFM_PIDA 		A_PIDA 		+FLUSSMITTEL_ASSERV_ADDR
#define AFM_PIDD 		A_PIDD 		+FLUSSMITTEL_ASSERV_ADDR

//////////////////////////////////
// 				//
// 	FlussMittel others 	//
// 				//
//////////////////////////////////


//////////////////////////////////
// 				//
// 	FlussMittel raspi 	//
// 				//
//////////////////////////////////


//////////////////////////////////
// 				//
// 	Tibot others 		//
// 				//
//////////////////////////////////


//////////////////////////////////
// 				//
// 	Tibot asserv 		//
// 				//
//////////////////////////////////

#define ATI_GOTOA 		A_GOTOA 	+TIBOT_ASSERV_ADDR
#define ATI_GOTO 		A_GOTO 		+TIBOT_ASSERV_ADDR
#define ATI_GOTOAR 		A_GOTOAR 	+TIBOT_ASSERV_ADDR
#define ATI_GOTOR		A_GOTOR 	+TIBOT_ASSERV_ADDR
#define ATI_ROT 		A_ROT 		+TIBOT_ASSERV_ADDR
#define ATI_ROTR 		A_ROTR 		+TIBOT_ASSERV_ADDR
#define ATI_KILLG 		A_KILLG 	+TIBOT_ASSERV_ADDR
#define ATI_CLEANG 		A_CLEANG 	+TIBOT_ASSERV_ADDR
#define ATI_PIDA 		A_PIDA 		+TIBOT_ASSERV_ADDR
#define ATI_PIDD 		A_PIDD 		+TIBOT_ASSERV_ADDR

//////////////////////////////////
// 				//
// 	Hokuyo 			//
// 				//
//////////////////////////////////

/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 11/12/13			*
 ****************************************/
#include "serial_decoder.h"
#include "serial_defines.h"
#include "serial_local.h"
#include "serial_switch.h"

void executeCmd(char serial_data){
	//static char checksum = 0;
	static char ordre = 0;
	static int argcc = 0;
	static int argc = 0;
	static char argv[MAX_DATA_SIZE];

	static enum etape etape = ador;

	//checksum = checksum ^ serial_data;//checksum

	switch(etape){
	case ador: //Si on attend un ordre/adresse
		ordre = serial_data;
		argc = getSize(ordre); //On recupere la taille des data à suivre
		argcc = 0; //On reset le compteur des data
		if(((ordre & 0xE0) == LOCAL_ADDR) || ((ordre & 0xE0) == BROADCAST_ADDR)){ //Si on est sur le robot cible de l'ordre
			if(argc > 0)
				etape = param;
			else{
				switchOrder(ordre, 0, 0);
				etape = ador; //fin de séquence
			}
		}
		else{
			etape = wait;
		}
		break;
	case param:
		argv[argcc++] = serial_data; //On recopie le byte dans l'argv et on post-incrémente argcc
		if(argcc >= argc){
			switchOrder(ordre, argc, argv);
			etape = ador;
		}
		break;
	case wait:
		if(++argcc >= argc)//on incrémente le compteur puis on le compare à l'argc
			etape = ador; //fin de séquence
		break;
	}
}

// Envisager un script pyhton pour écrire la fonction ci-dessous
// tout les case sont de la forme :
// case X_X:
// 	return X_X_SIZE;
//<PYTHON-MARKER>
int getSize(char ordre){
	switch(ordre){
	case AFM_GOTO:
	case ATI_GOTO:
		return A_GOTO_SIZE;
	case AFM_GOTOA:
	case ATI_GOTOA:
		return A_GOTOA_SIZE;
	case AFM_GOTOR:
	case ATI_GOTOR:
		return A_GOTOR_SIZE;
	case AFM_GOTOAR:
	case ATI_GOTOAR:
		return A_GOTOAR_SIZE;
	case AFM_ROT:
	case ATI_ROT:
		return A_ROT_SIZE;
	case AFM_ROTR:
	case ATI_ROTR:
		return A_ROTR_SIZE;
	case AFM_PIDA:
	case ATI_PIDA:
		return A_PIDA_SIZE;
	case AFM_PIDD:
	case ATI_PIDD:
		return A_PIDD_SIZE;
	case AFM_KILLG:
	case ATI_KILLG:
		return A_KILLG_SIZE;
	case AFM_CLEANG:
	case ATI_CLEANG:
		return A_CLEANG_SIZE;
	default: //Commandes génériques
		ordre &= 0b00011111;
		switch(ordre){
		case O_PING:
			return O_PING_SIZE;
		case O_PONG:
			return O_PONG_SIZE;
		default:
			return -1;//Pas un ordre
		}
	}
}

/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 11/12/13			*
 ****************************************/
#include "serial_switch.h"
#include "serial_defines.h"
#include "serial_types.h"

int switchOrder(char ordre, int argc, char *argv){
	switch(ordre){
	case ORDRE_001:
		break;
	default:
		return -1;//commande inconnue
	}
	return 0;
}

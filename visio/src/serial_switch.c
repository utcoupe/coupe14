/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/
#include "serial_switch.h"
#include "serial_defines.h"
#include "serial_types.h"
#include "pipe.h"

#include <stdint.h>
#include <stdio.h>

//La fonction renvoit le nombre d'octet dans ret, chaine de caractère de réponse. Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon){ 
	int ret_size = 0;
	switch(ordre){
	case GET_CAM: {
		FILE* f = fopen(PIPENAME, "r");
		int32_t red, yellow;
		fseek (f, -13, SEEK_END);
		while (fgetc (f) != '\n');
		fscanf(f, "%d;%d\n", &red, &yellow);
		printf("red = %d\tyellow = %d\n", red, yellow);
		ltob(red, ret);
		ltob(yellow, ret+4);
		ret_size = 8;
		break;
	}
	default:
		return -1;//commande inconnue
	}
	return ret_size;
}

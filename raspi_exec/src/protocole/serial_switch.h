/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/
#ifndef SERIAL_SWITCH_H
#define SERIAL_SWITCH_H

#include "compat.h"
#include "../com.h"

void pushCamData(struct camData *data, int nbr);
void pushHokData(struct hokData *data, long timestamp);
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon);//Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer 

#endif

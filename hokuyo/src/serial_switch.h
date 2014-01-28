/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/
#ifndef SERIAL_SWITCH_H
#define SERIAL_SWITCH_H

#include "fast_math.h"
#include "compat.h"

void pushCoords(struct coord *n_robots, int n);
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon);//Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer 

#endif

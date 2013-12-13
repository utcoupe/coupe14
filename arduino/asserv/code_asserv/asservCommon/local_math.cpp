/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 25/10/13			*
 ****************************************/

#include "local_math.h"
#include <math.h>

double moduloTwoPI(double angle){
	if(angle >= 0)
		while(angle >= M_PI)
			angle -= 2.0*M_PI;
	else
		while(angle < -M_PI)
			angle += 2.0*M_PI;
	return angle;
}

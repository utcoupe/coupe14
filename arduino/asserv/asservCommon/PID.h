/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#ifndef PID_H
#define PID_H

#include "parameters.h"

enum anti_windup_mode {none, bound}; //Pour réguler l'effet de windup de l'intégrale
/*
none : pas d'anti-windup
bound : limite la valeur de l'intégrale entre +max_I et -max_I
*/

class PID{
	public:
	void setPID(float n_P, float n_I, float n_D);
	void setBias(float n_bias);
	void reset();
	float getOutput();
	float compute(float error);
	PID(float n_p = 0, float n_I = 0, float n_D = 0, float n_bias = 0);
	private:
	float P, I, D;
	float last_error; //derniere erreur pour la (D)ériée
	float output;
	float error_I; //somme des erreurs * intervale = (I)ntégrale
	float bias; //somme constante ajoutée au résultat du PID
	bool initDone; //permet d'éviter les erreurs dues à l'absence de dérivée au premier compute
};

#endif

/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#ifndef PID_H
#define PID_H

#include "parameters.h"


class PID{
	public:
	void setPID(double n_P, double n_I, double n_D);
	void setBias(double n_bias);
	void reset();
	double getOutput();
	double compute(double error);	
	PID(double n_p = 0, double n_I = 0, double n_D = 0, double n_bias = 0);
	private:
	double P, I, D;
	double last_error; //derniere erreur pour la (D)ériée
	double output;
	double error_I; //somme des erreurs * intervale = (I)ntégrale
	double bias; //somme constante ajoutée au résultat du PID
	bool initDone; //permet d'éviter les erreurs dues à l'absence de dérivée au premier compute
};

#endif

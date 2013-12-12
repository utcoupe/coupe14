/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#include "PID.h"
#include "include_arduino.h"

PID::PID(double n_P, double n_I, double n_D, double n_bias){
	setPID(n_P,n_I,n_D);
	setBias(n_bias);
	reset();
	
}

void PID::setPID(double n_P, double n_I, double n_D){
	if(n_P == 0 || n_I < 0 || n_D < 0)
		return; //Controle de PID correct
	P = n_P;
	I = n_I;
	D = n_D;
}

void PID::setBias(double n_bias){
	bias = n_bias;
}

void PID::reset(){
	last_error = 0;//ici, on va créer une premire dérivée trop grande, ce sera corrigé à l'initialisation du compute
	error_I = 0;
	output = 0;
	initDone = false;
}

double PID::compute(double error){
	double error_D;

	if(!initDone){ //Lors du premier compute, on ne tient pas compte de I et D
		error_I = 0;
		error_D = 0;
		initDone = true;	
	}
	else{
		error_D = (error - last_error); //derivée = deltaErreur/dt - dt est la période de compute
		error_I = error_I + error; //integrale = somme(erreur*dt) - dt est la période de compute
	}
	
	output = bias + (P*error) + (I*error_I) + (D*error_D); //calcul de la sortie avec le PID

	last_error = error;

	return output;
}

double PID::getOutput(){
	return output;
}

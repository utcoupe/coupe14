/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#include "control.h"
#include "compaArduino.h"
#include "motor.h"
#include "local_math.h"

#include <math.h>
/********************************************************
 * 							*
 * 		      CLASSE CONTROLE			*
 *							*
 ********************************************************/

/********** PUBLIC **********/
Control::Control(){
	setPID_angle(ANG_P, ANG_I, ANG_D);
	setPID_distance(DIS_P, DIS_I, DIS_D);
	setPID_speed(SPD_P , SPD_I, SPD_D);
	setPwmMin(PWM_MIN);
	max_angle = MAX_ANGLE;
	setMaxSpd(SPD_MAX);
	setMaxAcc(ACC_MAX);

	value_pwm_right = 0;
	value_pwm_left = 0;
}

int Control::compute(){
	static bool reset = true, order_started = false;
	static long start_time;
	int overflow = NO_OVERFLOW;
	struct goal current_goal = fifo.getCurrentGoal();
	pos current_pos = robot.getMmPos();
	long now = timeMicros();
	robot.update();

	if(fifo.isPaused() || current_goal.type == NO_GOAL){
		value_pwm_right = 0;
		value_pwm_left = 0;
	}
	else{
		if(current_goal.isReached){//Si le but est atteint et que ce n'est pas le dernier, on passe au suivant
#ifdef DEBUG
			Serial.write("Next GOAL - ");
#endif
			current_goal = fifo.gotoNext();
			reset = true;
		}

		if(reset){//permet de reset des variables entre les goals
			PID_Angle.reset();
			PID_Distance.reset();
			PID_SpdR.reset();
			PID_SpdL.reset();
			reset = false;
			order_started = false;
		}
	
	/* Choix de l'action en fonction du type d'objectif */
		switch(current_goal.type){
			case TYPE_ANG :
			{
				double da = current_goal.data_1 - current_pos.angle;
				overflow = controlAngle(da);
#ifdef DEBUG
				static int counter = 0;
				counter++;
				if(counter > 100){
					counter = 0;
					Serial.println(da);
				}
#endif
				if(abs(current_goal.data_1 - current_pos.angle) < ERROR_ANGLE)
					Serial.println("Reached");
				//	fifo.pushIsReached();
				break;
			}

			case TYPE_POS :
			{
				double dx = current_goal.data_1 - current_pos.x;
				double dy = current_goal.data_2 - current_pos.y;
				double goal_a = atan2(dy, dx);
				double da = moduloTwoPI(goal_a - current_pos.angle);
				double dd = sqrt(pow(dx, 2.0)+pow(dy, 2.0));//erreur en distance

				if(da > max_angle)//On tourne sur place avant de se déplacer
					overflow = controlAngle(da);
				else
					overflow = controlPos(da, dd + current_goal.data_3);//erreur en dist = dist au point + dist additionelle
				if(dd < ERROR_POS)
					fifo.pushIsReached();
				break;
			}

			case TYPE_PWM :
			{
				if(!order_started){
					start_time = now;
					order_started = true;
				}
				if((now - start_time)/1000.0 <= current_goal.data_3){
					overflow = setPwms(current_goal.data_2,current_goal.data_1,false);
				}
				else{
					overflow = setPwms(0,0,false);
					fifo.pushIsReached();
				}
				break;
			}

			case TYPE_SPD :
			{
				if(!order_started){
					start_time = now;
					order_started = true;
				}
				if((now - start_time)/1000.0 <= current_goal.data_3){
					overflow = controlSpd(current_goal.data_1, current_goal.data_2);
				}
				else{
					value_pwm_right = 0;
					value_pwm_left = 0;
					fifo.pushIsReached();
				}
				break;
			}

			default:
			{
#ifdef DEBUG
				Serial.write("No Goal ? - ");
#endif
				break;
			}	
		}
	}

	applyPwm();
	return overflow;
}

void Control::update_robot_state(){
	robot.update();
}

void Control::reset(){
	value_pwm_left = 0;
	value_pwm_right = 0;
	fifo.clearGoals();
	robot.reset();
	applyPwm();
}


void Control::setPID_angle(double n_P, double n_I, double n_D){
	PID_Angle.setPID(n_P, n_I, n_D);
}

void Control::setPID_distance(double n_P, double n_I, double n_D){
	PID_Distance.setPID(n_P, n_I, n_D);
}

void Control::setPID_speed(double n_P, double n_I, double n_D){
	PID_SpdR.setPID(n_P, n_I, n_D);
	PID_SpdL.setPID(n_P, n_I, n_D);
}

void Control::setPwmMin(int n_pwm_min){
	pwm_min = n_pwm_min;
}

void Control::setMaxAngCurv(double n_max_ang){
	max_angle = n_max_ang;
}

void Control::setMaxSpd(double n_max_spd){
	max_spd = n_max_spd;
}

void Control::setMaxAcc(double n_max_acc){
	max_acc = n_max_acc;
}


void Control::pushPos(pos n_pos){
	robot.pushMmPos(n_pos);
}

int Control::pushGoal(int ID, int p_type, double p_data_1, double p_data_2, double p_data_3){
	return fifo.pushGoal(ID, p_type, p_data_1, p_data_2, p_data_3);
}

void Control::nextGoal(){
	fifo.gotoNext();
}

void Control::clearGoals(){
	fifo.clearGoals();
}

pos Control::getPos(){
	return robot.getMmPos();
}

spd Control::getMotorSpd(){
	return robot.getMmSpdMotor();
}

spd Control::getEncoderSpd(){
	return robot.getMmSpdEncoder();
}

Encoder* Control::getRenc(){
	return robot.getRenc();
}

Encoder* Control::getLenc(){
	return robot.getLenc();
}

void Control::pause(){
	fifo.pause();
}

void Control::resume(){
	fifo.resume();
}

/********** PRIVATE **********/

int Control::setPwms(int pwm_right, int pwm_left, bool enable_pwm_min){
	bool overflowPwm = false;
	//Ajout des pwm minimale : "shift" des pwm
	if(pwm_min != 0 && enable_pwm_min){
		if(pwm_right > 0)
			pwm_right += pwm_min;
		else if(pwm_right < 0)
			pwm_right -= pwm_min;
		if(pwm_left > 0)
			pwm_left += pwm_min;
		else if(pwm_left < 0)
			pwm_left -= pwm_min;
	}

	//Tests d'overflow
	if(pwm_right > 254){
		overflowPwm = PWM_OVERFLOW;
		pwm_right = 254;
	}
	else if(pwm_right < -254){
		overflowPwm = PWM_OVERFLOW;
		pwm_right = -254;
	}
	if(pwm_left > 254){
		overflowPwm = PWM_OVERFLOW;
		pwm_left = 254;
	}
	else if(pwm_left < -254){
		overflowPwm = PWM_OVERFLOW;
		pwm_left = -254;
	}
	value_pwm_right = pwm_right;
	value_pwm_left = pwm_left;

	return overflowPwm;
}

void Control::checkSpd(double *consigne, double last)
{
	//Check MAX_SPD
	if(*consigne > max_spd){//test d'overflow
		*consigne = max_spd;
	}
	else if(*consigne < -max_spd){//test d'overflow
		*consigne = -max_spd;
	}
	//Check MAX_ACC
	if(*consigne > last + max_acc){
		*consigne = last + max_acc;
	}
	else if(*consigne < last - max_acc){
		*consigne = last - max_acc;
	}
}

int Control::controlAngle(double da)
{
	spd current_spd = robot.getMmSpdMotor();
	double consigneSpd;
	int consignePwmL, consignePwmR;
	static double last_consigneSpd = 0;
	bool overflowPwm = false;

	//Asservissement en position, renvoie une consigne de vitesse
	consigneSpd = PID_Angle.compute(da);

	checkSpd(&consigneSpd, last_consigneSpd);
		
	//Asservissement en vitesse
	consignePwmR = PID_SpdR.compute(consigneSpd - current_spd.R); 
	consignePwmL = PID_SpdL.compute((-consigneSpd) - current_spd.L); 

	overflowPwm = setPwms(consignePwmR, consignePwmL, false);

	last_consigneSpd = consigneSpd;

	if(overflowPwm)
		return PWM_OVERFLOW;
	else
		return NO_OVERFLOW;
}

int Control::controlPos(double da, double dd)
{
	//spd current_spd = robot.getMmSpdMotor();
	double consigneSpdR, consigneSpdL, consigneSpdAngle, consigneSpdDistance, consignePwmR, consignePwmL;
	//static double last_consigneSpdR = 0;
	//static double last_consigneSpdL = 0;
	bool overflowPwm = false;

	//Asservissement en position, renvoie une consigne de vitesse
	//Calcul des spd angulaire
	consigneSpdAngle = PID_Angle.compute(da); //erreur = angle à corriger pour etre en direction du goal
	//Calcul des spd de distance
	consigneSpdDistance = PID_Distance.compute(dd); //erreur = distance au goal

	consigneSpdR = consigneSpdDistance + consigneSpdAngle; //On additionne les deux speed pour avoir une trajectoire curviligne
	consigneSpdL = consigneSpdDistance - consigneSpdAngle; //On additionne les deux speed pour avoir une trajectoire curviligne

/*
	checkSpd(consigneSpdR, last_consigneSpdR);
	checkSpd(consigneSpdL, last_consigneSpdL);

	//Asservissement en vitesse
	consignePwmR = PID_SpdR.compute(consigneSpdR - current_spd.R); 
	consignePwmL = PID_SpdL.compute(consigneSpdL - current_spd.L); 
*/
	consignePwmR = consigneSpdR;
	consignePwmL = consigneSpdL;
	
	overflowPwm = setPwms(consignePwmR, consignePwmL);
/*
	last_consigneSpdR = consigneSpdR;
	last_consigneSpdL = consigneSpdL;
*/
	if(overflowPwm)
		return PWM_OVERFLOW;
	else
		return NO_OVERFLOW;
}

int Control::controlSpd(double goal_spdL, double goal_spdR)
{
	spd current_spd = robot.getMmSpdMotor();
	double consignePwmR, consignePwmL;
	bool overflowPwm = false;

	//Asservissement en vitesse
	consignePwmR = PID_SpdR.compute(goal_spdR - current_spd.R); 
	consignePwmL = PID_SpdL.compute(goal_spdL - current_spd.L); 

	overflowPwm = setPwms(consignePwmR, consignePwmL);

	if(overflowPwm)
		return PWM_OVERFLOW;
	else
		return NO_OVERFLOW;
}

void Control::applyPwm(){
	set_pwm_left(value_pwm_left);
	set_pwm_right(value_pwm_right);
}

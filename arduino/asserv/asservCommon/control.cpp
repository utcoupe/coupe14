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
	setPwmMin(PWM_MIN);
	max_angle = MAX_ANGLE;
	setMaxPwm(PWM_MAX);
	setMaxAcc(ACC_MAX);

	value_pwm_right = 0;
	value_pwm_left = 0;
}

int Control::compute(){
	static bool reset = true, order_started = false;
	static long start_time;
	int overflow = NO_OVERFLOW;
	struct goal current_goal = fifo.getCurrentGoal();
	m_pos current_pos = robot.getMmPos();
	long now = timeMicros();
	robot.update();

	if(fifo.isPaused() || current_goal.type == NO_GOAL){
		value_pwm_right = 0;
		value_pwm_left = 0;
	}
	else{
		if(current_goal.isReached){//Si le but est atteint et que ce n'est pas le dernier, on passe au suivant
			PDEBUGLN("Next Goal");
			current_goal = fifo.gotoNext();
			reset = true;
		}

		if(reset){//permet de reset des variables entre les goals
			PID_Angle.reset();
			PID_Distance.reset();
			reset = false;
			order_started = false;
		}
	
	/* Choix de l'action en fonction du type d'objectif */
		switch(current_goal.type){
			case TYPE_ANG :
			{
				double da = current_goal.data_1 - current_pos.angle;
				if(abs(da) < ERROR_ANGLE && value_pwm_left == 0 && value_pwm_right == 0)
					fifo.pushIsReached();
				else
					overflow = controlAngle(da);
#ifdef DEBUG
				static int counter = 0;
				counter++;
				if(counter > 100){
					counter = 0;
					Serial.println(da);
					Serial.print(value_pwm_left);Serial.println(value_pwm_right);
				}
#endif
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
					overflow = setPwms(current_goal.data_1,current_goal.data_2);
				}
				else{
					overflow = setPwms(0,0);
					fifo.pushIsReached();
				}
				break;
			}
			default:
			{
				PDEBUGLN("No Goal");
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

void Control::setPwmMin(int n_pwm_min){
	pwm_min = n_pwm_min;
}

void Control::setMaxAngCurv(double n_max_ang){
	max_angle = n_max_ang;
}

void Control::setMaxPwm(double n_max_pwm){
	max_pwm = n_max_pwm;
}

void Control::setMaxAcc(double n_max_acc){
	max_acc = n_max_acc;
}

void Control::pushPos(m_pos n_pos){
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

m_pos Control::getPos(){
	return robot.getMmPos();
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

int Control::setPwms(int pwm_left, int pwm_right){
	bool overflowPwm = NO_OVERFLOW;
	//Ajout des pwm minimale : "shift" des pwm
	if(pwm_min != 0){
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
	if(pwm_right > max_pwm){
		overflowPwm = PWM_OVERFLOW;
		pwm_right = max_pwm;
	}
	else if(pwm_right < -max_pwm){
		overflowPwm = PWM_OVERFLOW;
		pwm_right = -max_pwm;
	}
	if(pwm_left > max_pwm){
		overflowPwm = PWM_OVERFLOW;
		pwm_left = max_pwm;
	}
	else if(pwm_left < -max_pwm){
		overflowPwm = PWM_OVERFLOW;
		pwm_left = -max_pwm;
	}
	value_pwm_right = pwm_right;
	value_pwm_left = pwm_left;

	return overflowPwm;
}

void Control::check(double *consigne, double last)
{
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
	double consigne;
	static double last_consigne = 0;
	int consignePwmL, consignePwmR;
	bool overflowPwm = false;

	//Asservissement en position, renvoie une consigne de vitesse
	consigne = PID_Angle.compute(da);

	check(&consigne, last_consigne);
		
	consignePwmR = consigne;
	consignePwmL = -consigne;

	overflowPwm = setPwms(consignePwmL, consignePwmR);
	last_consigne = consigne;

	return overflowPwm;
}

int Control::controlPos(double da, double dd)
{
	double consigneAngle, consigneDistance, consigneR, consigneL;
	static double last_consigneL = 0, last_consigneR = 0;
	bool overflowPwm = NO_OVERFLOW;

	//Asservissement en position, renvoie une consigne de vitesse
	//Calcul des spd angulaire
	consigneAngle = PID_Angle.compute(da); //erreur = angle à corriger pour etre en direction du goal
	//Calcul des spd de distance
	consigneDistance = PID_Distance.compute(dd); //erreur = distance au goal

	consigneR = consigneDistance + consigneAngle; //On additionne les deux speed pour avoir une trajectoire curviligne
	consigneL = consigneDistance - consigneAngle; //On additionne les deux speed pour avoir une trajectoire curviligne

	check(&consigneR, last_consigneR);
	check(&consigneL, last_consigneL);

	overflowPwm = setPwms(consigneL, consigneR);

	last_consigneR = consigneR;
	last_consigneL = consigneL;

	return overflowPwm;
}

void Control::applyPwm(){
	set_pwm_left(value_pwm_left);
	set_pwm_right(value_pwm_right);
}

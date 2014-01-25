/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 29/11/13			*
 ****************************************/
#include "control.h"
#include "compat.h"
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
	setConsigneOffset(CONSIGNE_OFFSET);
	max_angle = MAX_ANGLE;
	setMaxAcc(ACC_MAX);

	value_consigne_right = 0;
	value_consigne_left = 0;
}

void Control::compute(){
	static bool reset = true, order_started = false;
	static long start_time;
	struct goal current_goal = fifo.getCurrentGoal();
	static struct goal last_goal = current_goal;
	m_pos current_pos = robot.getMmPos();
	long now = timeMicros();
	robot.update();

	if(fifo.isPaused() || current_goal.type == NO_GOAL){
		value_consigne_right = 0;
		value_consigne_left = 0;
	}
	else{
		if (current_goal.isReached && fifo.getRemainingGoals() > 1){//Si le but est atteint et que ce n'est pas le dernier, on passe au suivant
			//PDEBUGLN("Next Goal");
			current_goal = fifo.gotoNext();
			reset = true;
		}
		else if (last_goal.data_1 != current_goal.data_1 || last_goal.data_2 != current_goal.data_2 || last_goal.data_3 != current_goal.data_3) { //On a cancel un goal
			reset = true;
		}
		if (reset) {//permet de reset des variables entre les goals
			current_goal = fifo.getCurrentGoal();
			PID_Angle.reset();
			PID_Distance.reset();
			reset = false;
			order_started = false;
		}
	
	/* Choix de l'action en fonction du type d'objectif */
		switch(current_goal.type){
			case TYPE_ANG :
			{
				//float da = current_goal.data_1 - current_pos.angle;
				float da = moduloTwoPI(current_goal.data_1 - current_pos.angle);
				if(abs(da) <= ERROR_ANGLE){
					setConsigne(0, 0);
					fifo.pushIsReached();
				}
				else
					controlAngle(da);
				break;
			}

			case TYPE_POS :
			{
				float dx = current_goal.data_1 - current_pos.x;
				float dy = current_goal.data_2 - current_pos.y;
				float goal_a = atan2(dy, dx);
				float da = moduloTwoPI(goal_a - current_pos.angle);
				float dd = sqrt(pow(dx, 2.0)+pow(dy, 2.0));//erreur en distance
				float d = dd * cos(da);
				static char aligne = 0;

				da = moduloPI(da);

				if (!order_started) {
					if(abs(da) < max_angle) {
						aligne = 1;
					}
					else {
						aligne = 0;
					}
					order_started = true;
				}
				if(!aligne && abs(da) <= ERROR_ANGLE) {
					aligne = 1;
				}

				if(!aligne) {//On tourne sur place avant de se déplacer
					controlPos(da, 0);
				}
				else {
					controlPos(da, d + current_goal.data_3);//erreur en dist = dist au point + dist additionelle
				}

				if(abs(dd) <= ERROR_POS) {
					setConsigne(0, 0);
					fifo.pushIsReached();
				}
				break;
			}

			case TYPE_PWM :
			{
				if(!order_started){
					start_time = now;
					order_started = true;
				}
				if((now - start_time)/1000.0 <= current_goal.data_3){
					setConsigne(current_goal.data_1,current_goal.data_2);
				}
				else{
					setConsigne(0,0);
					fifo.pushIsReached();
				}
				break;
			}
			default:
			{
				//PDEBUGLN("No Goal");
				break;
			}	
		}
	}

	applyPwm();
	last_goal = current_goal;
}

void Control::update_robot_state(){
	robot.update();
}

void Control::reset(){
	value_consigne_left = 0;
	value_consigne_right = 0;
	fifo.clearGoals();
	robot.reset();
	applyPwm();
}


void Control::setPID_angle(float n_P, float n_I, float n_D){
	PID_Angle.setPID(n_P, n_I / FREQ, n_D * FREQ);
}

void Control::setPID_distance(float n_P, float n_I, float n_D){
	PID_Distance.setPID(n_P, n_I / FREQ, n_D * FREQ);
}

void Control::setConsigneOffset(int n_offset){
	consigne_offset = n_offset;
}

void Control::setMaxAngCurv(float n_max_ang){
	max_angle = n_max_ang;
}

void Control::setMaxAcc(float n_max_acc){
	PDEBUGLN("");
	PDEBUGLN(FREQ);
	PDEBUGLN(n_max_acc);
	PDEBUGLN(max_acc);
	max_acc = n_max_acc / FREQ; 
	PDEBUGLN(max_acc);
}

void Control::pushPos(m_pos n_pos){
	robot.pushMmPos(n_pos);
}

int Control::pushGoal(int ID, int p_type, float p_data_1, float p_data_2, float p_data_3){
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

void Control::setConsigne(float consigne_left, float consigne_right){
	//Ajout des pwm minimale : "shift" des pwm
	if(consigne_offset != 0){
		if(consigne_right > 0)
			consigne_right += consigne_offset;
		else if(consigne_right < 0)
			consigne_right -= consigne_offset;
		if(consigne_left > 0)
			consigne_left += consigne_offset;
		else if(consigne_left < 0)
			consigne_left -= consigne_offset;
	}

	//Tests d'overflow
	check_max(&consigne_left);
	check_max(&consigne_right);
	
	value_consigne_right = (int)consigne_right;
	value_consigne_left = (int)consigne_left;
}

void Control::check_max(float *consigne) {
	if(*consigne > CONSIGNE_RANGE_MAX)
		*consigne = CONSIGNE_RANGE_MAX;
	else if(*consigne < CONSIGNE_RANGE_MIN)
		*consigne = CONSIGNE_RANGE_MIN;
}

void Control::check_acc(float *consigne, float last)
{
	//Check MAX_ACC
	if(*consigne > last + max_acc){
		*consigne = last + max_acc;
	}
	else if(*consigne < last - max_acc){
		*consigne = last - max_acc;
	}
}

void Control::controlAngle(float da)
{
	float consigne;
	static float last_consigne = 0;
	int consignePwmL, consignePwmR;

	//Asservissement en position, renvoie une consigne de vitesse
	consigne = PID_Angle.compute(da);

	check_acc(&consigne, last_consigne);

	consignePwmR = consigne;
	consignePwmL = -consigne;

	setConsigne(consignePwmL, consignePwmR);
	last_consigne = consigne;
}

void Control::controlPos(float da, float dd)
{
	float consigneAngle, consigneDistance, consigneR, consigneL;
	static float last_consigneL = 0, last_consigneR = 0;

	//Asservissement en position, renvoie une consigne de vitesse
	//Calcul des spd angulaire
	consigneAngle = PID_Angle.compute(da); //erreur = angle à corriger pour etre en direction du goal
	//Calcul des spd de distance
	consigneDistance = PID_Distance.compute(dd); //erreur = distance au goal

	check_max(&consigneAngle);
	check_max(&consigneDistance);

	consigneR = consigneDistance + consigneAngle; //On additionne les deux speed pour avoir une trajectoire curviligne
	consigneL = consigneDistance - consigneAngle; //On additionne les deux speed pour avoir une trajectoire curviligne

	check_acc(&consigneR, last_consigneR);
	check_acc(&consigneL, last_consigneL);

	setConsigne(consigneL, consigneR);

	last_consigneR = consigneR;
	last_consigneL = consigneL;
}

void Control::applyPwm(){
	set_pwm_left(value_consigne_left);
	set_pwm_right(value_consigne_right);
}

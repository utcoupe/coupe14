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
	setErrorUseI_angle(ANG_AWU);
	setErrorUseI_distance(DIS_AWU);
	max_angle = MAX_ANGLE;
	setMaxAcc(ACC_MAX);
	setMaxRotSpdRatio(RATIO_SPD_ROT_MAX);

	value_consigne_right = 0;
	value_consigne_left = 0;
	last_finished_id = 0;
}

void Control::compute(){
	static bool reset = true, order_started = false;
	static long start_time;
	struct goal current_goal = fifo.getCurrentGoal();
	static struct goal last_goal = current_goal;
	pos current_pos = robot.getMmPos();
	long now = timeMicros();
	robot.update();

	if(fifo.isPaused() || current_goal.type == NO_GOAL){
		value_consigne_right = 0;
		value_consigne_left = 0;
	}
	else{
		if (current_goal.isReached) {
			last_finished_id = current_goal.ID;
			if (fifo.getRemainingGoals() > 1){//Si le but est atteint et que ce n'est pas le dernier, on passe au suivant
				current_goal = fifo.gotoNext();
				reset = true;
			}
		}
		else if (last_goal.type != current_goal.type || last_goal.data_1 != current_goal.data_1 || last_goal.data_2 != current_goal.data_2 || last_goal.data_3 != current_goal.data_3) { //On a cancel un goal
			reset = true;
		}
		if (reset) {//permet de reset des variables entre les goals
			current_goal = fifo.getCurrentGoal();
			PID_Angle.reset();
			PID_Distance.reset();
			robot.clearBlocked();
			reset = false;
			order_started = false;
		}
	
	/* Choix de l'action en fonction du type d'objectif */
		switch(current_goal.type){
			case TYPE_ANG :
			{
				float da = (current_goal.data_1 - current_pos.angle);
				
				da = moduloPI(da);//Commenter pour multi-tour

				if(abs(da) <= ERROR_ANGLE){
					setConsigne(0, 0);
					fifo.pushIsReached();
				}
				else
					controlPos(da,0);
				break;
			}

			case TYPE_POS :
			{
				float dx = current_goal.data_1 - current_pos.x;
				float dy = current_goal.data_2 - current_pos.y;
				float goal_a = atan2(dy, dx);
				float da = (goal_a - current_pos.angle);
				float dd = sqrt(pow(dx, 2.0)+pow(dy, 2.0));//erreur en distance
				float d = dd * cos(da); //Distance opposée
				float dop = dd * sin(da); //Distance adjacente
				static char aligne = 0;

				//Commenter pour multi-tour
				da = moduloPI(da);

				if (dop < ERROR_POS && dd < D_MIN_ASSERV_ANGLE) { //"Zone" de précision TODO
					da = 0;
				}

				//Init ordre
				if (!order_started) {
					if(abs(da) < max_angle) {
						aligne = 1;
					}
					else {
						aligne = 0;
					}
					order_started = true;
				}

				//Fin de la procedure d'alignement
				if(!aligne && abs(da) <= ERROR_ANGLE) {// && value_consigne_right < CONSIGNE_REACHED && value_consigne_left < CONSIGNE_REACHED) {
					aligne = 1;
				}

				//En cours d'alignement
				if(!aligne) {//On tourne sur place avant de se déplacer
					controlPos(da, 0);
				}
				//En cours de déplacement
				else {
					controlPos(da, d + current_goal.data_3);//erreur en dist = dist au point + dist additionelle
				}

				//Fin de consigne
				if(abs(dd) <= ERROR_POS) {// && value_consigne_right < CONSIGNE_REACHED && value_consigne_left < CONSIGNE_REACHED) {
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

void Control::setErrorUseI_angle(float I){
	PID_Angle.setErrorUseI(I);
}

void Control::setErrorUseI_distance(float I){
	PID_Distance.setErrorUseI(I);
}

void Control::setPID_angle(float n_P, float n_I, float n_D){
	PID_Angle.setPID(n_P, n_I / FREQ, n_D * FREQ);
}

void Control::setPID_distance(float n_P, float n_I, float n_D){
	PID_Distance.setPID(n_P, n_I / FREQ, n_D * FREQ);
}

void Control::setMaxAngCurv(float n_max_ang){
	max_angle = n_max_ang;
}

void Control::setMaxAcc(float n_max_acc){
	max_acc = n_max_acc / FREQ; 
}

void Control::setMaxRotSpdRatio(float n_max_rot_spd){
	max_rot_spd_ratio = n_max_rot_spd;
}

void Control::pushPos(pos n_pos){
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

pos Control::getPos(){
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
	//Tests d'overflow
	check_max(&consigne_left);
	check_max(&consigne_right);
	
	value_consigne_right = (int)consigne_right;
	value_consigne_left = (int)consigne_left;
}

void Control::check_max(float *consigne, float max) {
	if(*consigne > max)
		*consigne = max;
	else if(*consigne < -max)
		*consigne = -max;
}

void Control::check_acc(float *consigneL, float *consigneR)
{
	static float lastL = *consigneL, lastR = *consigneR;


	//Check MAX ROT SPD
	float rot = abs((*consigneR - *consigneL) / 2.0);
	//Ratio consigne/max
	float r = rot / CONSIGNE_RANGE_MAX;
	if (r > 1) { //Trop rapide
		*consigneL /= r;
		*consigneR /= r;
	} 


	//Check MAX_ACC
	//On verifie l'acceleration de chaque moteur
	//SI elle est trop élevée, on la baisse, et on
	//baisse aussi celle de l'autre moteur proportionellement
	if(*consigneL > lastL + max_acc){
		float diff = *consigneL - (lastL + max_acc);
		*consigneL -= diff;
		*consigneR -= diff * (*consigneR / * consigneL);
	}
	else if(*consigneL < lastL - max_acc){
		float diff = (lastL - max_acc) - *consigneL;
		*consigneL += diff;
		*consigneR += diff * (*consigneR / * consigneL);
	}
	if(*consigneR > lastR + max_acc){
		float diff = *consigneR - (lastR + max_acc);
		*consigneR -= diff;
		*consigneL -= diff * (*consigneL / * consigneR);
	}
	else if(*consigneR < lastR - max_acc){
		float diff = (lastR - max_acc) - *consigneR;
		*consigneR += diff;
		*consigneL += diff * (*consigneL / * consigneR);
	}

	lastR = *consigneR; lastL = *consigneL;
}

void Control::controlPos(float da, float dd)
{
	float consigneAngle, consigneDistance, consigneR, consigneL;
	//Asservissement en position, renvoie une consigne de vitesse
	//Calcul des spd angulaire
	consigneAngle = PID_Angle.compute(da); //erreur = angle à corriger pour etre en direction du goal
	//Calcul des spd de distance
	consigneDistance = PID_Distance.compute(dd); //erreur = distance au goal

	check_max(&consigneAngle);
	check_max(&consigneDistance, CONSIGNE_MAX - abs(consigneAngle));

	consigneR = consigneDistance + consigneAngle; //On additionne les deux speed pour avoir une trajectoire curviligne
	consigneL = consigneDistance - consigneAngle; //On additionne les deux speed pour avoir une trajectoire curviligne

	check_acc(&consigneL, &consigneR);

	setConsigne(consigneL, consigneR);
}

void Control::applyPwm(){
	set_pwm_left(value_consigne_left);
	set_pwm_right(value_consigne_right);
}

int Control::getLastFinishedId() {
	return last_finished_id;
}

void Control::resetLastFinishedId() {
	last_finished_id = 0;
}

/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#ifndef CONTROL_H
#define CONTROL_H

#include "encoder.h"
#include "robotstate.h"
#include "goals.h"
#include "PID.h"

#define PWM_OVERFLOW 1
#define NO_OVERFLOW 0

class Control{
	public:
	//Constructeur sans argument, utilise les #define
	Control();

	//compute : update le robot_state puis compute l'asserv
	int compute();

	//update_robot_state : permet d'update la robot state sans compute l'asserv
	void update_robot_state();

	void reset();

	//set des differents PIDs
	void setPID_angle(double n_P, double n_I, double n_D); //PID de l'asservissement angulaire
	void setPID_distance(double n_P, double n_I, double n_D); //PID de l'asservissement en position
	void setPID_speed(double n_P, double n_I, double n_D); //PID de l'asserv vitesse
	
	//gestion de la pwm_mini. Attention, il faut modifier les PIDs !
	void setPwmMin(int n_pwm_min); //Pwm minimale
	void setMaxAngCurv(double n_max_ang);
	void setMaxSpd(double n_max_spd);
	void setMaxAcc(double n_max_acc);

	//Push un goal
	int pushGoal(int ID, int p_type, double p_data_1 = 0, double p_data_2 = 0, double p_data_3 = 0);
	void nextGoal(); //va au goal suivant
	void clearGoals();

	//Toutes les positions sont renvoyée en mm, toutes les vitess en mm/ms = m/s
	void pushPos(pos n_pos); 
	pos getPos();
	spd getMotorSpd();
	spd getEncoderSpd();

	//Renvoie les valeurs des codeur (utile pour debug)
	Encoder* getLenc();
	Encoder* getRenc();

	//Permet la gestion de la pause
	void pause();
	void resume();

	private:
	RobotState robot;
	Fifo fifo;
	PID PID_Angle;
	PID PID_Distance;
	PID PID_SpdL;
	PID PID_SpdR;
	//interface avec les PIDs
	int setPwms(int pwm_right, int pwm_left, bool enable_pwm_min = true); //controles puis modification (renvoie l'overflow)
	void checkSpd(double *consigne, double last);
	int controlAngle(double goal_angle); //goal en radians
	int controlPos(double e_angle, double e_dist); //goal en mm
	int controlSpd(double goal_spdL, double goal_spdR);

	void applyPwm();

	int pwm_min;
	double max_angle;

	double max_spd;
	double max_acc;

	//Les pwm à appliquer
	int value_pwm_right, value_pwm_left;
};
#endif

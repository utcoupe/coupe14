/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 29/11/13			*
 ****************************************/
#ifndef CONTROL_H
#define CONTROL_H

#include "encoder.h"
#include "robotstate.h"
#include "goals.h"
#include "PID.h"

class Control{
	public:
	//Constructeur sans argument, utilise les #define
	Control();

	//compute : update le robot_state puis compute l'asserv
	void compute();

	//update_robot_state : permet d'update la robot state sans compute l'asserv
	void update_robot_state();

	void reset();

	//set des differents PIDs
	void setPID_angle(double n_P, double n_I, double n_D); //PID de l'asservissement angulaire
	void setPID_distance(double n_P, double n_I, double n_D); //PID de l'asservissement en position
	
	//gestion de l'offset. Attention, il faut modifier les PIDs !
	void setConsigneOffset(int n_offset);
	void setMaxAngCurv(double n_max_ang);
	void setMaxAcc(double n_max_acc);

	//Push un goal
	int pushGoal(int ID, int p_type, double p_data_1 = 0, double p_data_2 = 0, double p_data_3 = 0);
	void nextGoal(); //va au goal suivant
	void clearGoals();

	//Toutes les positions sont renvoyée en mm, toutes les vitess en mm/ms = m/s
	void pushPos(m_pos n_pos); 
	m_pos getPos();

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
	//interface avec les PIDs
	void setConsigne(int consigne_left, int consigne_right); //controles puis modification (renvoie l'overflow)
	void check(double *consigne, double last);
	void controlAngle(double goal_angle); //goal en radians
	void controlPos(double e_angle, double e_dist); //goal en mm

	void applyPwm();

	int consigne_offset;
	double max_angle;

	double max_acc;

	//Les pwm à appliquer
	int value_consigne_right, value_consigne_left;
};
#endif

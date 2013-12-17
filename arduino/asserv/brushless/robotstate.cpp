/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#include "robotstate.h"
#include "compaArduino.h"
#include "local_math.h"

/********************************************************
 * 							*
 * 		      CLASSE ROBOTSTATE			*
 *							*
 ********************************************************/
RobotState::RobotState():encoderLeft(LEFT_SIDE), encoderRight(RIGHT_SIDE)
{
	RobotState::reset();
}

void RobotState::reset(){
	current_pos.x = 0;
	current_pos.y = 0;
	current_pos.angle = 0;
	current_pos.rangle = 0;
	encoderRight.reset();
	encoderLeft.reset();
	last_ticksR = encoderRight.getTicks();
	last_ticksL = encoderLeft.getTicks();
}

m_pos RobotState::getMmPos(){
	m_pos mm_pos;
	mm_pos.angle = current_pos.angle;
	mm_pos.x = current_pos.x * ENC_TICKS_TO_MM / FIXED_POINT_PRECISION;
	mm_pos.y = current_pos.y * ENC_TICKS_TO_MM / FIXED_POINT_PRECISION;
	return mm_pos;
}

Encoder* RobotState::getRenc(){
	return &encoderRight;
}

Encoder* RobotState::getLenc(){
	return &encoderLeft;
}

void RobotState::pushMmPos(m_pos n_pos){
	current_pos.x = n_pos.x * ENC_MM_TO_TICKS * FIXED_POINT_PRECISION;
	current_pos.y = n_pos.y * ENC_MM_TO_TICKS * FIXED_POINT_PRECISION;
	current_pos.angle = n_pos.angle;
}

void RobotState::update(){
	long ticksR = encoderRight.getTicks();
	long ticksL = encoderLeft.getTicks();
	int dl = (ticksL - last_ticksL)*FIXED_POINT_PRECISION;
	int dr = (ticksR - last_ticksR)*FIXED_POINT_PRECISION;

	float d_angle = tan((dr - dl)/(ENTRAXE_ENC * ENC_MM_TO_TICKS * FIXED_POINT_PRECISION)); //sans approximation tan
	current_pos.angle = current_pos.angle + d_angle;
	current_pos.rangle = moduloTwoPI(current_pos.rangle + d_angle);

	current_pos.x = current_pos.x + round(((dr + dl)/2.0)*cos(current_pos.angle));
	current_pos.y = current_pos.y + round(((dr + dl)/2.0)*sin(current_pos.angle));

	//prepare la prochaine update
	last_ticksR = ticksR;
	last_ticksL = ticksL;
}

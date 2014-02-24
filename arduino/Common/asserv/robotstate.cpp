/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#include "robotstate.h"
#include "compat.h"
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
	current_pos.modulo_angle = 0;
	encoderRight.reset();
	encoderLeft.reset();
	last_ticksR = encoderRight.getTicks();
	last_ticksL = encoderLeft.getTicks();
}

pos RobotState::getMmPos(){
	pos mm_pos;
	mm_pos.angle = current_pos.angle + 2*M_PI*current_pos.modulo_angle;
	mm_pos.x = current_pos.x / FIXED_POINT_PRECISION;
	mm_pos.y = current_pos.y / FIXED_POINT_PRECISION;
	return mm_pos;
}

Encoder* RobotState::getRenc(){
	return &encoderRight;
}

Encoder* RobotState::getLenc(){
	return &encoderLeft;
}

void RobotState::pushMmPos(pos n_pos){
	current_pos.x = n_pos.x * FIXED_POINT_PRECISION;
	current_pos.y = n_pos.y * FIXED_POINT_PRECISION;
	current_pos.angle = n_pos.angle;
}

void RobotState::update(){
	long ticksR = encoderRight.getTicks();
	long ticksL = encoderLeft.getTicks();
	float dl = (ticksL - last_ticksL)*TICKS_TO_MM_LEFT;
	float dr = (ticksR - last_ticksR)*TICKS_TO_MM_RIGHT;

	float d_angle = atan2(dr - dl, ENTRAXE_ENC); //sans approximation tan
	current_pos.angle += d_angle;
	if (current_pos.angle > M_PI) {
		current_pos.angle -= 2.0*M_PI;
		current_pos.modulo_angle++;
	}
	else if (current_pos.angle <= -M_PI) {
		current_pos.angle += 2.0*M_PI;
		current_pos.modulo_angle--;
	}

	static float last_angle = current_pos.angle; 
	dl *= FIXED_POINT_PRECISION;
	dr *= FIXED_POINT_PRECISION;

	current_pos.x += round(((dr + dl)/2.0)*cos((current_pos.angle + last_angle)/2.0));
	current_pos.y += round(((dr + dl)/2.0)*sin((current_pos.angle + last_angle)/2.0));

	//prepare la prochaine update
	last_ticksR = ticksR;
	last_ticksL = ticksL;
	last_angle = current_pos.angle;
}

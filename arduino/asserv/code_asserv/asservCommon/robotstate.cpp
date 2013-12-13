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
	spd_encoder.R = 0;
	spd_encoder.L = 0;
	spd_motor.R = 0;
	spd_motor.L = 0;
	encoderRight.reset();
	encoderLeft.reset();
	last_ticksR_spd = last_ticksR = encoderRight.getTicks();
	last_ticksL_spd = last_ticksL = encoderLeft.getTicks();
}

pos RobotState::getMmPos(){
	pos mm_pos = current_pos;
	mm_pos.x = mm_pos.x * ENC_TICKS_TO_MM / FIXED_POINT_PRECISION;
	mm_pos.y = mm_pos.y * ENC_TICKS_TO_MM / FIXED_POINT_PRECISION;
	return mm_pos;
}

spd RobotState::getMmSpdMotor(){
	spd mm_spd_motor;
	mm_spd_motor.R = spd_motor.R * ENC_TICKS_TO_MM / FIXED_POINT_PRECISION;
	mm_spd_motor.L = spd_motor.L * ENC_TICKS_TO_MM / FIXED_POINT_PRECISION;
	return mm_spd_motor;
}

spd RobotState::getMmSpdEncoder(){
	spd mm_spd_encoder;
	mm_spd_encoder.R = spd_encoder.R * (double)ENC_TICKS_TO_MM / (double)FIXED_POINT_PRECISION;
	mm_spd_encoder.L = spd_encoder.L * (double)ENC_TICKS_TO_MM / (double)FIXED_POINT_PRECISION;
	return mm_spd_encoder;
}

Encoder* RobotState::getRenc(){
	return &encoderRight;
}

Encoder* RobotState::getLenc(){
	return &encoderLeft;
}

void RobotState::pushMmPos(pos n_pos){
	current_pos.x = n_pos.x * ENC_MM_TO_TICKS * FIXED_POINT_PRECISION;
	current_pos.y = n_pos.y * ENC_MM_TO_TICKS * FIXED_POINT_PRECISION;
	current_pos.angle = n_pos.angle;
}

void RobotState::update(){
	unsigned long now = timeMicros();
	static int sous_echantillon = 0;
	static long last_speed_sample = now;
	long ticksR = encoderRight.getTicks();
	long ticksL = encoderLeft.getTicks();
	int dl = (ticksL - last_ticksL)*FIXED_POINT_PRECISION;
	int dr = (ticksR - last_ticksR)*FIXED_POINT_PRECISION;

	
	//calcul des vitesses en (ticks/ms)*FIXED_POINT_PRECISION
	sous_echantillon++;
	if(sous_echantillon >= SOUS_ECHANTILLONAGE_VITESSE){
		long dt = now - last_speed_sample;
		int dls = (ticksL - last_ticksL_spd)* FIXED_POINT_PRECISION;
		int drs = (ticksR - last_ticksR_spd) * FIXED_POINT_PRECISION;
		spd_encoder.R = (double)(drs*1000.0/dt);
		spd_encoder.L = (double)(dls*1000.0/dt);

		// SPD_ENCODER : (FIXED_POINT_PRECISION*ticks)/(DUREE_CYCLE*SOUS_ECHANTILLONAGE_VITESSE)
	
		//On s'amuse un peu avec la géométrie
		//TODO : Geometrie des deux lignes suivantes
		spd_motor.R = spd_encoder.R;
		spd_motor.L = spd_encoder.L;

		sous_echantillon = 0;
		last_speed_sample = now;
		last_ticksR_spd = ticksR;
		last_ticksL_spd = ticksL;
	}

	current_pos.angle = current_pos.angle + tan((dr - dl)/(ENTRAXE_ENC * ENC_MM_TO_TICKS * FIXED_POINT_PRECISION)); //sans approximation tan

	current_pos.x = current_pos.x + round(((dr + dl)/2.0)*cos(current_pos.angle));
	current_pos.y = current_pos.y + round(((dr + dl)/2.0)*sin(current_pos.angle));

	//prepare la prochaine update
	last_ticksR = ticksR;
	last_ticksL = ticksL;
}

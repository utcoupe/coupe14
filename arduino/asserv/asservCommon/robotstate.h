/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#ifndef ROBOTSTATE_H
#define ROBOTSTATE_H

#include "parameters.h"
#include "encoder.h"
#include <math.h>

const double ENC_TICKS_TO_MM = (2.0*M_PI*(ENC_RADIUS))/(TICKS_PER_TURN);// = mm/ticks
const double ENC_MM_TO_TICKS = (TICKS_PER_TURN)/(2.0*M_PI*(ENC_RADIUS)); // = ticks/mm

double moduloTwoPI(double angle);

typedef struct pos pos;
struct pos{
	long x;
	long y;
	double angle;
};


typedef struct spd spd;
struct spd{
	double R;
	double L;
};

class RobotState{
	public:
	RobotState();//Constructeur
	void reset();
	pos getMmPos();
	spd getMmSpdEncoder();
	spd getMmSpdMotor();
	Encoder* getRenc();
	Encoder* getLenc();
	void pushMmPos(pos n_pos);
	void update();

	private:
	Encoder encoderLeft;
	Encoder encoderRight;
	pos current_pos;
	spd spd_encoder, spd_motor; //conservées en ticks/ms
	long last_ticksR;
	long last_ticksL;
	long last_ticksL_spd, last_ticksR_spd;
};

#endif

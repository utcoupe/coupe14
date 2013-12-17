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

const float ENC_TICKS_TO_MM = (2.0*M_PI*(ENC_RADIUS))/(TICKS_PER_TURN);// = mm/ticks
const float ENC_MM_TO_TICKS = (TICKS_PER_TURN)/(2.0*M_PI*(ENC_RADIUS)); // = ticks/mm

typedef struct pos pos;
struct pos{
	long x;
	long y;
	float angle;
	float rangle;
};

typedef struct m_pos m_pos;
struct m_pos{
	float x;
	float y;
	float angle;
};

class RobotState{
	public:
	RobotState();//Constructeur
	void reset();
	m_pos getMmPos();
	Encoder* getRenc();
	Encoder* getLenc();
	void pushMmPos(m_pos n_pos);
	void update();

	private:
	Encoder encoderLeft;
	Encoder encoderRight;
	pos current_pos;
	long last_ticksR;
	long last_ticksL;
};

#endif

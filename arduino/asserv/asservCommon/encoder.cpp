/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#include "encoder.h"
#include "compaArduino.h"

/********************************************************
 * 							*
 * 		      CLASSE ENCODER			*
 *							*
 ********************************************************/
Encoder::Encoder(int p_side){
	side = p_side;
	Encoder::reset();
}

long Encoder::getTicks(){
	return ticks;
}

void Encoder::reset(){
	ticks = 0;
	signal_0_init = false;
	ticks_error = 0;
	if(side == LEFT_SIDE){
		last_value_A = digitalRead(PIN_ENC_LEFT_A);
		last_value_B = digitalRead(PIN_ENC_LEFT_B);
	}
	else{
		last_value_A = digitalRead(PIN_ENC_RIGHT_A);
		last_value_B = digitalRead(PIN_ENC_RIGHT_B);
	}
}

int Encoder::getError(){
	return ticks_error;
}

#if ENCODER_EVAL == 4
void Encoder::interruptA(){
	bool new_value;
	if(side == LEFT_SIDE){
		new_value = digitalRead(PIN_ENC_LEFT_A);
		if(new_value == 1)
			if(last_value_B == 1)
				ticks--;
			else
				ticks++;
	
		else
			if(last_value_B == 1)
				ticks++;
			else
				ticks--;
	}
	else{
		new_value = digitalRead(PIN_ENC_RIGHT_A);
		if(new_value == 1)
			if(last_value_B == 1)
				ticks++;
			else
				ticks--;

		else
			if(last_value_B == 1)
				ticks--;
			else
				ticks++;
	}

	last_value_A = new_value;
}

void Encoder::interruptB(){
	bool new_value;
	if(side == LEFT_SIDE){
		new_value = digitalRead(PIN_ENC_LEFT_B);
		if(new_value == 1)
			if(last_value_A == 1)
				ticks++;
			else
				ticks--;
	
		else
			if(last_value_A == 1)
				ticks--;
			else
				ticks++;
	}
	else{
		new_value = digitalRead(PIN_ENC_RIGHT_B);
		if(new_value == 1)
			if(last_value_A == 1)
				ticks--;
			else
				ticks++;
	
		else
			if(last_value_A == 1)
				ticks++;
			else
				ticks--;
	}

	last_value_B = new_value;
}
#elif ENCODER_EVAL == 2
void Encoder::interruptA(){
	bool new_value;
	if(side == LEFT_SIDE){
		new_value = digitalRead(PIN_ENC_LEFT_A);
		if(new_value == 1)
			if(digitalRead(PIN_ENC_LEFT_B) == 1)
				ticks--;
			else
				ticks++;
		else
			if(digitalRead(PIN_ENC_LEFT_B) == 1)
				ticks++;
			else
				ticks--;
	}
	else{
		new_value = digitalRead(PIN_ENC_RIGHT_A);
		if(new_value == 1)
			if(digitalRead(PIN_ENC_RIGHT_B) == 1)
				ticks++;
			else
				ticks--;
		else
			if(digitalRead(PIN_ENC_RIGHT_B) == 1)
				ticks--;
			else
				ticks++;
	}
}
#elif ENCODER_EVAL == 1
void Encoder::interruptA(){
	if(side == LEFT_SIDE)
		if(digitalRead(PIN_ENC_LEFT_B) == 1)
			ticks--;
		else
			ticks++;
	else
		if(digitalRead(PIN_ENC_RIGHT_B) == 1)
			ticks++;
		else
			ticks--;
}
#endif

void Encoder::interrupt0(){
	int diff;
	if(signal_0_init){
		diff = ticks - last_ticks_on_0;
		last_ticks_on_0 = ticks;
	}
	else{
		last_ticks_on_0 = ticks;
		signal_0_init = true;
		diff = 0;
	}
	if(diff > 0)
		diff = diff - TICKS_PER_TURN;
	else if (diff < 0)
		diff = diff + TICKS_PER_TURN;
	ticks_error = diff;
}


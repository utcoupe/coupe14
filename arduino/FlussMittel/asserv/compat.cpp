/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#include "compat.h"

extern Control control;

void initPins(){
	//set mode des pins pour arduino
	pinMode(PIN_ENC_LEFT_A,INPUT_PULLUP);
	pinMode(PIN_ENC_LEFT_B,INPUT_PULLUP);
	pinMode(PIN_ENC_LEFT_0,INPUT_PULLUP);
	pinMode(PIN_ENC_RIGHT_0,INPUT_PULLUP);
	pinMode(PIN_ENC_RIGHT_A,INPUT_PULLUP);
	pinMode(PIN_ENC_RIGHT_B,INPUT_PULLUP);

	//Definition des interruptions arduino en fonction du type d'évaluation
#if ENCODER_EVAL == 4
	attachInterrupt(INTERRUPT_ENC_LEFT_A,interruptLeftA,CHANGE);
	attachInterrupt(INTERRUPT_ENC_RIGHT_A,interruptRightA,CHANGE);
	attachInterrupt(INTERRUPT_ENC_LEFT_B,interruptLeftB,CHANGE);
	attachInterrupt(INTERRUPT_ENC_RIGHT_B,interruptRightB,CHANGE);
#elif ENCODER_EVAL == 2
	attachInterrupt(INTERRUPT_ENC_LEFT_A,interruptLeftA,CHANGE);
	attachInterrupt(INTERRUPT_ENC_RIGHT_A,interruptRightA,CHANGE);
#elif ENCODER_EVAL == 1
	attachInterrupt(INTERRUPT_ENC_LEFT_A,interruptLeftA,RISING);
	attachInterrupt(INTERRUPT_ENC_RIGHT_A,interruptRightA,RISING);
#endif

#if GESTION_3EME_FIL
	//Interruption du 3e fil des codeurs
	attachInterrupt(INTERRUPT_ENC_LEFT_0,interruptLeft0,RISING);
	attachInterrupt(INTERRUPT_ENC_RIGHT_0,interruptRight0,RISING);
#endif
}

unsigned long timeMillis(){
	return millis();
}
unsigned long timeMicros(){
	return micros();
}

//"hack" des interrupt arduino

void interruptLeftA(){
	control.getLenc()->interruptA();
}

void interruptRightA(){
	control.getRenc()->interruptA();
}

#if ENCODER_EVAL == 4
void interruptLeftB(){
	control.getLenc()->interruptB();
}

void interruptRightB(){
	control.getRenc()->interruptB();
}
#endif

#if GESTION_3EME_FIL
void interruptLeft0{
	control.getLenc()->interrupt0();
}

void interruptRight0{
	control.getRenc()->interrupt0();
}
#endif

char serial_read(){
	return Serial2.read();
}

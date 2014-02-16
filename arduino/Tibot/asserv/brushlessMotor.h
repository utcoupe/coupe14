//Adapted from Adafruit Motor Shield by Quentin C for UTCoupe
//Defined for brushless controler shield designed by UTCoupe
//08/04/2013

#ifndef BRUSHLESSMOTOR_H
#define BRUSHLESSMOTOR_H

#include "parameters.h"

#define MOTOR1_EN 28
#define MOTOR2_EN 24

#define MOTOR1_SPD 3
#define MOTOR2_SPD 2

#define MOTOR1_RDY 42
#define MOTOR2_RDY 36

#define MOTOR_LEFT 1
#define MOTOR_RIGHT 2

//Pins codeurs liés à la shield
#define PIN_ENC_RIGHT_A 18
#define PIN_ENC_RIGHT_B 19
#define PIN_ENC_RIGHT_0 2
#define PIN_ENC_LEFT_A 20
#define PIN_ENC_LEFT_B 21
#define PIN_ENC_LEFT_0 3

#define INTERRUPT_ENC_LEFT_A 5
#define INTERRUPT_ENC_LEFT_B 4
#define INTERRUPT_ENC_LEFT_0 0
#define INTERRUPT_ENC_RIGHT_A 3
#define INTERRUPT_ENC_RIGHT_B 2
#define INTERRUPT_ENC_RIGHT_0 1


class Motor
{
	public:
	Motor(int n_motor_side);
	void setPwm(int pwm);

	private:
	int motor_side;
};

#endif

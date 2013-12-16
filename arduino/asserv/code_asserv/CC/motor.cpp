/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 29/11/13			*
 ****************************************/
#include "motor.h"
#include "parameters.h"

//Controleur :
//-255:0 : Marche arrière
//0:255  : Marche avant

AF_DCMotor motor_left(1, MOTOR12_64KHZ);
AF_DCMotor motor_right(2, MOTOR12_64KHZ);

void set_pwm_left(int pwm){
	pwm = -pwm;//les moteurs sont faces à face, pour avancer il faut qu'il tournent dans un sens différent
	if(pwm > 255)
		pwm = 255;
	else if(pwm < -255)
		pwm = -255;

	if(pwm >= 0)
		motor_left.run(FORWARD);
	else
		motor_left.run(BACKWARD);

	motor_left.setSpeed(abs(pwm));
}

void set_pwm_right(int pwm){
	if(pwm > 255)
		pwm = 255;
	else if(pwm < -255)
		pwm = -255;

	if(pwm >= 0)
		motor_right.run(FORWARD);
	else
		motor_right.run(BACKWARD);
	
	motor_right.setSpeed(abs(pwm));
}

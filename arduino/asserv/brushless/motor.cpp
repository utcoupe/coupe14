/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 13/10/13			*
 ****************************************/
#include "motor.h"
#include "parameters.h"

Motor motor_left(MOTOR_LEFT);
Motor motor_right(MOTOR_RIGHT);

void set_pwm_left(int pwm){
	pwm = -pwm;//les moteurs sont faces à face, pour avancer il faut qu'il tournent dans un sens différent
	if(pwm > 255)
		pwm = 255;
	else if(pwm < -255)
		pwm = -255;

	if(pwm >= PWM_MIN){
		motor_left.run(FORWARD);
	}
	else if(pwm <= -PWM_MIN){
		motor_left.run(BACKWARD);
	}
	else
		pwm = 0;
	
	motor_left.setPwm(abs(pwm));
}

void set_pwm_right(int pwm){
	if(pwm > 255)
		pwm = 255;
	else if(pwm < -255)
		pwm = -255;

	if(pwm >= PWM_MIN){
		motor_right.run(FORWARD);
	}
	else if(pwm <= -PWM_MIN){ 
		motor_right.run(BACKWARD);
	}
	else
		pwm = 0;
	
	motor_right.setPwm(abs(pwm));
}

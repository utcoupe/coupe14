//Par Quentin pour UTCoupe2013 01/04/2013
//Commande de shield arduino brushless by UTCoupe

#include "include_arduino.h"

#include "brushlessMotor.h"


/******************************************
               MOTORS
******************************************/
/*********************************
DIG1 and DIG2 defined to 0 :
linear adjustment of the speed

might be configured to smth else in order use speed control
see datasheet of DEC-MODULE-24/2
***********************************/

Motor::Motor(int n_motor_side) {
	motor_side = n_motor_side;
	switch (motor_side) {
		case MOTOR_LEFT:{
		 	pinMode(MOTOR1_SPD, OUTPUT);

		 	pinMode(MOTOR1_EN, OUTPUT);
			digitalWrite(MOTOR1_EN, HIGH); //Enable motor

			pinMode(MOTOR1_RDY, INPUT);
			pinMode(MOTOR1_DIR, OUTPUT);
			digitalWrite(MOTOR1_DIR, LOW);
			break;
		}
		case MOTOR_RIGHT:{
			pinMode(MOTOR2_SPD, OUTPUT);

			pinMode(MOTOR2_EN, OUTPUT);
			digitalWrite(MOTOR2_EN,HIGH); //enable motor

			pinMode(MOTOR2_RDY, INPUT);
			pinMode(MOTOR2_DIR, OUTPUT);
			digitalWrite(MOTOR2_DIR, LOW);
		   	break;
		}
	}
}

void Motor::run(int cmd) {
	int dirPin;
	int enPin;
	switch (motor_side) {
		case MOTOR_LEFT:{
			dirPin = MOTOR1_DIR;
			enPin = MOTOR1_EN;
			break;
		}
		case MOTOR_RIGHT:{
			dirPin = MOTOR2_DIR;
			enPin = MOTOR2_EN;
			break;
		}
	}
  
	switch (cmd) {
		case FORWARD:{
			digitalWrite(dirPin, LOW);
			break;
		}
		case BACKWARD:{
			digitalWrite(dirPin, HIGH);
   			break;
		}
		case DISABLE:{
		   	digitalWrite(enPin, LOW);
    			break;
		}
		case ENABLE:{
		  	digitalWrite(enPin, HIGH);
			break;
		}
	}
}

void Motor::setPwm(int pwm) {
	switch (motor_side) {
		case MOTOR_LEFT:{
			analogWrite(MOTOR1_SPD, pwm);
		    	break;
		}
		case MOTOR_RIGHT:{
			analogWrite(MOTOR2_SPD, pwm);
			break;
		}
	}
}

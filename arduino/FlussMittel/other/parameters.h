#ifndef PARAMETERS_H
#define PARAMETERS_H

//////////////////////
//		PARAMETERS  //
//////////////////////

#define H_TO_STEP 16

#define HAUTEUR_MAX 133 //En mm
#define HAUTEUR_MIN 15 //en mm
#define LONGUEUR_MAX 70 
#define MARGE_SECU_TOP 40 //En steps

#define ANGLE_DIST_MAX_DEG 85
#define ANGLE_ANGLE_MAX_DEG 130

#define BRAS_OFFSET_DIST 0 //Distance in mm
#define BRAS_OFFSET_ANGLE 0 //Angle offset in degrees

#define MARGE_DEPOT 50

#define ANGLE_RET ((110/180)*M_PI)

#define ANGLE_DEPOT M_PI/2.0
#define LONGUEUR_DEPOT 5

#define ANGLE_DEPOT_RET ((130/180)*M_PI) 
#define LONGUEUR_DEPOT_RET 20

#define L1 43//Petit bras
#define L2 82//Grand bras
#define PERIOD_STEPPER 600
#define VMAX_STEPPER 600 
#define AMAX_STEPPER 10000

#define PWM_PUMP 255 

#define DELAY_REPLI_BRAS 1000000
#define DELAY_STOP_PUMP 500000
//////////////////////
//		PINS		//
//////////////////////
#define PIN_SERVO_RET 51

#define PIN_SERVO_BRAS_ANGLE 53
#define PIN_SERVO_BRAS_DIST 52

#define PIN_STEPPER_STEP 31
#define PIN_STEPPER_DIR 30
#define PIN_INTERRUPT_BRAS 20 //PULLUP ICI
#define INT_BRAS 3
#define PIN_INT_HAUT_ASC 21 //PULLUP
#define INT_ASC_HAUT 2

#define PIN_DEBUG_LED 23

//////////////////////
//		DEBUG		//
//////////////////////
#ifdef DEBUG
#define PDEBUG(x) Serial3.print(x)
#define PDEBUGLN(x) Serial3.println(x)
#define BINPR(x) Serial3.print(x, BIN)
#else
#define PDEBUG(x)
#define PDEBUGLN(x)
#define BINPR(x)
#endif


#define MIN(x,y) x<y?x:y
#define MAX(x,y) x>y?x:y
#define ABS(x) x<0?-x:x
#endif

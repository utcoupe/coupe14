#ifndef PARAMETERS_H
#define PARAMETERS_H

//////////////////////
//		PARAMETERS  //
//////////////////////

#define HAUTEUR_MAX 114//En mm

#define BRAS_OFFSET_DIST 0 //Distance in mm
#define BRAS_OFFSET_ANGLE 0 //Angle offset in degrees

#define MARGE_DEPOT 30

#define ANGLE_DEPOT M_PI/2.0
#define LONGUEUR_DEPOT 5

#define ANGLE_DEPOT_RET 2.27 // 130°
#define LONGUEUR_DEPOT_RET 20

#define L1 43//Petit bras
#define L2 82//Grand bras
#define H_TO_STEP 8
#define PERIOD_STEPPER 1000
#define VMAX_STEPPER 400
#define AMAX_STEPPER 800

//////////////////////
//		PINS		//
//////////////////////
#define PIN_SERVO_BRAS 8
#define PIN_SERVO_RET 9

#define PIN_SERVO_BRAS_ANGLE 2
#define PIN_SERVO_BRAS_DIST 3

#define PIN_STEPPER_STEP 31
#define PIN_STEPPER_DIR 30
#define PIN_INTERRUPT_BRAS 32 //PULLUP ICI
#define PIN_INT_HAUT_ASC 33 //PULLUP

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


#define MIN(x,y) x>y?x:y
#define MAX(x,y) x<y?x:y
#define ABS(x) x<0?-x:x
#endif

#ifndef PARAMETERS_H
#define PARAMETERS_H

//////////////////////
//		PARAMETERS  //
//////////////////////

#define HAUTEUR_MAX 150//En mm

#define BRAS_OFFSET_DIST 100 //Distance in mm
#define BRAS_OFFSET_ANGLE 10 //Angle offset in degrees
#define ANGLE_DEPOT 0
#define LONGUEUR_DEPOT 0

#define ANGLE_DEPOT_RET 0
#define LONGUEUR_DEPOT_RET 0
#define HAUTEUR_DEPOT_RET 0

#define L1 43//Petit bras
#define L2 82//Grand bras
#define H_TO_STEP 200
#define FREQUENCY_STEPPER 10
#define DELAY_STEPPER_CONTROLER 50

//////////////////////
//		PINS		//
//////////////////////
#define PIN_SERVO_BRAS 8
#define PIN_SERVO_RET 9

#define PIN_INT_HAUT_ASC 22
#define PIN_INT_BAS_ASC 23

#define PIN_SERVO_BRAS_ANGLE 2
#define PIN_SERVO_BRAS_DIST 3

#define PIN_STEPPER_STEP 31
#define PIN_STEPPER_DIR 30
#define PIN_INTERRUPT_BRAS 32 //PULLUP ICI

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

#endif

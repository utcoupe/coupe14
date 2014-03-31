#ifndef PARAMETERS_H
#define PARAMETERS_H

//////////////////////
//		PARAMETERS  //
//////////////////////

#define BRAS_OFFSET_DIST 100 //Distance in mm
#define BRAS_DIST_TO_ANGLE 0.01 //Conversion between the distance to move and the angle to give to the servo
#define BRAS_OFFSET_ANGLE 10 //Angle offset in degrees

//////////////////////
//		PINS		//
//////////////////////
#define PIN_SERVO_BRAS 8
#define PIN_SERVO_RET 9

#define PIN_INT_HAUT_ASC 22
#define PIN_INT_BAS_ASC 23

#define PIN_SERVO_BRAS_ANGLE 2
#define PIN_SERVO_BRAS_DIST 3

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

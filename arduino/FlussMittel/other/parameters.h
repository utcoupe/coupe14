#ifndef PARAMETERS_H
#define PARAMETERS_H

//////////////////////
//		PARAMETERS  //
//////////////////////

//DIMENSIONS

#define BRAS_OFFSET_DIST 145 //Distance in mm
#define BRAS_OFFSET_ANGLE 30 //Angle offset in degrees

#define HAUTEUR_MAX 128 //En mm
#define HAUTEUR_MIN 15 //en mm

#define X_BRAS 128
#define Y_BRAS 130

//SECU BRAS : en degree commande

#define ANGLE_DIST_MAX 85
#define ANGLE_ANGLE_MAX 130
#define ANGLE_INSIDE_ROBOT 70
#define SECU_DELAY_REPLI_BRAS 200 //ms
#define SECU_DELAY_ROT_BRAS 500 //ms

//BRAS

#define H_TO_STEP 16

#define LONGUEUR_MAX 215 
#define LONGUEUR_MIN BRAS_OFFSET_DIST
#define MARGE_SECU_TOP 40 //En steps

#define MARGE_DEPOT 80
#define MARGE_PREHENSION 40
#define HAUTEUR_GARDE_DEPOT HAUTEUR_MIN

#define ANGLE_DEPOT (-(110.0/180.0)*M_PI)
#define LONGUEUR_DEPOT 150

#define ANGLE_DEPOT_RET (-(140.0/180.0)*M_PI) 
#define LONGUEUR_DEPOT_RET 210

#define PERIOD_STEPPER 200
#define VMAX_STEPPER 600 
#define AMAX_STEPPER 10000

#define DELAY_SERVO_PUSH 500
#define DELAY_REPLI_BRAS 1000
#define DELAY_REPLI_BRAS2 100
#define DELAY_STOP_PUMP 500

//TRIANGLES BORDURES
#define HAUTEUR_TRI_BORDURE 70
#define LONGUEUR_TRI_BORDURE 200
#define ANGLE_REPLI_TRI (-(80/180.0)*M_PI) 
#define ANGLE_OUVERT 0 

//RETOURNEMENT
#define ANGLE_RET 70

//POMPE
#define PWM_PUMP 255

//////////////////////
//		PINS		//
//////////////////////
#define PIN_SERVO_RET 50

#define PIN_SERVO_BRAS_ANGLE 51
#define PIN_SERVO_BRAS_DIST 52

#define PIN_STEPPER_STEP 31
#define PIN_STEPPER_DIR 30
#define PIN_INTERRUPT_BRAS 20 //PULLUP ICI
#define INT_BRAS 3
#define PIN_INT_HAUT_ASC 21 //PULLUP
#define INT_ASC_HAUT 2

#define PIN_DEBUG_LED 23

#define SERIAL_MAIN Serial
#define SERIAL_FWD Serial1

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


#define MIN(x,y) (x<y?x:y)
#define MAX(x,y) (x>y?x:y)
#define ABS(x) x<0?-x:x
#endif

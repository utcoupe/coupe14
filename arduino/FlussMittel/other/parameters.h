#ifndef PARAMETERS_H
#define PARAMETERS_H

//////////////////////
//		PARAMETERS  //
//////////////////////

//DIMENSIONS

#define BRAS_OFFSET_DIST 130 //Distance in mm
#define BRAS_OFFSET_ANGLE -4 //Angle offset in degrees

#define DECALAGE_VENT_AXE 35

#define HAUTEUR_MAX 150 //En mm
#define HAUTEUR_MIN 17 //en mm

#define X_BRAS 128
#define Y_BRAS 130

//STEPPER

#define PERIOD_STEPPER 200
#define VMAX_STEPPER 350 
#define AMAX_STEPPER 30000 

//SECU BRAS : en degree commande

#define ANGLE_DIST_MAX 150
#define ANGLE_DIST_MIN 70

#define ANGLE_ANGLE_MAX 180 
#define ANGLE_ANGLE_MIN 40
#define ANGLE_INSIDE_ROBOT 110
#define SECU_DELAY_REPLI_BRAS 100 //ms
#define SECU_DELAY_ROT_BRAS 500 //ms

//BRAS

#define H_TO_STEP (16.0/3.0)

#define LONGUEUR_MAX 225 
#define LONGUEUR_MIN BRAS_OFFSET_DIST
#define MARGE_SECU_TOP 40 //En steps

#define MARGE_DEPOT 50
#define MARGE_PREHENSION 20
#define HAUTEUR_GARDE_DEPOT HAUTEUR_MIN + 10
#define HAUTEUR_DEPOT_ARRIERE 130

#define ANGLE_DEPOT (-(95.0/180.0)*M_PI)
#define LONGUEUR_DEPOT LONGUEUR_MIN

#define ANGLE_DEPOT_RET (-(105.0/180.0)*M_PI) 
#define LONGUEUR_DEPOT_RET 205


//PREHENSION

#define DELAY_REPLI_BRAS_AVANT_POMPE 700
#define DELAY_REPLI_BRAS_ARRIERE_POMPE 1100
#define DELAY_REPLI_BRAS2 100
#define DELAY_STOP_PUMP 100

//DEPOT TRIANGLES

#define HAUTEUR_BRAS_DEPOT 80
#define LONGUEUR_BRAS_AVANT_DEPOT 205

//POUSSER TRIANGLES

#define DELAY_SERVO_PUSH 500
#define HAUTEUR_PUSH_TRI 40
#define LONGUEUR_PUSH_TRI 180 

//TRIANGLES BORDURES
#define HAUTEUR_TRI_BORDURE 70
#define LONGUEUR_TRI_BORDURE 200
#define ANGLE_REPLI_TRI (-(70/180.0)*M_PI) 
#define ANGLE_OUVERT 0 

//RETOURNEMENT
#define ANGLE_RET 85
#define DELAY_RET 500
#define ACTIVATE 1

//POMPE
#define PWM_PUMP 255

//////////////////////
//		PINS		//
//////////////////////
#define PIN_SERVO_RET 47
#define PIN_SERVO_BRAS_ANGLE 45
#define PIN_SERVO_BRAS_DIST 43

#define PIN_JACK 52

#define PIN_VALVE 48

#define PIN_INTERRUPT_BRAS 26 //PULLUP ICI
#define PIN_INT_HAUT_ASC 24 //PULLUP

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

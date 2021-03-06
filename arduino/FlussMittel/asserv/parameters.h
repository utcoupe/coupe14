/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 29/11/13			*
 ****************************************/
#ifndef PARAMETERS_H
#define PARAMETERS_H

//#define DEBUG //Commenter cette ligne pour enlever les pints de debug

/* Simple ou Double ou Quadruple evaluation ? 
 * La quadruple evaluation utilise 4 interruption par tick
 * (une pour chaque changement de valeur des fils A et B)
 *
 * La double evaluation utilise 2 interruptions par tick
 * (une pour chaque changement de valeur du fil A
 *
 * La simple evaluation utilise 1 interruption par tick
 * (front montant du fil A)
 *
 * Ces trois méthodes sont equivalentes
 * La quadruple evaluation est plus précise mais utilise
 * plus de puissance processeur
 * Il convient de tester la plus adapté selon le processeur
 * et le nombre de ticks du codeur 
 * 
 * OPTIONS : '1' - '2 - '4' */

#define ENCODER_EVAL 1

#define FIXED_POINT_PRECISION 100000 //The robot's position is stocked with a precision of 1/FIXED_POINT_PRECISION mm 

#define GESTION_3EME_FIL false

#define MAX_GOALS 15 //nombre max de goals dans la file, évite surcharge mémoire
#define DUREE_CYCLE 5 //période de calcul, en ms
#define FREQ (1/(DUREE_CYCLE/1000.0))

#define ACC_MAX 500 //consigne*s-2
#define RATIO_SPD_ROT_MAX 0.8

/* CONSIGNE OFFSET
 * DEVRAIT ETRE A 0
 * "shift" de la pwm sur l'asservissement CC
 * cela sert à remédier au problème lié au fait 
 * qu'en dessous d'une certaine tension, les moteurs
 * CC ne tournent pas
 * 
 * Process de rélage :
 * envoyer des consignes en pwm au robot
 * partant de 0 et en augmentant progressivement
 * dès que le robot avance, la pwm min est trouvée */
#define PWM_MIN 5

#define CONSIGNE_MAX 255

#define CONSIGNE_RANGE_MAX (CONSIGNE_MAX - PWM_MIN)

//CONSIGNE_REACHED est la pwm en dessous de laquelle un robot peut etre considéré comme arrêté à son goal
#define CONSIGNE_REACHED 10

#define ENC_RESOLUTION 1024 //resolution du codeur

#define ENC_LEFT_RADIUS 36.15 //REGLE PAR TEST - rayon de la roue codeuse
#define ENC_RIGHT_RADIUS 36.15 //REGLE PAR TEST - rayon de la roue codeuse
#define ENTRAXE_ENC 323.85 //REGLE PAR TES - Distance entre chaque roue codeuse en mm

#define ERROR_ANGLE 0.02 //erreur en angle(radians) maximale pour considérer l'objectif comme atteint
#define ERROR_ANGLE_TO_GO 0.1 //erreur en angle(radians) maximale avant de partir en cas de GOTO
#define ERROR_POS 10 // erreur en position (mm)  maximale pour considérer l'objectif comme atteint

#define MAX_ANGLE 0.20  //~10° angle en dessous duquel on décrit une trajectoire curviligne (trop bas, le robot s'arretera constamment pour se recaler au lieu d'avancer, trop haut, les trajectoires seront très courbes voir meme fausses (overflow spd -> overflow pwm).
#define D_MIN_ASSERV_ANGLE 20
#define CONE_ALIGNEMENT 2.09 //120deg

//Intégrales et dérivée sont calculée avec un intervalle de temps en SECONDES
//Ne modifier que le nombre, laisser les DUREE_CYCLE

//Le "I" devrait etre faible (ou nul), le "D" est à régler progressivement pour éviter le dépassement
#define ANG_P 1000 //spd = P * E_ang(rad)
#define ANG_I 0 //spd = I * I_ang(rad * s)
#define ANG_D 150 //a regler par incrementation
#define ANG_AWU 0

#define DIS_P 3.5 //spd = P * E_dis(mm)
#define DIS_I 0 //spd = I * I_dis(mm * s)
#define DIS_D 0.4 //a regler par incrementation
#define DIS_AWU 0

#define TIME_BETWEEN_ORDERS 500

//BLOCAGE
//TIME_BLOCKED : période de vérification (ms)
//MIN_DIST_BLOCKED : disatcne min a parcourir pour ne pas etre considere bloqué (mm)
#define PERIOD_BLOCKED 1000
#define MIN_DIST_BLOCKED 3

//PIN LED
#define LED_MAINLOOP 22
#define LED_BLOCKED 23

//DEFINES ARDUINO
#define SERIAL_MAIN Serial2

#define PIN_ENC_RIGHT_A 21
#define PIN_ENC_RIGHT_B 20
#define PIN_ENC_RIGHT_0 4 //non utilisé
#define PIN_ENC_LEFT_A 19
#define PIN_ENC_LEFT_B 18
#define PIN_ENC_LEFT_0 2 //non utilisé

#define INTERRUPT_ENC_LEFT_A 4
#define INTERRUPT_ENC_LEFT_B 5
#define INTERRUPT_ENC_LEFT_0 0 //non utilisé
#define INTERRUPT_ENC_RIGHT_A 2
#define INTERRUPT_ENC_RIGHT_B 3
#define INTERRUPT_ENC_RIGHT_0 1 //non utilisé

/*****************************************
 *            PRIVATE                    *
 *****************************************/
#if ENCODER_EVAL == 4
	#define TICKS_PER_TURN (ENC_RESOLUTION * 4)
#elif ENCODER_EVAL == 2
	#define TICKS_PER_TURN (ENC_RESOLUTION * 2)
#elif ENCODER_EVAL == 1
	#define TICKS_PER_TURN ENC_RESOLUTION
#endif

#ifdef DEBUG
#define PDEBUG(x) Serial.print(x)
#define PDEBUGLN(x) Serial.println(x)
#define WRDEBUG(x) Serial.write(x)
#define BINPR(x) Serial.print(x, BIN)
#else
#define PDEBUG(x)
#define PDEBUGLN(x)
#define WRDEBUG(x)
#define BINPR(x)
#endif

#endif

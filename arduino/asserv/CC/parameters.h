/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 11/10/13			*
 ****************************************/
#ifndef PARAMETERS_H
#define PARAMETERS_H

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

#define FIXED_POINT_PRECISION 100 //The robot's position is stocked with a precision of 1/FIXED_POINT_PRECISION ticks

#define GESTION_3EME_FIL false

#define MAX_GOALS 15 //nombre max de goals dans la file, évite surcharge mémoire
#define DUREE_CYCLE 5 //période de calcul, en ms

/* Vitesse Maximale
 * Vitesse max à laquelle peuvent aller les moteurs
 * Utile pour asservir la vitesse
 * Il suffit de commander les moteurs à pwm maximale et de faire un
 * control.getMotorSpd()
 * Cette vitesse est en mm/ms = m/s  */

//#define SPD_MAX 1.0
//#define ACCELERATION_MAX 0.5

/* PWM MINIMALE 
 * "shift" de la pwm sur l'asservissement CC
 * cela sert à remédier au problème lié au fait 
 * qu'en dessous d'une certaine tension, les moteurs
 * CC ne tournent pas
 * 
 * Process de rélage :
 * envoyer des consignes en pwm au robot
 * partant de 0 et en augmentant progressivement
 * dès que le robot avance, la pwm min est trouvée */
#define PWM_MIN 0

#define ENC_RESOLUTION 1024 //resolution du codeur

#define ENC_RADIUS 34 //rayon de la roue codeuse
#define ENTRAXE_ENC 262.0 // Distance entre chaque roue codeuse en mm
#define ENTRAXE_MOTOR 262.0 // Distance entre chaque roue motrice en mm

#define ERROR_ANGLE 0.05 //erreur en angle(radians) maximale pour considérer l'objectif comme atteint
#define ERROR_POS 10 // erreur en position (mm)  maximale pour considérer l'objectif comme atteint

#define MAX_ANGLE 0.20  //~10° angle en dessous duquel on décrit une trajectoire curviligne (trop bas, le robot s'arretera constamment pour se recaler au lieu d'avancer, trop haut, les trajectoires seront très courbes voir meme fausses (overflow spd -> overflow pwm).

//Intégrales et dérivée sont calculée avec un intervalle de temps en SECONDES
//Ne modifier que le nombre, laisser les DUREE_CYCLE
/*
//Le "I" est très important, sans lui, l'erreur statique sera très élevée
#define SPEED_P 255 //pwm += P * E_spd(m/s)
#define SPEED_I 10 //pwm += I * I_spd(m/s * s)
#define SPEED_D 0 
*/
//Le "I" devrait etre faible (ou nul), le "D" est à régler progressivement pour éviter le dépassement
#define ANGLE_P 0.75 //spd = P * E_ang(rad)
#define ANGLE_I 0 //spd = I * I_ang(rad * s)
#define ANGLE_D 0 //a regler par incrementation

#define DISTANCE_P 0.002 //spd = P * E_dis(mm)
#define DISTANCE_I 0 //spd = I * I_dis(mm * s)
#define DISTANCE_D 0 //a regler par incrementation

//DEFINES ARDUINO
#define PIN_ENC_RIGHT_A 21
#define PIN_ENC_RIGHT_B 20
#define PIN_ENC_RIGHT_0 3
#define PIN_ENC_LEFT_A 18
#define PIN_ENC_LEFT_B 19
#define PIN_ENC_LEFT_0 2

#define INTERRUPT_ENC_LEFT_A 5
#define INTERRUPT_ENC_LEFT_B 4
#define INTERRUPT_ENC_LEFT_0 0
#define INTERRUPT_ENC_RIGHT_A 2
#define INTERRUPT_ENC_RIGHT_B 3
#define INTERRUPT_ENC_RIGHT_0 1

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
/*
#define ACC_MAX ACCELERATION_MAX * DUREE_CYCLE

#define SPD_P SPEED_P 
#define SPD_I SPEED_I * DUREE_CYCLE
#define SPD_D SPEED_D / DUREE_CYCLE
*/
#define ANG_P ANGLE_P
#define ANG_I ANGLE_I * DUREE_CYCLE
#define ANG_D ANGLE_D / DUREE_CYCLE

#define DIS_P DISTANCE_P
#define DIS_I DISTANCE_I * DUREE_CYCLE
#define DIS_D DISTANCE_D / DUREE_CYCLE

#endif

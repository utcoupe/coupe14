#ifndef ACTIONS_H
#define ACTIONS_H

#include "parameters.h"
#include "Servo.h"

void retourServo(Servo *servo=0, int pos=0, int delay=RETOUR_SERVO);
void tirBalles(int nbr);
void balai(int side);
void tirFilet();
void initPins();
void initServos();

#endif

/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 11/12/13			*
 ****************************************/
#ifndef SERIAL_TYPES_H
#define SERIAL_TYPES_H
#include <stdint.h>

// SUR ARDUINO //
// sizeof(int) = 2B
// sizeof(long) = 4B
// sizeof(float) = sizeof(double) = 4B
//
// Pas de double sur arduino donc pas de double dans le protocole

int16_t btoi(unsigned char *bytes);
int32_t btol(unsigned char *bytes);
float btof(unsigned char *bytes);
unsigned char* itob(int16_t i, unsigned char *bytes);
unsigned char* ltob(int32_t i, unsigned char *bytes);
unsigned char* ftob(float f, unsigned char *bytes);

#endif

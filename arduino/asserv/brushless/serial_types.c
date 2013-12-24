/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 11/12/13			*
 ****************************************/
#include "serial_types.h"
#include <string.h> //memcpy dépends de string.h
#include <stdint.h>

int16_t btoi(unsigned char *bytes){
	int16_t i;
	memcpy(&i, bytes, sizeof(int16_t));
	return i;
}

int32_t btol(unsigned char *bytes){
	int32_t i;
	memcpy(&i, bytes, sizeof(int32_t));
	return i;
}

float btof(unsigned char *bytes){
	float f;
	memcpy(&f, bytes, sizeof(float));
	return f;
}

unsigned char* itob(int16_t i, unsigned char *bytes){
	memcpy(bytes, &i, sizeof(int16_t));
	return bytes;
}

unsigned char* ltob(int32_t i, unsigned char *bytes){
	memcpy(bytes, &i, sizeof(int32_t));
	return bytes;
}

unsigned char* ftob(float f, unsigned char *bytes){
	memcpy(bytes, &f, sizeof(float));
	return bytes;
}

#ifndef COMPAT_H
#define COMPAT_H

#include <stdio.h>
#include "global.h"

#define LOCAL_ADDR ADDR_HOKUYO

typedef enum bool 
{ 
	true = 1, false = 0 
} bool;

long timeMillis();
unsigned char generic_serial_read();
void serial_send(char c);
int set_interface_attribs (int fd, int speed, int parity);
void set_blocking (int fd, int should_block);

#ifdef DEBUG
#define PDEBUGLN(x) printf(x);printf("\n");
#define PDEBUG(x) printf(x);
#else
#define PDEBUGLN(x)
#define PDEBUG(x)
#endif

#endif

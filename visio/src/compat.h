#ifndef COMPAT_H
#define COMPAT_H

#include <stdio.h>
#include "global.h"

typedef enum bool 
{ 
	true = 1, false = 0 
} bool;

long timeMillis();
unsigned char serial_read();
void serial_send(char c);
int set_interface_attribs (int fd, int speed, int parity);
void set_blocking (int fd, int should_block);

#endif

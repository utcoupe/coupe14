#ifndef COMPAT_H
#define COMPAT_H

#define LOCAL_ADDR ADDR_FLUSSMITTEL_CAM

#include <stdio.h>

#ifdef DEBUG
#define PDEBUGLN(x) printf(x);printf("\n");
#define PDEBUG(x) printf(x);
#else
#define PDEBUGLN(x)
#define PDEBUG(x)
#endif

typedef enum bool 
{ 
	true = 1, false = 0 
} bool;

long timeMillis();
unsigned char serial_read();
void sendByte(char c);
int set_interface_attribs (int fd, int speed, int parity);
void set_blocking (int fd, int should_block);

#endif

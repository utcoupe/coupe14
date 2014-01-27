#ifndef COMPAT_H
#define COMPAT_H

#define LOCAL_ADDR ADDR_FLUSSMITTEL_CAM

void sendByte(char c);
void set_blocking (int fd, int should_block);
int set_interface_attribs (int fd, int speed, int parity);

#endif

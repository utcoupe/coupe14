#ifndef HARDWARE_H_INCLUDED
#define HARDWARE_H_INCLUDED

int serialInit();

int serialSend(char*, char);

int serialRead(char*, char);

void serialClose();


#endif // HARDWARE_H_INCLUDED

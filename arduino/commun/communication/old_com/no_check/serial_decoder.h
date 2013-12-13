/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 11/12/13			*
 ****************************************/
#ifndef SERIAL_DECODER_H
#define SERIAL_DECODER_H

enum etape {ador,param,wait};
void executeCmd(char serial_data);
int getSize(char ordre);

#endif

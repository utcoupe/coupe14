/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/
#ifndef SERIAL_DECODER_H
#define SERIAL_DECODER_H

#define MAX_DATA 20 //Nombre max d'octet par frame

enum etape {ID_step,data_step,end_step,wait_step};
void executeCmd(char serial_data);
int decode(unsigned char *data_in, unsigned char *data_out, int data_counter); //7bits -> 8bits (on garde le même tableau)
int encode(unsigned char *data_in, unsigned char *data_out, int data_counter); //8bits -> 7bits (deux tableaux)
int check(unsigned char *data, int data_counter); //Vérifie la validité des données 8 bits
int executeOrdre(unsigned char *data, int data_counter, unsigned char id, bool doublon);
void sendResponse(unsigned char *data, int data_counter, unsigned char id); //Envoit un tableau de char 8 bits en réponse standard
void sendInvalid(); //renvoit le code de message invalide (dépend de la plateforme)

#endif

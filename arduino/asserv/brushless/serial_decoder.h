/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 22/01/13			*
 ****************************************/
#ifndef SERIAL_DECODER_H
#define SERIAL_DECODER_H

#define MAX_DATA 20 //Nombre max d'octet par frame

enum etape {ID_step,data_step,wait_step};
void executeCmd(char serial_data);
int decode(unsigned char *data_in, unsigned char *data_out, int data_counter); //Decodage des données et vérification de corruption
unsigned char right_shift_array(unsigned char *data_in, unsigned char *data_out, int data_counter, int shift); //Decalage de tableau à droite
int encode(unsigned char *data_in, unsigned char *data_out, int data_counter); //8bits -> 7bits (deux tableaux)
void executeOrdre(unsigned char *data, int data_counter, unsigned char id, bool doublon);
void sendResponse(unsigned char *data, int data_counter, unsigned char id); //Envoit un tableau de char 8 bits en réponse standard
void sendInvalid(); //renvoit le code de message invalide (dépend de la plateforme)
void protocol_reset(char *ID); //reset du protocole

#endif

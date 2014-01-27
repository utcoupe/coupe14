/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 22/01/13			*
 ****************************************/

#include <unistd.h>
#include <stdio.h>

#include "compat.h"
#include "serial_decoder_raspy.h"
#include "serial_defines.h"
#include "serial_types.h"

extern unsigned char ordreSize[MAX_ORDRES];
extern int fd;

int executeCmd(char serial_data){
	static char ID_recu;
	static char ID_attendu = 0;
	static unsigned char data[MAX_DATA];
	static int data_counter = 0;
	static int doublon = 0;

	static enum etape etape = wait_step;
	int executer_ordre = 0;

	if((serial_data & PROTOCOL_BIT) == PROTOCOL_BIT){ //Si 0b1xxxxxxx
		if (serial_data == END) { //Fin de trame, execution de l'ordre
			unsigned char data_8bits[MAX_DATA];

                        data_counter = decode(data, data_8bits, data_counter);
                        if(data_counter == -1){ //Si données invalides
				sendInvalid();
				etape = wait_step;
			}
			else{
				executer_ordre = executeOrdre(data_8bits, data_counter, ID_recu, doublon); //Execute les ordres, envoit les réponses
				if (!doublon){
					ID_attendu=(ID_attendu + 1) % (ID_MAX+1);//ID sur 6 bits effectifs, incrémentée si non doublon
				}
				etape = wait_step;
			}
			data_counter = 0;
			doublon = 0;
		}
		else if((serial_data & 0x0F) == LOCAL_ADDR){ //Si début de paquet adressé au client
			if ((serial_data & 0xF0) == RESET){ //Si demande de reset
				ID_attendu = 0;
				sendByte(RESET_CONF | LOCAL_ADDR);
				printf("Reset confirme\n");
			}
			else{
				etape = ID_step; //Sinon le message nous est adressé
			}
		}
		else{ //Si fin de paquet ou packet non adressé au client
			etape = wait_step;
		}
	}
	else{
		switch(etape){
		case ID_step: //On attend l'ID du paquet (1er octet)
			ID_recu = serial_data;
			if(ID_recu == ID_attendu){//ID correct
				etape = data_step;
			}
			else if(ID_recu > ID_attendu || (ID_attendu == ID_MAX && ID_recu < (ID_attendu - ID_MAX/2))){//On a raté un paquet - ID_MAX/2 représente la marge de paquets perdus
				etape = wait_step;
				sendInvalid();
			}
			else {//Doublon
				etape = data_step;
				doublon = 1;
			}
			break;
		case data_step:
			data[data_counter] = serial_data;
			data_counter++;
			break;
		case wait_step:
			break;
		}
	}
	if (executer_ordre)
		return ID_recu;
	else
		return -1;
}

//decode permet de décoder les données recues par la protocole, de manièe complète (plusieurs ordres par tramme. En revanche, le décodage est BEAUCOUP plus long.
//En plus, full_decode effectue la vérification des dnnées
//Renvoit le compte de données en cas de succès, -1 en cas de corruption de données
int decode(unsigned char *data_in, unsigned char *data_out, int data_counter){ 
	int i = 0, j = 0, offset = 0;
	//Transformation 7->8bits classique
	for(i=0;i<data_counter;i++){
		if(offset == 7){
			i++;
			offset = 0;
		}
		data_out[j] = data_in[i] << (1+offset);
		data_out[j] |= data_in[i+1] >> (6-offset);
		offset++;
		j++;
	}

        data_counter = j; //nouveau compte de datas

        //recalage des ordres 6bits
        i = 0;
	while(i<data_counter){
                unsigned char overflow = right_shift_array(data_out + i, data_out + i, data_counter - i, 2); //Shift tout le tableau à droite de 1 à partir de i (le premier ordre est calé)
                if(overflow != 0){
                        data_out[data_counter] = overflow; //Si overflow, on le met (attention aux segfault)
                }
                //Ici le premier ordre est calé à la première boucle, le deuxieme à la deuxieme,etc ...
                
                unsigned char ordre = data_out[i];
		if(ordre > MAX_ORDRES){//L'odre n'existe pas => corruption
			return -1;
		}
		unsigned char size = ordreSize[(int)ordre];
		if(size == SIZE_ERROR){//L'ordre n'existe pas => corruption de données
			return -1;
		}
		else{
			i += size + 1; //On se décale de la taille de l'ordre + 1 (+1 car on se décale aussi de l'ordre)
		}
	}
	return data_counter;
}

//Shift un tableau de char à droite, le même tablaue peut etre donnée en entrée et en sortie, l'overflow est renvoyé
unsigned char right_shift_array(unsigned char *data_in, unsigned char *data_out, int data_counter, int shift){
        int i;
        unsigned char temp = 0, last = 0;
        for(i=0;i<data_counter;i++){
                temp = data_in[i] << (8-shift);
                data_out[i] = (data_in[i] >> shift) | last;
                last = temp;
        }
        return last;
}

int encode(unsigned char *data_in, unsigned char *data_out, int data_counter){ //8bits -> 7bits (deux tableaux)
	int offset = 0, i = 0, j = 0;
	unsigned char copy = 0;
	for (i=0;i<data_counter;i++){
		if(offset == 7){
			data_out[j] = copy & 0x7f;
			offset = 0;
			copy = 0;
			i--;
		}
		else{
			unsigned char temp = data_in[i];
			data_out[j] = data_in[i] >> (1+offset);
			data_out[j] |= copy << (7-offset);
			data_out[j] &= 0x7f;
			copy = temp;
			offset++;
		}
		j++;
	}
	if (offset == 0){
		j--;
	}
	else{
		data_out[j] = copy << (7-offset);
		data_out[j] &= 0x7f;
	}
	return j+1;
}

int executeOrdre(unsigned char *data, int data_counter, unsigned char id, int doublon){
	int i = 0;
	unsigned char ordre;
	ordre = data[i];
	if (ordre == GET_CAM)
		return 1;
	return 0;
}

void sendResponse(unsigned char *data, int data_counter, unsigned char id){
	unsigned char data_7bits[MAX_DATA];
	int i, size;
	size = encode(data, data_7bits, data_counter);
	sendByte(LOCAL_ADDR | PROTOCOL_BIT); //début de réponse
	sendByte(id);
	for(i = 0 ; i < size ; i++){
		sendByte(data_7bits[i]); //contenu
	}
	sendByte(END); //fin de réponse
}

void sendInvalid() {//renvoit le code de message invalide (dépend de la plateforme)
	perror("Data invalid\n");
	sendByte(LOCAL_ADDR | PROTOCOL_BIT); //début de réponse
	sendByte(INVALID_MESSAGE);
	sendByte(END);
}

void protocol_reset(){
	char data;
	while(read(fd, &data, 1) != (RESET_CONF | LOCAL_ADDR)){
		sendByte(RESET | LOCAL_ADDR);
	}
	printf("Reset\n");
}

void init_protocol(){
	initSize();
	protocol_reset();
}


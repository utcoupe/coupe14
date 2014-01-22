/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/
#include "serial_decoder.h"
#include "serial_defines.h"
#include "serial_local.h"
#include "serial_switch.h"
#include "serial_types.h"

extern unsigned char ordreSize[MAX_ORDRES];

void executeCmd(char serial_data){
	static char ID_recu;
	static char ID_attendu = 0;
	static unsigned char data[MAX_DATA];
	static int data_counter = 0;
	static bool doublon = false;

	static enum etape etape = wait_step;

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
			doublon = true;
		}
		break;
	case data_step:
		if ((serial_data & PROTOCOL_BIT) == 0){
			data[data_counter] = serial_data;
			data_counter++;
			break;
		}
		else if (serial_data == END) {
			unsigned char data_8bits[MAX_DATA];

                        /* ANCIEN DECODEUR
			data_counter = decode(data, data_8bits, data_counter); //Décale le tableau data pour avoir des données 8 bits, renvoit le nombre d'octets apres décalage
			if(check(data_8bits, data_counter) != 0){//Si les data sont invalide
                        */
                        data_counter = decode(data, data_8bits, data_counter);
                        if(data_counter == -1){ //Si données invalides
				sendInvalid();
				etape = wait_step;
			}
			else{
#ifdef DEBUG
                                int i;
                                for(i = 0; i < data_counter; i++){
                                        PDEBUG("Data "); PDEBUG(i); PDEBUG(" : ");
                                        BINPR((int)data_8bits[i]); PDEBUGLN("");
                                }
#endif
				executeOrdre(data_8bits, data_counter, ID_recu, doublon); //Execute les ordres, envoit les réponses
				if (!doublon){
					ID_attendu=(ID_attendu + 1) % (ID_MAX+1);//ID sur 6 bits effectifs, incrémentée si non doublon
				}
				etape = wait_step;
			}
			data_counter = 0;
			doublon = false;
		}
		else {
			sendInvalid();
			etape = wait_step;
			break;
		}
		break;
	case wait_step:
		break;
	}

	if((serial_data & PROTOCOL_BIT) != 0){ //Si 0b1xxxxxxx
		if((serial_data & 0x7f) == LOCAL_ADDR) //Si début de paquet adressé au client
			etape = ID_step;
		else //Si fin de paquet ou packet non adressé au client
			etape = wait_step;
	}
}
/*
// decode permet de transformée un tableau de char de données recues sur 7 bits en données faisant sens sur 8 bits.
// Un simple décalage ne suffit pas car l'ordre est codé sur 6bits, il faut donc l'extraire avant de traiter la suite.
//
// N'ayant pas trouvé de solution jugée suffisamment efficace (il ne faut pas que la communication prenne des ressources), la fonction ne peut décoder qu'un peu rre par tramme.
int decode(unsigned char *data_in, unsigned char *data_out, int data_counter){ 
	int i = 0, j = 0, offset = 0;
	//Recupération de l'ordre sur 6bits
	data_out[0] = data_in[0] >> 1;
	j++;

	//Test necessaire pour ne pas seg-fault (ou corruption de data) sur les ordres sans paramètres
	if(data_counter > 1){
		data_out[1] = (data_in[0] << 7) | data_in[1] ;
		j++;
	}
	
	//Transformation 7->8bits classique
	for(i=2;i<data_counter;i++){
		if(offset == 7){
			i++;
			offset = 0;
		}
		data_out[j] = data_in[i] << (1+offset);
		data_out[j] |= data_in[i+1] >> (6-offset);
		offset++;
		j++;
	}
	return j;
}*/

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

//Shift un tableau de char à gauche, le même tableau peut etre donnée en entrée et en sortie
//Inutile ?
unsigned char left_shift_array(unsigned char *data_in, unsigned char *data_out, int data_counter, int shift){
        int i;
        unsigned char ret = data_in[0] >> (8-shift);
        for(i=0;i<data_counter-1;i++){
                unsigned char temp = data_in[i+1] >> (8-shift);
                data_out[i] = (data_in[i] << shift) | temp;
        }
        data_out[i] = data_in[i] << shift;
        return ret;
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

/* ANCIEN DECODEUR
int check(unsigned char *data, int data_counter){ //Vérifie la validité des données 8 bits
	int i = 0;
	while(i<data_counter){
		unsigned char ordre = data[i];
		if(ordre > MAX_ORDRES){//L'odre n'existe pas => corruption
			return -1;
		}
		unsigned char size = ordreSize[ordre];
		if(size == SIZE_ERROR){//L'ordre n'existe pas => corruption de données
			return -1;
		}
		else{
			i += size + 1; //On se décale de la taille de l'ordre + 1 (+1 car on se décale aussi de l'ordre)
		}
	}
	return 0;
}*/

void executeOrdre(unsigned char *data, int data_counter, unsigned char id, bool doublon){
	int i = 0, ret_size = 0;
	unsigned char ordre;
	unsigned char *params;
	unsigned char ret[MAX_DATA];
	//while (i < data_counter) { PROBLEME : les bits poubelles crée un ordre en trop - Solution : On commente la boucle : un seule ordre par tramme
		ordre = data[i];
		params = data + i + 1;
		ret_size += switchOrdre(ordre, params, (ret + ret_size), doublon);//execution ordres, enregistrement du retour
		i += ordreSize[ordre] + 1;
	//}
	sendResponse(ret, ret_size, id);
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
        PDEBUGLN("Data error");
	sendByte(LOCAL_ADDR | PROTOCOL_BIT); //début de réponse
	sendByte(INVALID_MESSAGE);
	sendByte(END);
}

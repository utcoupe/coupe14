/****************************************
 * Author : Quentin C			*
 * Mail : quentin.chateau@gmail.com	*
 * Date : 18/12/13			*
 ****************************************/
#include "Servo.h"
#include "Arduino.h"

#include "parameters.h"
#include "serial_switch.h"
#include "serial_defines.h"
#include "serial_types.h"

static Servo servoFilet, servoBalles1, servoBalles2, servoBalai;
static int tirs = 0;

void initPins() {
	servoFilet.attach(PIN_SERVO_FILET);
	servoBalles1.attach(PIN_SERVO_BALLES1);
	servoBalles2.attach(PIN_SERVO_BALLES2);
	servoBalai.attach(PIN_SERVO_BALAI);
}

void initServos() {
	servoFilet.write(POS_FILET_INIT);
	servoBalles1.write(POS_BALLES1_INIT);
	servoBalles2.write(POS_BALLES2_INIT);
	servoBalai.write(POS_BALAI_INIT);
}

//La fonction renvoit le nombre d'octet dans ret, chaine de caractère de réponse. Si doublon, ne pas executer d'ordre mais renvoyer les données à renvoyer
int switchOrdre(unsigned char ordre, unsigned char *argv, unsigned char *ret, bool doublon){ 
	static int last_id = 0;
	int ret_size = 0;
	switch(ordre){
	case O_TIR_FILET:
		last_id = btoi(argv);
		servoFilet.write(POS_TIR_FILET);
		break;
	case O_BALAI: {
		last_id = btoi(argv);
		int side = btoi(argv+2);
		if (side == LEFT) 
			servoBalai.write(POS_BALAI_L);
		else if (side == RIGHT) 
			servoBalai.write(POS_BALAI_R);
		}
		break;
	case O_TIR_BALLE: 
		last_id = btoi(argv);
		tirs += btoi(argv+2);
		if (tirs > 3) {
			servoBalles2.write((tirs - 3)*PAS_PAR_TIR + POS_BALLES2_INIT);
			servoBalles1.write(3*PAS_PAR_TIR + POS_BALLES2_INIT);
		} else {
			servoBalles1.write(tirs*PAS_PAR_TIR + POS_BALLES1_INIT);
		}
		break;
	case GET_LAST_ID:
		ret_size = 2;
		itob(last_id, ret);
		break;
	case RESET_ID:
		last_id = 0;
		break;
	default:
		return -1;//commande inconnue
	}
	return ret_size;
}

#include "compaArduino.h"
#include "serial_switch.h"
#include "serial_defines.h"
#include "serial_types.h"
#include "parameters.h"

extern Control control;

int switchOrder(char ordre, int argc, char *argv){
	ordre &= 0b00011111; //ordre sans adresse
	switch(ordre){
	case O_PING:
		Serial.write(IA_ADDR + O_PONG);
		break;
	case A_GOTO:
		//DEBUG
		PDEBUGLN("GOTO :");
		PDEBUG("arg 1 : ");PDEBUG(btoi(argv));
		PDEBUG(" arg 2 : ");PDEBUG(btoi(argv+2));
		PDEBUG(" arg 3 : ");PDEBUGLN(btof(argv+4));
		break;
	case A_GOTOA:
		break;
	case A_GOTOR:
		break;
	case A_GOTOAR:
		break;
	case A_ROT:
		control.pushGoal(0,TYPE_ANG, btof(argv), 0, 0);
		break;
	case A_ROTR:
		break;
	case A_PIDA:
		control.setPID_angle(btoi(argv),btoi(argv+2),btoi(argv+4));
		PDEBUG("PID : "); PDEBUG(btoi(argv)); PDEBUG(btoi(argv+2)); PDEBUGLN(btoi(argv+4)); 
		break;
	case A_PIDD:
		control.setPID_distance(btoi(argv),btoi(argv+2),btoi(argv+4));
		PDEBUG("PID : "); PDEBUG(btoi(argv)); PDEBUG(btoi(argv+2)); PDEBUGLN(btoi(argv+4)); 
		break;
	default:
		return -1;
	}
	return 0;
}

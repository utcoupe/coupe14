#ifndef PARAMETERS_H
#define PARAMETERS_H

#define DEBUG

// PINS
#define PIN_SERVO_FILET 42
#define PIN_SERVO_BALLES1 30
#define PIN_SERVO_BALLES2 38
#define PIN_SERVO_BALAI 34

#define SERIAL_MAIN Serial1
#define SERIAL_FWD Serial2

// PARAMETRES
#define POS_FILET_INIT 30 
#define POS_BALLES1_INIT 4
#define POS_BALLES2_INIT 4 
#define POS_BALAI_INIT 80 

#define POS_TIR_FILET 4 
#define POS_BALAI_R 0
#define POS_BALAI_L 140
#define PAS_PAR_TIR 10

#define LEFT -1
#define RIGHT 1



#ifdef DEBUG
#define PDEBUG(x) Serial.print(x)
#define PDEBUGLN(x) Serial.println(x)
#define BINPR(x) Serial.print(x, BIN)
#else
#define PDEBUG(x)
#define PDEBUGLN(x)
#define WRDEBUG(x)
#define BINPR(x)
#endif

#endif

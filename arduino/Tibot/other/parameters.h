#ifndef PARAMETERS_H
#define PARAMETERS_H

#define DEBUG

// PINS
#define PIN_SERVO_FILET 30
#define PIN_SERVO_BALLES1 31
#define PIN_SERVO_BALLES2 32
#define PIN_SERVO_BALAI 33

#define SERIAL_MAIN Serial2
#define SERIAL_FWD Serial1

// PARAMETRES
#define POS_FILET_INIT 0
#define POS_BALLES1_INIT 0
#define POS_BALLES2_INIT 0
#define POS_BALAI_INIT 90

#define POS_TIR_FILET 90
#define POS_BALAI_R 0
#define POS_BALAI_L 180
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

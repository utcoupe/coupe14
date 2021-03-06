#ifndef PARAMETERS_H
#define PARAMETERS_H
#define ARDUINO

#define DEBUG

// PINS
#define PIN_SERVO_FILET 42
#define PIN_SERVO_BALLES_L 30
#define PIN_SERVO_BALLES_R 38
#define PIN_SERVO_BALAI 34
#define PIN_JACK 52

#define SERIAL_MAIN Serial1
#define SERIAL_FWD Serial2

// PARAMETRES

#define RETOUR_SERVO 1000// ms

#define POS_FILET_INIT 30 
#define POS_BALLES_R0 4
#define POS_BALLES_L0 23 
#define POS_BALLES_R1 18
#define POS_BALLES_L1 11
#define POS_BALLES_R2 27
#define POS_BALLES_L2 8
#define POS_BALLES_R3 30
#define POS_BALLES_L3 3

#define POS_BALAI_INIT 70 

#define POS_TIR_FILET 0 
#define POS_BALAI_R 0
#define POS_BALAI_L 140

#define LEFT -1
#define MIDDLE 0
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

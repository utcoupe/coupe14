#ifndef PARAMETERS_H
#define PARAMETERS_H

#define PIN_SERVO_BRAS 8
#define PIN_SERVO_RET 9

#define PIN_INT_HAUT_ASC 22
#define PIN_INT_BAS_ASC 23

#ifdef DEBUG
#define PDEBUG(x) Serial3.print(x)
#define PDEBUGLN(x) Serial3.println(x)
#define BINPR(x) Serial3.print(x, BIN)
#else
#define PDEBUG(x)
#define PDEBUGLN(x)
#define BINPR(x)
#endif

#endif

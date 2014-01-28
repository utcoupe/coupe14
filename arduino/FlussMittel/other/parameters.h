#ifndef PARAMETERS_H
#define PARAMETERS_H

#include <Arduino.h>

#define DEBUG

#define PIN_SERVO_BRAS 8

#define PIN_INT_HAUT_ASC 2
#define INT_HAUT_ASC 0
#define PIN_INT_BAS_ASC 3
#define INT_BAS_ASC 1

#ifdef DEBUG
#define PDEBUG(x) Serial3.print(x)
#define PDEBUGLN(x) Serial3.println(x)
#define WRDEBUG(x) Serial3.write(x)
#define BINPR(x) Serial3.print(x, BIN)
#else
#define PDEBUG(x)
#define PDEBUGLN(x)
#define WRDEBUG(x)
#define BINPR(x)
#endif

#endif

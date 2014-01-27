#ifndef PARAMETERS_H
#define PARAMETERS_H

#define DEBUG

#define PIN_SERVO_BRAS 2

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

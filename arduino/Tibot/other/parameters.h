#ifndef PARAMETERS_H
#define PARAMETERS_H

#define DEBUG

#define PIN_SERVO_BRAS 2

#ifdef DEBUG
#define PDEBUG(x) Serial.print(x)
#define PDEBUGLN(x) Serial.println(x)
#define WRDEBUG(x) Serial.write(x)
#define BINPR(x) Serial.print(x, BIN)
#else
#define PDEBUG(x)
#define PDEBUGLN(x)
#define WRDEBUG(x)
#define BINPR(x)
#endif

#endif

// Visio UTCoupe 2014
// Par Quentin CHATEAU

#ifndef GLOBAL_H
#define GLOBAL_H

#define H_YEL 25
#define H_YEL_TOL 15
#define S_YEL_TOL 185
#define V_YEL_TOL 185

#define H_RED 0
#define H_RED_TOL 15
#define S_RED_TOL 185
#define V_RED_TOL 185

#define LOCAL_ADDR ADDR_FLUSSMITTEL_CAM

#ifdef DEBUG
#define PDEBUGLN(x) printf(x);printf("\n");
#define PDEBUG(x) printf(x);
#else
#define PDEBUGLN(x)
#define PDEBUG(x)
#endif

#endif

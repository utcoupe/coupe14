#include "actions.h"
#include "Servo.h"
#include "parameters.h"
#include <math.h>

extern Servo servoBras, servoRet, servoBrasAngle, servoBrasDist;

void cmdBras(int x, int y) {
	int d = (sqrt(x*x + y*y) + BRAS_OFFSET_DIST) * BRAS_DIST_TO_ANGLE;
	double theta = atan2(y, x) + BRAS_OFFSET_ANGLE;
	servoBrasAngle.write(theta);
	servoBrasDist.write(d);
}

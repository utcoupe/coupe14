#ifndef FAST_MATH_H
#define FAST_MATH_H

#include "global.h"

struct coord{
	int x;
	int y;
};

struct fastmathTrigo {
	int n;
	double *cos, *sin; 
};


int dist_squared(struct coord p1, struct coord p2);
int dist_to_edge(struct coord p, int largeurX, int largeurY);


struct fastmathTrigo initFastmath(int n, double *angles);
void freeFastmath(struct fastmathTrigo s);

double fastCos(struct fastmathTrigo f, int index);
double fastSin(struct fastmathTrigo f, int index);
double modTwoPi(double a);

#endif

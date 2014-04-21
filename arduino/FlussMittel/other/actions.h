#ifndef ACTIONS_H
#define ACTIONS_H

void initPins();
void init_act();
void asc_int();
void getTri(long x, long y, int h);
void deposeTri(int dep);
void cmdBrasServ(double a, int l);
void criticalCmdBras(int n_theta = -1, int n_alpha = -1);
void cmdAsc(int h);
void cmdBras(double angle = 1, int length = -1, int height = -1, int n_depot = 0);
int getCurrentHauteur();
void pump(bool etat);
void topStop();
void forwardstep();
void backwardstep();

#endif

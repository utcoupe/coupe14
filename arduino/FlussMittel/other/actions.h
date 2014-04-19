#ifndef ACTIONS_H
#define ACTIONS_H

void init_act();
void asc_int();
void cmdBrasServ(double a, int l);
void cmdAsc(int h);
void cmdBras(double angle, int length, int height, int n_depot);
void pump(bool etat);
void callback();
void topStop();

#endif

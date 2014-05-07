#ifndef ACTIONS_H
#define ACTIONS_H

enum action {
	None,
	BrasVentouse,
	TriBordure
};

void initPins();
void initAct();
void stopAct();
void getTri(long x, long y, int h);
void getTriBordure(int hauteur_ouverture=0);
void getTriBordureRepliBras();
void deposeTri(int dep);
void cmdBrasServ(double a, int l);
void criticalCmdBras(int n_theta = -1, int n_alpha = -1);
void cmdAsc(int h);
void updateBras();
void cmdBrasVentouse(double angle = 1, int length = -1, int height = -1, int n_depot = 0);
void cmdTriBordure(int hauteur_ouverture=0);
int getCurrentHauteur();
void ascInt();
void pump(bool etat);
void topStop();
void forwardstep();
void backwardstep();

#endif

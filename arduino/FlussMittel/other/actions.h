#ifndef ACTIONS_H
#define ACTIONS_H

enum action {
	None,
	BrasVentouse,
	TriBordure,
	TriPush,
	BrasDepot
};

void updateAct();
void updateJackState();
void initPins();
void initAct();
void callbackRet(int use=0);
void stopAct();
bool readyForNext();
void getBrasDepot(int x, int y);
void getTri(long x, long y, int h);
void getTriPush();
void getTriBordure();
void getTriBordureRepliBras();
void deposeTri(int dep);
void cmdBrasServ(double a, int l);
void criticalCmdBras(int n_theta = -1, int n_alpha = -1, int direction = 2);
void cmdAsc(int h);
void updateBras();
void cmdBrasDepot(double a = -1, int l=-1);
void cmdBrasVentouse(double angle = 1, int length = -1, int height = -1, int n_depot = 0);
void cmdTriPush();
void cmdTriBordure();
int getCurrentHauteur();
int getCurrentStockHeight();
void ascInt();
void pump(bool etat);
void topStop();
void forwardstep();
void backwardstep();

#endif

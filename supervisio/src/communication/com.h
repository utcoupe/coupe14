#ifndef COM_H
#define COM_H

#include "../traitement/traitement.h"

void communication(int index, std::string path_to_conf="./", bool save=false);
void comLoop(Visio& visio);

#endif

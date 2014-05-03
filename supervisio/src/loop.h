#ifndef LOOP_H
#define LOOP_H

#include <string>

void communication(int index, std::string path_to_conf="./", bool save=false);
void calibration(int index, std::string path="./");
void perspectiveOnlyLoop(int index, std::string path="./");

#endif

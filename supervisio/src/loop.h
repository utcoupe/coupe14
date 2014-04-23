#ifndef LOOP_H
#define LOOP_H

#include <string>

void communication(int index, std::string path_to_conf="./");
void calibration(int index, std::string path="./");
void perspectiveOnlyLoop(int index, std::string path="./");

#endif

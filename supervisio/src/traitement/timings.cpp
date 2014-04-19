#include <ctime>
#include <sys/time.h>
#include <iostream>
#include "timings.h"
#include "../global.h"

using namespace std;

long timeMicros() {
        struct timeval tv;       
        if(gettimeofday(&tv, NULL) != 0) return 0;
        return (unsigned long)((tv.tv_sec * 1000000ul) + (tv.tv_usec));        
}

Timings::Timings() {
	step = start = timeMicros();
}

float Timings::igetTime() {
	step = timeMicros();
	return (step - start)/1000.0;
}

float Timings::igetStepTime() {
	long new_step = timeMicros();
	long time = (new_step - step)/1000.0;
	step = new_step;
	return time;
}

void Timings::startTimer(int i) {
	if (i = nb_instances) {
		if (nb_max <= nb_instances) {
			Timings** temp = instances;
			instances = new Timings* [nb_instances + 5];
			for (int j=0; j < nb_instances; j++) {
				instances[j] = temp[j];
			}
			nb_max = nb_instances + 5;
			delete[] temp;
		}
		instances[nb_instances] = new Timings();
	}
	if (i < nb_instances) {
		delete instances[i];
		instances[i] = new Timings();
	}
	else {
		cerr << "Timins index incorrect" << endl;
	}
}

float Timings::getTime(int i) {
	if (i < nb_instances) {
		return instances[i]->igetTime();
	}
	else return 0;
}

float Timings::getStepTime(int i) {
	if (i < nb_instances) {
		return instances[i]->igetStepTime();
	}
	else return 0;
}

void Timings::writeTime(int i, string str) {
	cout << str << " : " << getTime(i) << endl;
}

void Timings::writeStepTime(int i, string str) {
	cout << str << " : " << getStepTime(i) << endl;
}

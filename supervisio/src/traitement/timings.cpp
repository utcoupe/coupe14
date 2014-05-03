#include <ctime>
#include <sys/time.h>
#include <iostream>
#include "timings.h"
#include "../global.h"

using namespace std;

int Timings::nb_instances = 0;
int Timings::nb_max = 0;
Timings** Timings::instances;

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
	float time = (new_step - step)/1000.0;
	step = new_step;
	return time;
}

void Timings::startTimer(int i) {
	if (TIMEBENCH) {
		if (i == nb_instances) {
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
			nb_instances++;
		}
		if (i < nb_instances) {
			delete instances[i];
			instances[i] = new Timings();
		}
		else {
			cerr << "Timins index incorrect : asked " << i << " and expcted " << nb_instances << " or less" << endl;
		}
	}
}

float Timings::getTime(int i) {
	if (TIMEBENCH) {
		if (i < nb_instances) {
			return instances[i]->igetTime();
		}
	}
	else return 0;
}

float Timings::getStepTime(int i) {
	if (TIMEBENCH) {
		if (i < nb_instances) {
			return instances[i]->igetStepTime();
		}
	}
	else return 0;
}

void Timings::writeTime(int i, string str) {
	if (TIMEBENCH) {
		cout << str << " : " << getTime(i) << "ms" << endl;
	}
}

void Timings::writeStepTime(int i, string str) {
	if (TIMEBENCH) {
		cout << str << " : " << getStepTime(i) << "ms" << endl;
	}
}

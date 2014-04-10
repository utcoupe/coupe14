#include <ctime>
#include <iostream>
#include "timings.h"
#include "../global.h"

using namespace std;

void timings(string name) {
	if (TIMEBENCH) {
		static bool init = true;
		static time_t start, end;
		if (name == "") {
			init == true;
		}
		if (init) {
			time(&start);
			init = false;
		}
		else {
			time(&end);
			cout << name << difftime(end, start) << endl;
			start = end;
		}
	}
}


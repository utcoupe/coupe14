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

void timings(string name) {
	if (TIMEBENCH) {
		static bool init = true;
		static long start, end;
		if (name == "") {
			init = true;
		}
		if (init) {
			start = timeMicros();
			init = false;
		}
		else {
			end = timeMicros();
			cout << name << (end - start)/1000.0 << "ms" << endl;
			start = end;
		}
	}
}


#ifndef TIMINGS_H
#define TIMINGS_H

#include <iostream>

class Timings {
	public:
		static void startTimer(int i);
		static float getTime(int i);
		static float getStepTime(int i);
		static void writeTime(int i, std::string str="");
		static void writeStepTime(int i, std::string str="");
	private:
		static Timings** instances;
		static int nb_instances = 0, nb_max = 0;
		Timings();
		float igetTime();
		float igetStepTime();
		long start, step;
}
void timings(std::string name = "");

#endif

// Visio UTCoupe 2014
// Par Quentin CHATEAU

#include <iostream>
#include <opencv2/opencv.hpp>

#include "loop.h"

using namespace cv;
using namespace std;

int main(int argc, char **argv){
	string mode = "com";
	int index = 0;
	if (argc > 1){
		index = argv[1][0] - '0';
	}
	if (argc > 2){
		mode = argv[2];
	}
	if (mode == "com") {
		communication(index);
	}
	else if(mode == "param") {
		perspectiveOnlyLoop(index);
	}
	else if (mode == "calib") {
		calibration(index);
	}
	else {
		cout << "./visio [index] [com/param/calib]" << endl;
	}
	return 0;
}

// Visio UTCoupe 2014
// Par Quentin CHATEAU

#include <iostream>
#include <opencv2/opencv.hpp>

#include "loop.h"

using namespace cv;
using namespace std;

int main(int argc, char **argv){
	string mode = "com", path = "./";
	int index = 0;
	if (argc > 1){
		index = argv[1][0] - '0';
	}
	if (argc > 2){
		mode = argv[2];
	}
	if (argc > 3) {
		path = argv[3]+(string)"/";
	}
	if (mode == "com") {
		communication(index, path);
	}
	else if(mode == "param") {
		perspectiveOnlyLoop(index, path);
	}
	else if (mode == "calib") {
		calibration(index, path);
	}
	else {
		cout << "./visio [index] [com/param/calib] [path_to_config]" << endl;
	}
	return 0;
}

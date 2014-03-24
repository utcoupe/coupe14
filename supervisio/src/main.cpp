// Visio UTCoupe 2014
// Par Quentin CHATEAU

#include <iostream>
#include <opencv2/opencv.hpp>

#include "perspective/traitement.h"
#include "perspective/gui.h"
#include "loop.h"

using namespace cv;
using namespace std;

int main(int argc, char **argv){
	int index = 0;
	if (argc > 1){
		index = argv[1][0] - '0';
	}
	perspectiveOnlyLoop(index);
	//testStereo();
	//color3d();
	return 0;
}

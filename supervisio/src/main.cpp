// Visio UTCoupe 2014
// Par Quentin CHATEAU

#include <iostream>
#include <opencv2/opencv.hpp>

#include "communication/com.h"
#include "traitement/traitement.h"
#include "traitement/gui.h"
#include "loop.h"

using namespace cv;
using namespace std;

int main(int argc, char **argv){
	char com = '1';
	int index = 0;
	if (argc > 1){
		index = argv[1][0] - '0';
	}
	if (argc > 2){
		com = argv[2][0];
	}
	if (com == '1') {
		VideoCapture cam(index);
		Visio visio(cam);
		visio.loadTransformMatrix();
		namedWindow("img");
		Mat img;
		cam >> img;
		comLoop(visio);
	}
	else
		perspectiveOnlyLoop(index);
	return 0;
}

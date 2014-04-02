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
	int index = 0;
	if (argc > 1){
		index = argv[1][0] - '0';
	}
	VideoCapture cam(index);
	Visio visio(cam);
	visio.loadTransformMatrix();
	namedWindow("img");
	Mat img;
	cam >> img;
	comLoop(visio);
	//perspectiveOnlyLoop(index);
	return 0;
}

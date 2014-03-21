#include "perspective/traitement.h"
#include "perspective/gui.h"
#include "stereo/stereo.h"
#include "loop.h"

void perspectiveOnlyLoop(int index){
	VideoCapture cam(index);
	 if(!cam.isOpened())  // check if we succeeded
		return;

	int h_min(100), h_max(110), s_min(200), s_max(255), v_min(130), v_max(255), key = -1;
	bool calibrating = true, real_time = false;

	namedWindow("parameters");
	namedWindow("origin");

	createTrackbar("h_min", "parameters", &h_min, 180);
	createTrackbar("h_max", "parameters", &h_max, 180);
	createTrackbar("s_min", "parameters", &s_min, 255);
	createTrackbar("s_max", "parameters", &s_max, 255);
	createTrackbar("v_min", "parameters", &v_min, 255);
	createTrackbar("v_max", "parameters", &v_max, 255);

	Mat transform;
	Scalar red(0,0,255);
	vector<Point2f> position;
	position.push_back(Point2f(0,0));
	position.push_back(Point2f(0,200));
	position.push_back(Point2f(200,0));
	position.push_back(Point2f(200,200));
	for(;;) { //int i=0; i>=0; i++) {
		Contours contour, detected_contours;
		vector<Point2f> detected_pts, realworld;
		Mat frame, persp;
		cam >> frame;

		if (key == 'c') {
			calibrating = !calibrating;
			real_time = false;
		}
		if (key == 'r') {
			calibrating = false;
			real_time = !real_time;
		}
		
		if (calibrating || real_time) {
			if (!real_time)
				destroyWindow("perspective");
			transform = getTransformMatrix(frame, frame, position);
		}
		if (!calibrating) {
			Scalar min(h_min,s_min,v_min), max(h_max,s_max,255);

			warpPerspective(frame, persp, transform, Size(200,200));
			getDetectedPosition(persp, detected_pts, detected_contours, min, max, 100);
			drawContours(persp, detected_contours, -1, red, 1);
			for(int i=0; i<detected_pts.size(); i++) {
				drawObject(detected_pts[i].x, detected_pts[i].y, persp);
			}

			resize(persp, persp, Size(600, 600));
			imshow("perspective", persp);
		}
		imshow("origin", frame);
		key = waitKey(1);
	}
}

void testStereo() {
	Stereo stereo(0,1);
	stereo.calibrate(15);
	stereo.displayCalibration();
}

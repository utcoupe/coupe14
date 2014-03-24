#include <opencv2/opencv.hpp>
#include "perspective/traitement.h"
#include "perspective/gui.h"
#include "stereo/stereo.h"
#include "loop.h"

using namespace cv;

void perspectiveOnlyLoop(int index){
	VideoCapture cam(index);
	 if(!cam.isOpened())  // check if we succeeded
		return;

	Visio visio;

	int h_min(90), h_max(100), s_min(200), s_max(255), v_min(130), v_max(255), key = -1;
	bool calibrating = true, real_time = false;

	namedWindow("parameters");
	namedWindow("origin");

	createTrackbar("h_min", "parameters", &h_min, 180);
	createTrackbar("h_max", "parameters", &h_max, 180);
	createTrackbar("s_min", "parameters", &s_min, 255);
	createTrackbar("s_max", "parameters", &s_max, 255);
	createTrackbar("v_min", "parameters", &v_min, 255);
	createTrackbar("v_max", "parameters", &v_max, 255);

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
			visio.computeTransformMatrix(frame, position, &frame);
		}
		if (!calibrating) {
			Scalar min(h_min,s_min,v_min), max(h_max,s_max,v_max);
			visio.setParameters(min, max);

			warpPerspective(frame, persp, visio.getQ(), Size(200,200));
			visio.getDetectedPosition(persp, detected_pts, detected_contours);
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
	Stereo stereo(1,2);
	if (!stereo.loadCameraCalibration()) {
		stereo.calibrate();
		stereo.saveCameraCalibration();
	}
	stereo.displayCalibration();
}

void color3d() {
	int h_min(90), h_max(100), s_min(200), s_max(255), v_min(130), v_max(255);
	Mat disp;
	vector<Point2f> position;
	position.push_back(Point2f(0,0));
	position.push_back(Point2f(200,0));
	position.push_back(Point2f(0,170));
	position.push_back(Point2f(200,170));

	Stereo stereo(1,2);
	Scalar min(h_min,s_min,v_min), max(h_max,s_max,v_max);
	Visio visio(min, max);

	if (!stereo.loadCameraCalibration()) {
		stereo.calibrate();
		stereo.saveCameraCalibration();
	}

	namedWindow("Left");
	do {
		stereo.newImage();
		Mat img = stereo.left_img;
		putText(img, "Chessboard not found",Point(20,20),1,2,Scalar(0,0,255),1);
		stereo.newImage();
	} while(!visio.computeTransformMatrix(stereo.left_img, position));


	namedWindow("Disp");
	namedWindow("XYZ");
	int key = 0;
	while (key != 'q') {
		vector<Point3f> real_world;
		vector<Point> points;
		Contours detected_contours;
		vector<Point2f> detected_pts;
		Mat disp8, xyz;
		
		stereo.newImage();
		visio.getDetectedPosition(stereo.left_img, detected_pts, detected_contours);
		if (detected_pts.size() > 0) {
			//Disparity
			stereo.getDisparity(disp);
			Point p = detected_pts[0];
			points.push_back(p);
			normalize(disp, disp8, 0, 255, CV_MINMAX, CV_8U);

			//Depth
			Mat Q = stereo.getQ();
			reprojectImageTo3D(disp, xyz, Q);
			vector<Mat> channels;
			split(xyz, channels);
			for(int i=0; i<3; i++) {
				normalize(channels[i], channels[i], 0, 255, CV_MINMAX, CV_8U);
			}
			merge(channels, xyz);
			imshow("XYZ", xyz);
			imshow("Disp", disp8);
		}
		imshow("Left", stereo.left_img);
		key = waitKey(20);
	}
}

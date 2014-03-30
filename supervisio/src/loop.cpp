#include <opencv2/opencv.hpp>
#include "traitement/traitement.h"
#include "traitement/gui.h"
#include "stereo/stereo.h"
#include "loop.h"

using namespace cv;

void perspectiveOnlyLoop(int index){
	VideoCapture cam(index);
	 if(!cam.isOpened())  // check if we succeeded
		return;

	Visio visio;
	visio.setMinSize(1000);
	visio.setChessboardSize(Size(9,6));

	int s_max(255), v_max(255);
	int h_min_r(110), h_max_r(140), s_min_r(100), v_min_r(70);
	int h_min_y(90), h_max_y(110), s_min_y(110), v_min_y(70), epsilon(7), key = -1;
	bool calibrating = !visio.loadTransformMatrix();

	namedWindow("parameters");
	namedWindow("origin");
	namedWindow("persp");

	createTrackbar("h_min_y", "parameters", &h_min_y, 180);
	createTrackbar("h_max_y", "parameters", &h_max_y, 180);
	createTrackbar("s_min_y", "parameters", &s_min_y, 255);
	createTrackbar("v_min_y", "parameters", &v_min_y, 255);
	createTrackbar("h_min_r", "parameters", &h_min_r, 180);
	createTrackbar("h_max_r", "parameters", &h_max_r, 180);
	createTrackbar("s_min_r", "parameters", &s_min_r, 255);
	createTrackbar("v_min_r", "parameters", &v_min_r, 255);
	createTrackbar("epsilon", "parameters", &epsilon, 100);

	Scalar c_red(0,0,255), c_blue(255, 0, 0), c_yel(0,110,130);
	vector<Point2f> position;
	position.push_back(Point2f(108,119));
	position.push_back(Point2f(108,328));
	position.push_back(Point2f(239,119));
	position.push_back(Point2f(239,328));
	for(;;) { //int i=0; i>=0; i++) {
		vector<vector<Point> > detected_contours_yel, detected_contours_red;
		vector<Point2f> detected_pts_yel, detected_pts_red;
		Mat frame, persp;
		cam >> frame;

		if (key == 'c') {
			calibrating = !calibrating;
		}
		if (key == 's') {
			visio.saveTransformMatrix();
		}
		if (key == 'l') {
			visio.loadTransformMatrix();
		}
		
		if (calibrating) {
			visio.computeTransformMatrix(frame, position, &frame);
			imshow("origin", frame);
		}
		else {
			Scalar min_r(h_min_r,s_min_r,v_min_r), max_r(h_max_r,s_max,v_max);
			Scalar min_y(h_min_y,s_min_y,v_min_y), max_y(h_max_y,s_max,v_max);
			visio.setYelParameters(min_y, max_y);
			visio.setRedParameters(min_r, max_r);

			warpPerspective(frame, persp, visio.getQ(), frame.size());
			visio.setColor(yellow);
			visio.getDetectedPosition(frame, detected_pts_yel, detected_contours_yel);
			visio.setColor(red);
			visio.getDetectedPosition(frame, detected_pts_red, detected_contours_red);
			
			drawContours(frame, detected_contours_yel, -1, c_yel, 2);
			drawContours(frame, detected_contours_red, -1, c_red, 2);

			vector<Triangle> tri;
			visio.triangles(frame, tri, Rect(0,0,1000,1000));
			for(int i=0; i<tri.size(); i++) {
				string txt = "TRIANGLE";
				Scalar color;
				if (tri[i].color == yellow) 
					color = Scalar(0, 195, 210);
				else if (tri[i].color == red)
					color = Scalar(0, 0, 255);

				drawObject(tri[i].coords.x, tri[i].coords.y, persp, txt, color, true);
				 //Repr de l'angle
				int len = 100;
				Point2f angle(len*cos(tri[i].angle), len*sin(tri[i].angle));
				angle += tri[i].coords;
				line(persp, tri[i].coords, angle, c_blue, 2);
				vector<vector<Point> > t; t.push_back(convertFtoI(tri[i].contour));
				drawContours(persp, t, -1, c_blue, 2);
			}

	//		resize(persp, persp, Size(600, 600));
			resize(persp, persp, Size(persp.size().width*1.5, persp.size().height*1.5));
			imshow("persp", persp);
			imshow("origin", frame);
		}
		key = waitKey(20);
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

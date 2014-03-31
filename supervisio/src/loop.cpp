#include <opencv2/opencv.hpp>
#include "traitement/traitement.h"
#include "traitement/gui.h"
#include "stereo/stereo.h"
#include "loop.h"
#include "global.h"

using namespace cv;

template <typename T>
void perspectiveOnlyLoop(T index_or_filename){
	VideoCapture cam(index_or_filename);
	 if(!cam.isOpened())  // check if we succeeded
		return;

	Visio visio;
	visio.setChessboardSize(Size(9,6));

	int size_min(5000), max_diff_triangle_edge(30);
	int h_min_y(YEL_HUE_MIN), h_max_y(YEL_HUE_MAX), s_min_y(YEL_SAT_MIN), s_max_y(YEL_SAT_MAX), v_min_y(YEL_VAL_MIN), v_max_y(YEL_VAL_MAX);
	int h_min_r(RED_HUE_MIN), h_max_r(RED_HUE_MAX), s_min_r(RED_SAT_MIN), s_max_r(RED_SAT_MAX), v_min_r(RED_VAL_MIN), v_max_r(RED_VAL_MAX);
	int h_min_b(BLK_HUE_MIN), h_max_b(BLK_HUE_MAX), s_min_b(BLK_SAT_MIN), s_max_b(BLK_SAT_MAX), v_min_b(BLK_VAL_MIN), v_max_b(BLK_SAT_MAX);
	int epsilon(7), key = -1;
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
	createTrackbar("h_min_b", "parameters", &h_min_b, 180);
	createTrackbar("h_max_b", "parameters", &h_max_b, 180);
	createTrackbar("s_min_b", "parameters", &s_min_b, 255);
	createTrackbar("s_max_b", "parameters", &s_max_b, 255);
	createTrackbar("v_min_b", "parameters", &v_min_b, 255);
	createTrackbar("v_max_b", "parameters", &v_max_b, 255);
	createTrackbar("epsilon", "parameters", &epsilon, 100);
	createTrackbar("is equi", "parameters", &max_diff_triangle_edge, 100);
	createTrackbar("size_min", "parameters", &size_min, 20000);

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
			Scalar min_r(h_min_r,s_min_r,v_min_r), max_r(h_max_r,s_max_r,v_max_r);
			Scalar min_y(h_min_y,s_min_y,v_min_y), max_y(h_max_y,s_max_y,v_max_y);
			Scalar min_b(h_min_b,s_min_b,v_min_b), max_b(h_max_b,s_max_b,v_max_b);
			visio.setMinSize(size_min);
			visio.setMaxDiffTriangleEdget(max_diff_triangle_edge);
			visio.setEpsilonPoly(epsilon);
			visio.setYelParameters(min_y, max_y);
			visio.setRedParameters(min_r, max_r);
			visio.setBlkParameters(min_b, max_b);

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
				string txt = intToString(tri[i].size);
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

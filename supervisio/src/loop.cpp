#include <opencv2/opencv.hpp>
#include "traitement/traitement.h"
#include "traitement/gui.h"
#include "communication/com.h"
#include "loop.h"
#include "global.h"

//Le fichier dégueu pour faire moins degueu

using namespace cv;

void communication(int index, string path_to_conf, bool save) {
	Visio visio(index, path_to_conf, save);
	if (!visio.isCalibrated()) {
		cerr << "ERROR : Uncalibarted" << endl;
		return;
	}
	if (visio.getDistortMode() != none) {
		cerr << "INFO : Starting visio WITH distortion correction" << endl;
	} else {
		cerr << "INFO : Starting visio WITHOUT distortion correction" << endl;
	}
	comLoop(visio);
}

void calibration(int index, string path) {
	Visio visio(index, path);
	visio.setChessboardSize(Size(9,6));
	if (visio.camCalibrate(25)) 
		visio.saveCameraMatrix();
	if (visio.camPerspective())
		visio.saveTransformMatrix();
}

void getColor(int event, int x, int y, int, void* img_mat) {
	if (event == EVENT_LBUTTONDOWN) {
		Mat *img = reinterpret_cast<Mat*> (img_mat);
		Mat hsv;
		cvtColor(*img, hsv, CV_BGR2HSV);
		Scalar pt(hsv.at<Vec3b>(x,y)[0],hsv.at<Vec3b>(x,y)[1],hsv.at<Vec3b>(x,y)[2]);
		cout << x << ":" << y << " = " << pt << endl;
	}
}

void perspectiveOnlyLoop(int index, string path){
	Mat frame;
	Visio visio(index, path);
	visio.setChessboardSize(Size(9,6));

	int size_min(5000), max_diff_triangle_edge(MAX_DIFF_TRI_EDGE);
	int h_min_y(YEL_HUE_MIN), h_max_y(YEL_HUE_MAX), s_min_y(YEL_SAT_MIN), s_max_y(YEL_SAT_MAX), v_min_y(YEL_VAL_MIN), v_max_y(YEL_VAL_MAX);
	int h_min_r(RED_HUE_MIN), h_max_r(RED_HUE_MAX), s_min_r(RED_SAT_MIN), s_max_r(RED_SAT_MAX), v_min_r(RED_VAL_MIN), v_max_r(RED_VAL_MAX);
	int h_min_b(BLK_HUE_MIN), h_max_b(BLK_HUE_MAX), s_min_b(BLK_SAT_MIN), s_max_b(BLK_SAT_MAX), v_min_b(BLK_VAL_MIN), v_max_b(BLK_VAL_MAX);
	int epsilon(EPSILON_POLY*100), key = -1;

	namedWindow("parameters");
	namedWindow("parameters2");
	namedWindow("origin");
	namedWindow("persp");

	setMouseCallback("origin", getColor, &frame);

	createTrackbar("h_min_y", "parameters", &h_min_y, 180);
	createTrackbar("h_max_y", "parameters", &h_max_y, 180);
	createTrackbar("s_min_y", "parameters", &s_min_y, 255);
	createTrackbar("v_min_y", "parameters", &v_min_y, 255);
	createTrackbar("v_max_y", "parameters", &v_max_y, 255);
	createTrackbar("h_min_r", "parameters", &h_min_r, 180);
	createTrackbar("h_max_r", "parameters", &h_max_r, 180);
	createTrackbar("s_min_r", "parameters", &s_min_r, 255);
	createTrackbar("v_min_r", "parameters", &v_min_r, 255);
	createTrackbar("v_max_r", "parameters", &v_max_r, 255);
	if(ENABLE_BLK) {
		createTrackbar("h_min_b", "parameters2", &h_min_b, 180);
		createTrackbar("h_max_b", "parameters2", &h_max_b, 180);
		createTrackbar("s_min_b", "parameters2", &s_min_b, 255);
		createTrackbar("s_max_b", "parameters2", &s_max_b, 255);
		createTrackbar("v_min_b", "parameters2", &v_min_b, 255);
		createTrackbar("v_max_b", "parameters2", &v_max_b, 255);
	}
	createTrackbar("epsilon", "parameters2", &epsilon, 100);
	createTrackbar("is equi", "parameters2", &max_diff_triangle_edge, 100);
	createTrackbar("size_min", "parameters2", &size_min, 20000);

	Scalar c_red(0,0,255), c_blue(255, 0, 0), c_yel(0,110,130);
	for(;;) { //int i=0; i>=0; i++) {
		vector<vector<Point> > detected_contours_yel, detected_contours_red, detected_contours_blk;
		vector<Point2f> detected_pts_yel, detected_pts_red, detected_pts_blk;
		Mat frame_ori, persp;
		frame_ori = visio.getImg();

		if (key == 's') {
			visio.saveTransformMatrix();
		}
		if (key == 'l') {
			visio.loadTransformMatrix();
		}
		
		else {
			Scalar min_r(h_min_r,s_min_r,v_min_r), max_r(h_max_r,s_max_r,v_max_r);
			Scalar min_y(h_min_y,s_min_y,v_min_y), max_y(h_max_y,s_max_y,v_max_y);
			Scalar min_b(h_min_b,s_min_b,v_min_b), max_b(h_max_b,s_max_b,v_max_b);
			visio.setMinSize(size_min);
			visio.setMaxDiffTriangleEdget(max_diff_triangle_edge);
			visio.setEpsilonPoly(epsilon/100.0);
			visio.setYelParameters(min_y, max_y);
			visio.setRedParameters(min_r, max_r);
			visio.setBlkParameters(min_b, max_b);

			Mat frame_hsv;
			cvtColor(frame_ori, frame_hsv, CV_BGR2HSV);
			undistort(frame_ori, frame, visio.getCM(), visio.getD());
			warpPerspective(frame, persp, visio.getQ(), Size(1000,1000));
			visio.setColor(yellow);
			visio.getDetectedPosition(frame_hsv, detected_pts_yel, detected_contours_yel);
			visio.setColor(red);
			visio.getDetectedPosition(frame_hsv, detected_pts_red, detected_contours_red);
			if (ENABLE_BLK) {
				visio.setColor(black);
				visio.getDetectedPosition(frame_hsv, detected_pts_blk, detected_contours_blk);
				drawContours(frame, detected_contours_blk, -1, Scalar(255,255,0), 2);
			}
			
			drawContours(frame, detected_contours_yel, -1, c_yel, 2);
			drawContours(frame, detected_contours_red, -1, c_red, 2);

			vector<Triangle> tri;
			visio.trianglesFromImg(frame_hsv, tri);
			for(int i=0; i<tri.size(); i++) {
				string txt = intToString(tri[i].size);
				Scalar color;
				if (tri[i].color == yellow) 
					color = Scalar(0, 195, 210);
				else if (tri[i].color == red)
					color = Scalar(0, 0, 255);
				else if (tri[i].color == black) {
					color = Scalar(0,0,0);
				}

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
			resize(persp, persp, Size(900,900));
			imshow("persp", persp);
			imshow("undistort", frame);
			imshow("origin", frame_ori);
		}
		key = waitKey(20);
	}
}

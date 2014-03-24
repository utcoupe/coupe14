#include "traitement.h"
#include "gui.h"

#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/types_c.h>

using namespace std;

Persp::Persp() : min(0,0,0), max(0,0,0) {
	init();
}

Persp::Persp(Scalar min, Scalar max) {
	this->min = min;
	this->max = max;
	init();
}

void Persp::init() {
	chessboard_size = Size(7,6);
	min_size = 100;
	calibrated = false;
}

void Persp::detectColor(const Mat& img, Mat& out) {
	Mat hsv;
	cvtColor(img, hsv, CV_RGB2HSV);
	if (min.val[0] > max.val[0]) { //car les teintes sont circulaires
		//Si la détection "fait le tour" de la teinte, on la décale pour rester sur l'intervale 0-180
		add(hsv, Scalar(-max.val[0], 0, 0), hsv);
		min.val[0] -= max.val[0];
		max.val[0] = 180;
	}
	inRange(hsv, min, max, out);
}

Contours Persp::getContour(const Mat& img) {
	Contours contours;
	Mat thresh;
	detectColor(img, thresh);
	Mat kernel = getStructuringElement(MORPH_ELLIPSE, Size(10,10));
	erode(thresh, thresh, kernel);
	dilate(thresh, thresh, kernel);

	//edges is a temporary variable here
	findContours(thresh, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
	return contours;
}

bool Persp::computeTransformMatrix(const Mat &img, const vector<Point2f> real_positions, Mat *out) {
	Mat gray;
	bool pattern_found = false;
	vector<Point2f> corners, ext_corn;
	cvtColor(img, gray, CV_BGR2GRAY);
	pattern_found = findChessboardCorners(gray, chessboard_size, corners, CALIB_CB_ADAPTIVE_THRESH + CALIB_CB_NORMALIZE_IMAGE + CALIB_CB_FAST_CHECK);
	if (pattern_found) {
		//On recupere les 4 points exterieurs de l'échiquier
		ext_corn.push_back(corners[0]);
		ext_corn.push_back(corners[chessboard_size.width - 1]);
		ext_corn.push_back(corners[(chessboard_size.width)*(chessboard_size.height - 1)]);
		ext_corn.push_back(corners[chessboard_size.height - 1 + (chessboard_size.width - 1)*(chessboard_size.height)]);
		cornerSubPix(gray, ext_corn, Size(11, 11), Size(-1, -1), TermCriteria(CV_TERMCRIT_EPS + CV_TERMCRIT_ITER, 30, 0.1));
		perspectiveMatrix = getPerspectiveTransform(ext_corn, real_positions);
		calibrated = true;
		if (out != 0) { //La matrice ou existe
			for(int i=0; i<4; i++) {
				drawObject(ext_corn[i].x, ext_corn[i].y, *out, intToString(i));
			}
		}

	}
	else {
		perspectiveMatrix =  Mat::eye(3, 3, CV_64F);
		calibrated = false;
		if (out != 0) { //La matrice ou existe
			drawChessboardCorners(*out, chessboard_size, corners, pattern_found);
		}
	}
	return calibrated;
}

void Persp::getDetectedPosition(const Mat& img, vector<Point2f>& detected_pts, Contours& detected_contours) {
	Contours contours = getContour(img);
	float x, y;
	for(int i=0 ; i < contours.size(); i++){
		Moments moment = moments(contours[i]);
		if (moment.m00 > min_size) {
			x = moment.m10 / moment.m00;
			y = moment.m01 / moment.m00;
			detected_pts.push_back(Point2f(x,y));
			detected_contours.push_back(contours[i]);
		}
	}
}

void Persp::warpPerspective(const Mat& frame, Mat& out, Size size) {
	cv::warpPerspective(frame, out, perspectiveMatrix, size);
}

//SETTER

void Persp::setParameters(Scalar min, Scalar max, int size) {
	this->min = min;
	this->max = max;
	if (size > 0) {
		min_size = size;
	}
}

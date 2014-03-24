#include "traitement.h"
#include "gui.h"

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/types_c.h>

using namespace std;

Visio::Visio() : min(0,0,0), max(0,0,0) {
	init();
}

Visio::Visio(Scalar min, Scalar max) {
	this->min = min;
	this->max = max;
	init();
}

void Visio::init() {
	chessboard_size = Size(7,6);
	min_size = 100;
	calibrated = false;
}

void Visio::detectColor(const Mat& img, Mat& out) {
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

Contours Visio::getContour(const Mat& img) {
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

bool Visio::computeTransformMatrix(const Mat &img, const vector<Point2f> real_positions, Mat *out) {
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

void Visio::saveTransformMatrix() {
	cout << "Saving calibration data" << endl;
	if (!calibrated) {
		cerr << "ERROR : Uncalibrated camera" << endl;
		return;
	}
	FileStorage fs("calibration_persp.yml", FileStorage::WRITE);
	fs << "Q" << perspectiveMatrix;
	fs.release();
}

bool Visio::loadTransformMatrix() {
	cout << "Loading calibration data" << endl;
	FileStorage fs("calibration_persp.yml", FileStorage::READ);
	if (!fs.isOpened()) {
		cerr << "ERROR : Couldn't find calibration_persp.yml" << endl;
		return false;
	}
	fs.release();
	calibrated = true;
	return true;
}

void Visio::getDetectedPosition(const Mat& img, vector<Point2f>& detected_pts, Contours& detected_contours) {
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

void Visio::getRealWorldPosition(const Mat& img, vector<Point2f>& detected_pts, Contours& detected_contours, Rect ROI) {
	getDetectedPosition(img, detected_pts, detected_contours);
	perspectiveTransform(detected_pts, detected_pts, perspectiveMatrix);
	for(int i=0; i < detected_contours.size(); i++) {
		perspectiveTransform(detected_contours, detected_contours, perspectiveMatrix);
	}
}

//SETTER

void Visio::setParameters(Scalar min, Scalar max, int size) {
	this->min = min;
	this->max = max;
	if (size > 0) {
		min_size = size;
	}
}

//GETTER

Mat Visio::getQ() {
	return perspectiveMatrix;
}

#include "traitement.h"
#include "gui.h"

#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/types_c.h>

using namespace std;

void detectColor(const Mat& img, Mat& out, Scalar min, Scalar max) {
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

Contours getContour(const Mat& img, Scalar min, Scalar max) {
	Contours contours;
	Mat thresh;
	detectColor(img, thresh, min, max);
	Mat kernel = getStructuringElement(MORPH_ELLIPSE, Size(10,10));
	erode(thresh, thresh, kernel);
	dilate(thresh, thresh, kernel);

	//edges is a temporary variable here
	findContours(thresh, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
	return contours;
}

Mat getTransformMatrix(const Mat &img, const vector<Point2f> real_positions) {
	Mat gray, perspectiveMatrix;
	bool pattern_found = false;
	vector<Point2f> corners, ext_corn, ordered_corn, ordered_real;
	cvtColor(img, gray, CV_BGR2GRAY);
	pattern_found = findChessboardCorners(gray, Size(7,7), corners, CALIB_CB_ADAPTIVE_THRESH + CALIB_CB_NORMALIZE_IMAGE + CALIB_CB_FAST_CHECK);
	if (pattern_found) {
		//On recupere les 4 points exterieurs de l'échiquier
		ext_corn.push_back(corners[0]);
		ext_corn.push_back(corners[6]);
		ext_corn.push_back(corners[0 + 6*7]);
		ext_corn.push_back(corners[6 + 6*7]);
		cornerSubPix(gray, ext_corn, Size(11, 11), Size(-1, -1), TermCriteria(CV_TERMCRIT_EPS + CV_TERMCRIT_ITER, 30, 0.1));
		//On reordonne les position
		ordered_corn = orderPoints(ext_corn);
		ordered_real = orderPoints(real_positions);

		perspectiveMatrix = getPerspectiveTransform(ordered_corn, ordered_real);
	}
	else {
		perspectiveMatrix =  Mat::eye(3, 3, CV_64F);
	}
	return perspectiveMatrix;
}

void getDetectedPosition(const Mat& img, vector<Point2f>& detected_pts, Contours& detected_contours, Scalar min, Scalar max, int min_size) {
	Contours contours = getContour(img, min, max);
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

vector<Point2f> orderPoints(const vector<Point2f> &pts) {
	vector<Point2f> ordered;
	int dist[4], min=0, max=0, second=0, third=0;
	for (int i=0; i<4; i++){
		dist[i] = pts[i].x + pts[i].y;
	}
	for (int i=1; i<4; i++){
		if (dist[i] < dist[min])
			min = i;
		if (dist[i] > dist[max])
			max = i;
	}
	second = min;
	for (int i=0; i<4; i++) {
		if (i != max and i != min) {
			if (pts[i].x > pts[second].x){
				second = i;
				third = 6 - max - min - i;
			}
		}
	}
	ordered.push_back(pts[min]);
	ordered.push_back(pts[second]);
	ordered.push_back(pts[third]);
	ordered.push_back(pts[max]);
	return ordered;
}

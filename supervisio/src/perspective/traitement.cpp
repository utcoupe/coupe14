#include "traitement.h"
#include "gui.h"

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/types_c.h>

using namespace std;

/******************
 * CONSTRUCTEUR   *
 * ****************/

Visio::Visio() : 
	color(red), calibrated(false), min_size(100),
	chessboard_size(Size(7,6)), epsilon_poly(3) {
	init();
}

void Visio::init() {
	setRedParameters(Scalar(0,70,70), Scalar(30, 255, 255));
	setYelParameters(Scalar(90,70,70), Scalar(110, 255, 255));
	erode_dilate_kernel = getStructuringElement(MORPH_ELLIPSE, Size(10,10));
}

/**********
 * PUBLIC *
 * ********/

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
	erode(out, out, erode_dilate_kernel);
	dilate(out, out, erode_dilate_kernel);

}

void Visio::getContour(const Mat& img, vector<vector<Point> > contours) {
	Mat thresh;
	detectColor(img, thresh);
	findContours(thresh, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
}

//Renvoit positions et contours de la couleur détectée dans l'image en argument
int Visio::getDetectedPosition(const Mat& img, vector<Point2f>& detected_pts, vector<vector<Point> >& detected_contours) {
	vector<vector<Point> > contours;
	getContour(img, contours);
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
	return detected_pts.size();
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

void Visio::polyDegree(const vector<vector<Point> >& contours, vector<int> degree, double epsilon) {
	vector<vector<Point> > approx;
	polyDegree(contours, degree, approx, epsilon);
}

void Visio::polyDegree(const vector<vector<Point> >& contours, vector<int> degree, vector<vector<Point> > approx, double epsilon) {
	if (epsilon < 0)
		epsilon = epsilon_poly;
	for(int i=0; i < contours.size(); i++) {
		vector<Point> poly;
		approxPolyDP(contours[i], poly, epsilon, true);
		approx.push_back(poly);
		int size = poly.size();
		degree.push_back(size);
	}
}

int Visio::triangles(const Mat& img, vector<Triangle>& triangles, Rect area) {
	vector<vector<Point> >detected_pts_red, contours_red, detected_pts_yel, contours_yel; 
	Mat persp;
	int nb_triangles = 0;
	//Transformation de l'image
	//TODO coordonnées negatives
	Size area_temp(area.width, area.height);
	warpPerspective(img, persp, perspectiveMatrix, area_temp);
	//Analyse triangles rouges
	nb_triangles += trianglesColor(persp, triangles, red);
	nb_triangles += trianglesColor(persp, triangles, yellow);
	//TODO triangles vus de dessus, entierement noirs
	return nb_triangles;
}

//FILE MANAGER

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

//SETTER

void Visio::setRedParameters(Scalar min, Scalar max) {
	red_min = min;
	red_max = max;
	if (color == red) {
		setParameters(red_min, red_max);
	}
}

void Visio::setYelParameters(Scalar min, Scalar max) {
	yel_min = min;
	yel_max = max;
	if (color == yellow) {
		setParameters(yel_min, yel_max);
	}
}

void Visio::setMinSize(int size) {
	min_size = size;
}

void Visio::setColor(Color color) {
	if (color == yellow) {
		min = yel_min;
		max = yel_max;
	}
	else if (color == red) {
		min = red_min;
		max = red_max;
	}
	this->color = color;
}

void Visio::setErodeDilateKernel(Mat kernel) {
	erode_dilate_kernel = kernel;
}

void Visio::setEpsilonPoly(double ep) {
	epsilon_poly = ep;
}

//GETTER

Mat Visio::getQ() {
	return perspectiveMatrix;
}

//AFFICHAGE ET DEBUG

//Renvoit les positions dans le repère du monde réel de la couleur dans l'imgae en argument
int Visio::getRealWorldPosition(const Mat& img, vector<Point2f>& detected_pts) {
	detected_pts.clear();
	vector<vector<Point> > contours;
	if (getDetectedPosition(img, detected_pts, contours) > 0) {
		perspectiveTransform(detected_pts, detected_pts, perspectiveMatrix);
	}
	return detected_pts.size();
}

/***********
 * PRIVATE *
 * *********/

void Visio::setParameters(Scalar min, Scalar max, int size) {
	this->min = min;
	this->max = max;
	if (size > 0) {
		min_size = size;
	}
}

//Fonction à usage unique pour rendre le code plus clair. Detecte des triangles dans une image
//triangles n'est pas effacé, les triangles trouvés sont ajoutés
int Visio::trianglesColor(const Mat& img, vector<Triangle>& triangles, Color color) {
	vector<vector<Point> > contours;
	vector<Point2f> detected_pts;
	int nb_triangles = 0, detected_size;
	setColor(color);
	if (detected_size = getDetectedPosition(img, detected_pts, contours) > 0) {
		vector<int> degree;
		//Calcul du nombre de polylignes
		polyDegree(contours, degree);
		//Pour chaque contour
		for(int i=0; i < detected_size; i++) {
			//Si c'est un triangle
			if (degree[i] == 3) {
				nb_triangles++;
				Triangle tri;
				tri.color == color;
				//Si le triangle est couché
				if(contourArea(contours[i]) > min_down_size) {
					tri.isDown = true;
				}
				else {
					tri.isDown = false;
				}
				triangles.push_back(tri);
			}
		}
	}
	return nb_triangles;
}



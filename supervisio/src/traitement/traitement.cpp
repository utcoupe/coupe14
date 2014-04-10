#include "traitement.h"
#include "../global.h"
#include "gui.h"
#include "timings.h"

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/types_c.h>

using namespace std;

/******************
 * CONSTRUCTEUR   *
 * ****************/

Visio::Visio(VideoCapture& cam) : 
	color(red), min_size(500),
	chessboard_size(Size(9,6)), epsilon_poly(0.04),
	max_diff_triangle_edge(50), camera(cam),
	size_frame(camera.get(CV_CAP_PROP_FRAME_WIDTH), camera.get(CV_CAP_PROP_FRAME_HEIGHT)){
	init();
}

void Visio::init() {
	setRedParameters(Scalar(RED_HUE_MIN, RED_SAT_MIN, RED_VAL_MIN), Scalar(RED_HUE_MAX, RED_SAT_MAX, RED_VAL_MAX));
	setYelParameters(Scalar(YEL_HUE_MIN, YEL_SAT_MIN, YEL_VAL_MIN), Scalar(YEL_HUE_MAX, YEL_SAT_MAX, YEL_VAL_MAX));
	setBlkParameters(Scalar(BLK_HUE_MIN, BLK_SAT_MIN, BLK_VAL_MIN), Scalar(BLK_HUE_MAX, BLK_SAT_MAX, BLK_VAL_MAX));
	erode_dilate_kernel = getStructuringElement(MORPH_ELLIPSE, Size(10,10));
	trans_calibrated = loadTransformMatrix();
	cam_calibrated = loadCameraMatrix();
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

void Visio::getContour(const Mat& img, vector<vector<Point> >& contours) {
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


void Visio::polyDegree(const vector<vector<Point> >& contours, vector<int>& degree, double epsilon) {
	if (epsilon < 0)
		epsilon = epsilon_poly;
	for(int i=0; i < contours.size(); i++) {
		vector<Point> poly;
		approxPolyDP(contours[i], poly, arcLength(contours[i], true)*epsilon, true);
		int size = poly.size();
		degree.push_back(size);
	}
}

void Visio::polyDegree(const vector<vector<Point> >& contours, vector<int>& degree, vector<vector<Point> >& approx, double epsilon) {
	vector<vector<Point> > temp;
	if (epsilon < 0)
		epsilon = epsilon_poly;
	for(int i=0; i < contours.size(); i++) {
		vector<Point> poly;
		approxPolyDP(contours[i], poly, arcLength(contours[i], true)*epsilon, true);
		temp.push_back(poly);
		int size = poly.size();
		degree.push_back(size);
	}
	approx = temp;
}

int Visio::trianglesFromImg(const Mat& img, vector<Triangle>& triangles) {
	int nb_triangles = 0;
	nb_triangles += trianglesColor(img, triangles, red);
	nb_triangles += trianglesColor(img, triangles, yellow);
	//triangles vus de dessus, entierement noirs, seulement si on ne detecte rien d'autre
	if (ENABLE_BLK && nb_triangles == 0) {
		nb_triangles += trianglesColor(img, triangles, black);
	}
	return nb_triangles;
}

int Visio::triangles(vector<Triangle>& triangles) {
	Mat img;
	//for(int i=0; i<6; i++) camera >> img; //Hack provisoire
	while (camera.grab()) { cerr << "Grabbing frame" << endl; } //A TESTER
	//for(int i=0; i<6; i++) camera.grab(); //Hack provisoire, porbablement bon
	camera.retrieve(img);
	return trianglesFromImg(img, triangles);
}

/*********************
 *	UI CALIBRATION	 *
 *	******************/

bool Visio::computeTransformMatrix(const Mat &img, const vector<Point2f> real_positions, Mat *out) {
	Mat gray;
	bool pattern_found = false;
	bool &calibrated = trans_calibrated;
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

void Visio::camPerspective() {
	vector<Point2f> position;
	position.push_back(Point2f(300,300));
	position.push_back(Point2f(300,562));
	position.push_back(Point2f(482,300));
	position.push_back(Point2f(482,562));
	Mat img;
	camera >> img;
	namedWindow("Perspective");
	while (!computeTransformMatrix(img, position, &img)) {
		imshow("Perspective", img);
	}
	destroyWindow("Perspective");
}

bool Visio::camCalibrate(int nbr_of_views) {
	//points reels et image pour la calibration
	vector<vector<Point3f> > objectPoints;
	vector<vector<Point2f> > imagePoints;

	//position des points corners (dimension abstraite)
	vector<Point3f> obj;
	for (int j=0; j<chessboard_size.height * chessboard_size.width; j++)
	{
		obj.push_back(Point3f(j/chessboard_size.width, j%chessboard_size.width, 0.0f));
	}
	//Calibration caméra gauche
	namedWindow("Calibration");
	int key = 0;
	bool capture = false;
	for(int success=0; success < nbr_of_views;) {
		Mat img, gray;
		vector<Point2f> corners;
		bool pattern_found;

		//A-t-on appuyé sur 'c' pour capturer cette frame ?
		if (key == 'c') {
			capture = true;
		}
		if (key == 'q') {
			cerr << "WARNING : Calibration failed" << endl;
			destroyWindow("Calibration");
			return false;
		}
		//Capture d'image
		camera >> img;
		cvtColor(img, gray, CV_BGR2GRAY);
		pattern_found = findChessboardCorners(gray, chessboard_size, corners, CALIB_CB_ADAPTIVE_THRESH + CALIB_CB_NORMALIZE_IMAGE + CALIB_CB_FAST_CHECK);
		if (pattern_found) {
			cornerSubPix(gray, corners, Size(11, 11), Size(-1, -1), TermCriteria(CV_TERMCRIT_EPS + CV_TERMCRIT_ITER, 30, 0.1));
		}
		//Retour graphique
		drawChessboardCorners(img, chessboard_size, corners, pattern_found);
		stringstream txt;
		txt << "Captures effectuees : " << success << "/" << nbr_of_views;
		putText(img, txt.str(), Point(10,10),1,1,Scalar(0,255,0),1);
		//Si l'echiquier est détecté dans les deux images et que l'on souhaite capturer cette frame
		if (capture && pattern_found) {
			success++;
			objectPoints.push_back(obj);
			imagePoints.push_back(corners);
			capture = false;
		}
		imshow("Calibration", img);
		key = waitKey(20);
	}
	cout << "Beginning processing" << endl;
	destroyWindow("Calibration");
	vector<Mat> empty;
	calibrateCamera(objectPoints, imagePoints, size_frame, CM, D, empty, empty);
	cout << "Done !" << endl;
	return true;
}

//FILE MANAGER

bool Visio::loadTransformMatrix() {
	bool &calibrated = trans_calibrated;
	cout << "Loading transform data" << endl;
	FileStorage fs("calibration_persp.yml", FileStorage::READ);
	if (!fs.isOpened()) {
		cerr << "ERROR : Couldn't find calibration_persp.yml" << endl;
		return false;
	}
	fs["Q"] >> perspectiveMatrix;
	fs.release();
	calibrated = true;
	return true;
}

bool Visio::loadCameraMatrix() {
	bool &calibrated = cam_calibrated;
	cout << "Loading camera data" << endl;
	FileStorage fs("calibration_camera.yml", FileStorage::READ);
	if (!fs.isOpened()) {
		cerr << "ERROR : Couldn't find calibration_camera.yml" << endl;
		return false;
	}
	fs["D"] >> D;
	fs["CM"] >> CM;
	fs["size"] >> size_frame;
	fs.release();
	calibrated = true;
	return true;
}

void Visio::saveTransformMatrix() {
	cout << "Saving transform data" << endl;
	if (!trans_calibrated) {
		cerr << "ERROR : Uncalibrated trasnform" << endl;
		return;
	}
	FileStorage fs("calibration_persp.yml", FileStorage::WRITE);
	fs << "Q" << perspectiveMatrix;
	fs.release();
}

void Visio::saveCameraMatrix() {
	cout << "Saving camera data" << endl;
	if (!cam_calibrated) {
		cerr << "ERROR : Uncalibrated camera" << endl;
		return;
	}
	FileStorage fs("calibration_camera.yml", FileStorage::WRITE);
	fs << "D" << D;
	fs << "CM" << CM;
	fs << "size" << size_frame;
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

void Visio::setBlkParameters(Scalar min, Scalar max) {
	blk_min = min;
	blk_max = max;
	if (color == black) {
		setParameters(blk_min, blk_max);
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
	else if (color == black) {
		min = blk_min;
		max = blk_max;
	}
	this->color = color;
}

void Visio::setErodeDilateKernel(Mat kernel) {
	erode_dilate_kernel = kernel;
}

void Visio::setEpsilonPoly(double ep) {
	epsilon_poly = ep;
}

void Visio::setChessboardSize(Size s) {
	chessboard_size = s;
}

void Visio::setMaxDiffTriangleEdget(int max) {
	max_diff_triangle_edge = max;
}

//GETTER

Mat Visio::getQ() {
	return perspectiveMatrix;
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
	if (color == black && ENABLE_BLK) { cerr << "Appel à la fonction de détection couleur noir alors que ENABLE_BLK=false" << endl; }
	vector<vector<Point> > contours;
	vector<Point2f> detected_pts;
	int nb_triangles = 0, detected_size;
	setColor(color);
	timings();
	if ((detected_size = getDetectedPosition(img, detected_pts, contours)) > 0) {
		timings("\tgetDetectedPosition : ");
		vector<Point2f> points_real;
		vector<int> degree;
		//Transformation perspective des points detectes
		perspectiveTransform(detected_pts, points_real, perspectiveMatrix);
		timings("\tPTS perspectiveTransform : ");
		//Calcul du nombre de polylignes
		polyDegree(contours, degree, contours);
		timings("\tpolyDegree : ");
		//Pour chaque contour
		for (int i=0; i < detected_size; i++) {
			//Si c'est un triangle
			if (color != black) {
				if (degree[i] == 3) {
					timings();
					vector<Point2f> contour_real = convertItoF(contours[i]);
					perspectiveTransform(contour_real, contour_real, perspectiveMatrix);
					addTriangle(points_real[i], contour_real, triangles);
					timings("\tTRI perspectiveTransform : ");
					nb_triangles++;
				}
				else if (degree[i] > 3 && degree[i] < 8) {
					timings();
					vector<Point2f> contour_real = convertItoF(contours[i]);
					perspectiveTransform(contour_real, contour_real, perspectiveMatrix);
					timings("\tTRI perspectiveTransform : ");
					//Voir si on a pas plusieurs triangles collés
					nb_triangles += deduceTrianglesFromContour(contour_real, triangles);
					timings("\tdeduceTriangles : ");
				}
			}
			else if (ENABLE_BLK) { //black
				if (degree[i] >= 4){
					vector<Point2f> contour_real = convertItoF(contours[i]);
					perspectiveTransform(contour_real, contour_real, perspectiveMatrix);
					addTriangle(points_real[i], contour_real, triangles);
					nb_triangles++;
				}
			}
		}
	}
	return nb_triangles;
}

void Visio::addTriangle(const Point2f& point_real, const vector<Point2f>& contour_real, vector<Triangle>& triangles) {
	Triangle tri;
	tri.color = color;
	tri.coords = point_real;
	//Calcule de l'angle du triangle
	double dx = contour_real[0].x - tri.coords.x;
	double dy = contour_real[0].y - tri.coords.y; 
	tri.angle = atan2(dy, dx);

	//Modulo 2*PI/3
	while (tri.angle < 0) {
		tri.angle += 2*M_PI/3;
	}
	while (tri.angle > 2*M_PI/3) {
		tri.angle -= 2*M_PI/3;
	}
	//Si le triangle est couché
	if ((tri.size = contourArea(contour_real)) > min_down_size) {
		tri.isDown = true;
	}
	else {
		tri.isDown = false;
	}
	tri.contour = contour_real;
	triangles.push_back(tri);
}

int Visio::deduceTrianglesFromContour(vector<Point2f>& contour_real, vector<Triangle>& triangles) {
	int nb_triangles = 0;
	for (int j=0; j<contour_real.size(); j++) {
		Point2f p1 = contour_real[j];
		for (int k=j+1; k<contour_real.size(); k++) {
			Point2f p2 = contour_real[k];
			for (int l=k+1; l<contour_real.size(); l++) {
				Point2f p3 = contour_real[l];
				if (isEqui(p1, p2, p3)) {
					//Point central
					vector<Point2f> contour_tri;
					contour_tri.push_back(p1);
					contour_tri.push_back(p2);
					contour_tri.push_back(p3);
					Moments moment = moments(contour_tri);
					if (moment.m00 > min_size) {
						Triangle tri;
						nb_triangles++;
						float x = moment.m10 / moment.m00;
						float y = moment.m01 / moment.m00;
						tri.coords = Point2f(x,y);
						tri.color = color;
						//Calcule de l'angle du triangle
						double dx = contour_tri[0].x - tri.coords.x;
						double dy = contour_tri[0].y - tri.coords.y; 
						tri.angle = atan2(dy, dx);

						//Modulo 2*PI/3
						while (tri.angle < 0) {
							tri.angle += 2*M_PI/3;
						}
						while (tri.angle > 2*M_PI/3) {
							tri.angle -= 2*M_PI/3;
						}

						//On ne detecte pas les triangles debout dans ce cas, ce ne serait pas assez fiable
						tri.isDown = false;
						tri.contour = contour_tri;
						triangles.push_back(tri);
						return nb_triangles;
					}
				}
			}
		}
	}
	return nb_triangles;
}

bool Visio::isEqui(Point2f p1, Point2f p2, Point2f p3) {
	double d1 = norm(p1 - p2), d2 = norm(p3 - p2), d3 = norm(p1 - p3);
	if (abs(d1 - d2) < max_diff_triangle_edge && 
		abs(d2 - d3) < max_diff_triangle_edge &&
		abs(d3 - d1) < max_diff_triangle_edge) {
		return true;
	}
	return false;
}


vector<vector<Point2f> > convertItoF(vector<vector<Point> > v) {
	vector<vector<Point2f> > out;
	for(int i=0; i<v.size(); i++) {
		vector<Point2f> vtemp;
		for(int j=0; j<v[i].size(); j++) {
			vtemp.push_back(v[i][j]);
		}
		out.push_back(vtemp);
	}
	return out;
}

vector<Point2f> convertItoF(vector<Point> v) {
	vector<Point2f> out;
	for(int i=0; i<v.size(); i++) {
		out.push_back(v[i]);
	}
	return out;
}

vector<Point> convertFtoI(vector<Point2f> v) {
	vector<Point> out;
	for(int i=0; i<v.size(); i++) {
		out.push_back(v[i]);
	}
	return out;
}

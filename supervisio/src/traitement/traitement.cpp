#include "../global.h"
#include "traitement.h"
#include "gui.h"
#include "timings.h"

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/types_c.h>
#include <thread>
#include <mutex>
#include <unistd.h>

/***************************************************
 *  CLASSE VISIO DE TRAITEMENT GENERAL 
 *
 *  Cette classe effectue toutes les operation
 *  necessaires pour la visio UTCoupe 2014
 *
 *  Dans cette classes toutes les images sont  en HSV
 *
 *  Tests de vitesse du code :
 *  Les durées de transformations affines de 
 *  perspectives sont negligeables. 
 *  La durée de conversion RGB->HSV est ce qui prend
 *  le plus de temps
 *  *************************************************/

using namespace std;

/******************
 * CONSTRUCTEUR   *
 * ****************/

Visio::Visio(int index_cam, string path, bool save_vid) : camera(), save_video(save_vid),
	//Genral
	calib_cam_filename(DEFAULT_CAMERA_MATRIX_FILENAME), calib_detection_filename(DEFAULT_PARAMS_FILENAME), 
	calib_transform_matrix_filename(DEFAULT_PERSPECTIVE_MATRIX_FILENAME), mask_name("mask.jpg"),
	color(red), distort(none), path_to_conf(path), chessboard_size(Size(9,6)), isready(false), is_opened(false),
	index(index_cam),


	//Params par defaut
	min_size(MIN_SIZE), real_min_size(MIN_REAL_SIZE), epsilon_poly(EPSILON_POLY), max_diff_triangle_edge(MAX_DIFF_TRI_EDGE), 

	//Options
	use_mask(USE_MASK) {
	//param cam
	frame_mutex.lock();
	camera.open(index);
	if(!camera.isOpened()) {  // check if we succeeded
		cerr << "Failed to open camera" << endl;
	} else  {
		init();

		cout << "Starting camera " << index << " :" << flush; 
		int ignore = system("v4l2-ctl -V | sed 's/\tWidth\\/Height  ://p' -n | tr '\n' ' @'");
		ignore = system("v4l2-ctl -P | sed 's/\tFrames per second://p' -n | tr '\n' ' '");
		cout << "distort ";
		if (distort == none) {
			cout << "none";
		} else if (distort == points) { 
			cout << "points";
		} else if (distort == image) {
			cout << "image";
		}
		cout << endl;

		if (save_video) {
			init_writer();
		}
		is_opened = true;
		thread_update = thread(&Visio::refreshFrame, this);
	}
}

void Visio::init() {
	setRedParameters(Scalar(RED_HUE_MIN, RED_SAT_MIN, RED_VAL_MIN), Scalar(RED_HUE_MAX, RED_SAT_MAX, RED_VAL_MAX));
	setYelParameters(Scalar(YEL_HUE_MIN, YEL_SAT_MIN, YEL_VAL_MIN), Scalar(YEL_HUE_MAX, YEL_SAT_MAX, YEL_VAL_MAX));
	setBlkParameters(Scalar(BLK_HUE_MIN, BLK_SAT_MIN, BLK_VAL_MIN), Scalar(BLK_HUE_MAX, BLK_SAT_MAX, BLK_VAL_MAX));

	erode_dilate_kernel = getStructuringElement(MORPH_ELLIPSE, Size(10,10));
	trans_calibrated = loadPerspectiveMatrix(calib_transform_matrix_filename);
	cam_calibrated = loadCameraMatrix(calib_cam_filename);


	//Parametres par defaut, modifies dans loadParams
	size_frame = Size(camera.get(CV_CAP_PROP_FRAME_WIDTH), camera.get(CV_CAP_PROP_FRAME_HEIGHT));
	cam_fps = CAM_FPS;
	distort = none;

	loadParams(calib_detection_filename);

	camera.set(CV_CAP_PROP_FRAME_WIDTH, size_frame.width);
	camera.set(CV_CAP_PROP_FRAME_HEIGHT, size_frame.height);
	camera.set(CV_CAP_PROP_FPS, cam_fps);

	if (use_mask) {
		mask = imread(path_to_conf+mask_name);
	}
}

void Visio::init_writer() {
	time_t rawtime;
	struct tm * timeinfo;
	char buffer[80];
	time (&rawtime);
	timeinfo = localtime(&rawtime);
	strftime(buffer,80,"-%d-%m %I:%M:%S",timeinfo);
	string date(buffer);
	string path = path_to_conf+(string)"video"+(char)(index+'0')+"-"+date+(string)".avi";
	cout << "Saving video to : " << path << endl;
	int codec = CV_FOURCC('D', 'I', 'V', 'X'); //Marche
	writer = VideoWriter(path, codec, cam_fps, size_frame);
	if (!writer.isOpened()) {
		cerr << "Failed to initialize writer, video can't be saved" << endl;
		save_video = false;
	}
}

/**********
 * PUBLIC *
 * ********/

void Visio::detectColor(const Mat& img, Mat& out) {
	Mat hsv = img;
	if (min.val[0] > max.val[0]) { //car les teintes sont circulaires
		//Si la détection "fait le tour" de la teinte, on la décale pour rester sur l'intervale 0-180
		Mat temp;
		inRange(hsv, min, Scalar(180, max.val[1], max.val[2]), temp);
		inRange(hsv, Scalar(0, min.val[1], min.val[2]), max, out);
		bitwise_or(temp, out, out);
	}
	else {
		inRange(hsv, min, max, out);
	}
	erode(out, out, erode_dilate_kernel);
	dilate(out, out, erode_dilate_kernel);

}

void Visio::getContour(const Mat& img, vector<vector<Point> >& contours) {
	Mat thresh;
	Timings::startTimer(3);
	detectColor(img, thresh);
	Timings::writeStepTime(3, "\t\t\t\tdetectColor");
	findContours(thresh, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
	Timings::writeStepTime(3, "\t\t\t\tfindContour");
}

//Renvoit positions et contours de la couleur détectée dans l'image en argument
int Visio::getDetectedPosition(const Mat& img, vector<Point2f>& detected_pts, vector<vector<Point> >& detected_contours) {
	Timings::startTimer(2);
	vector<vector<Point> > contours;
	getContour(img, contours);
	Timings::writeStepTime(2, "\t\t\tContours");
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
	Timings::writeStepTime(2, "\t\t\tMoments");
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
	if (contours.size() <= 0) {
		degree.push_back(0);
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
	if (contours.size() <= 0) {
		degree.push_back(0);
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
	Timings::startTimer(0);
	int nbr_of_tri = 0;
	Mat img, src_img, color_img;
	src_img = getImg();
	if (USE_MASK) {
		src_img.copyTo(color_img, mask);
	} else {
		color_img = src_img;
	}
	Timings::writeStepTime(0, "\tRetrieving");
	cvtColor(color_img, color_img, CV_BGR2HSV);
	Timings::writeStepTime(0, "\tConvert Color");
	if (distort == image && cam_calibrated) {
		undistort(src_img, img, CM, D);
		nbr_of_tri = trianglesFromImg(img, triangles);
	}
	else {
		if (distort == image) {
			cerr << "Distorsion par image demandé mais caméra non calibrée" << endl;
			return 0;
		}
		nbr_of_tri = trianglesFromImg(src_img, triangles);
	}
	Timings::writeStepTime(0, "\tTriangles");
	Timings::writeTime(0, "Total");
	return nbr_of_tri;
}

/*********************
 *	UI CALIBRATION	 *
 *	******************/

bool Visio::computeTransformMatrix(const Mat &img, const vector<Point2f> real_positions, Mat *out) {
	Mat gray;
	bool pattern_found = false;
	vector<Point2f> corners, ext_corn;
	cvtColor(img, gray, CV_BGR2GRAY);
	pattern_found = findChessboardCorners(gray, chessboard_size, corners, CALIB_CB_ADAPTIVE_THRESH + CALIB_CB_NORMALIZE_IMAGE);// + CALIB_CB_FAST_CHECK);
	if (pattern_found) {
		//On recupere les 4 points exterieurs de l'échiquier
		ext_corn.push_back(corners[0]);
		ext_corn.push_back(corners[chessboard_size.width - 1]);
		ext_corn.push_back(corners[(chessboard_size.width)*(chessboard_size.height - 1)]);
		ext_corn.push_back(corners[chessboard_size.height - 1 + (chessboard_size.width - 1)*(chessboard_size.height)]);
		cornerSubPix(gray, ext_corn, Size(11, 11), Size(-1, -1), TermCriteria(CV_TERMCRIT_EPS + CV_TERMCRIT_ITER, 30, 0.1));
		perspectiveMatrix = getPerspectiveTransform(ext_corn, real_positions);
		trans_calibrated = true;
		if (out != 0) { //La matrice ou existe
			drawObject(ext_corn[0].x, ext_corn[0].y, *out, intToString(real_positions[0].x) + (string)":" + intToString(real_positions[0].y), Scalar(255,0,0));
			for(int i=1; i<4; i++) {
				drawObject(ext_corn[i].x, ext_corn[i].y, *out, intToString(real_positions[i].x) + (string)":" + intToString(real_positions[i].y), Scalar(0,0,255));
			}
		}

	}
	else {
		perspectiveMatrix =  Mat::eye(3, 3, CV_64F);
		trans_calibrated = false;
		if (out != 0) { //La matrice ou existe
			drawChessboardCorners(*out, chessboard_size, corners, pattern_found);
		}
	}
	return trans_calibrated;
}

bool Visio::camPerspective() {
	//TODO choix position
	int xsize = 130, ysize = 210;
	int x = 185, y = 105;
	namedWindow("parameters");
	createTrackbar("x_size", "parameters", &xsize, 600);
	createTrackbar("y_size", "parameters", &ysize, 600);
	createTrackbar("x", "parameters", &x, 3000);
	createTrackbar("y", "parameters", &y, 2000);
	Mat img, undistorted_img;
	bool calibrated = false;
	int key = 0;
	cout << "Starting perpective calibration" << endl;
	namedWindow("Perspective");
	while (!(calibrated && key == 'c')) {
		vector<Point2f> position;
		position.push_back(Point2f(x, y - ysize));
		position.push_back(Point2f(x, y));
		position.push_back(Point2f(x + xsize, y - ysize));
		position.push_back(Point2f(x + xsize, y));
		img = getImg();
		if (cam_calibrated) {
			undistort(img, undistorted_img, CM, D);
		} else {
			cerr << "WARNING : Calibration de perspective sans calibration camera" << endl;
			undistorted_img = img;
		}
		calibrated = computeTransformMatrix(undistorted_img, position, &undistorted_img);
		if (key == 'q') {
			cerr << "WARNING : Perspective calibration failed" << endl;
			return false;
		}
		putText(undistorted_img, "Appuyer sur 'c' pour valider une vue", Point(10,10),1,1,Scalar(0,255,0),1);
		putText(undistorted_img, "Appuyer sur 'q' pour quiter", Point(10,30),1,1,Scalar(0,255,0),1);
		imshow("Perspective", undistorted_img);
		key = waitKey(20);
	}
	destroyWindow("Perspective");
	destroyWindow("parameters");
	return calibrated;
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
	//Calibration caméra
	cout << "Starting camera calibration" << endl;
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
		img = getImg();
		cvtColor(img, gray, CV_BGR2GRAY);
		pattern_found = findChessboardCorners(gray, chessboard_size, corners, CALIB_CB_ADAPTIVE_THRESH + CALIB_CB_NORMALIZE_IMAGE);// + CALIB_CB_FAST_CHECK);
		if (pattern_found) {
			cornerSubPix(gray, corners, Size(11, 11), Size(-1, -1), TermCriteria(CV_TERMCRIT_EPS + CV_TERMCRIT_ITER, 30, 0.1));
		}
		//Retour graphique
		drawChessboardCorners(img, chessboard_size, corners, pattern_found);
		stringstream txt;
		txt << "Captures effectuees : " << success << "/" << nbr_of_views;
		putText(img, txt.str(), Point(10,10),1,1,Scalar(0,255,0),1);
		putText(img, "Appuyer sur 'c' pour valider une vue", Point(10,30),1,1,Scalar(0,255,0),1);
		putText(img, "Appuyer sur 'q' pour quiter", Point(10,50),1,1,Scalar(0,255,0),1);
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
	cam_calibrated = true;
	return true;
}

//FILE MANAGER

bool Visio::loadPerspectiveMatrix(string filename) {
	cout << "Loading transform matrix from " << path_to_conf+filename << endl;
	FileStorage fs(path_to_conf+filename, FileStorage::READ);
	if (!fs.isOpened()) {
		cerr << "ERROR : Couldn't find " << filename << endl;
		return false;
	}
	fs["Q"] >> perspectiveMatrix;
	fs.release();
	trans_calibrated = true;
	return true;
}

void Visio::loadParams(string filename) {
	cout << "Loading detection params from " << path_to_conf+filename << endl;
	FileStorage fs(path_to_conf+filename, FileStorage::READ);
	if (!fs.isOpened()) {
		cerr << "ERROR : Couldn't find " << filename << endl;
		return;
	}
	int h, w, temp_dist;
	fs["min_size"] >> min_size;
	fs["real_min_size"] >> real_min_size;
	fs["distort_mode"] >> temp_dist;
	switch (temp_dist) {
		case 1:
			distort = image;
			break;
		case 2:
			distort = points;
			break;
		default:
			distort = none;
			break;
	}
	fs["epsilon_poly"] >> epsilon_poly;
	fs["max_diff_triangle_edge"] >> max_diff_triangle_edge;
	fs["use_mask"] >> use_mask;
	fs["mask_name"] >> mask_name;
	fs["width"] >> w;
	fs["height"] >> h;
	fs["fps"] >> cam_fps;
	size_frame = Size(w,h);
	fs.release();
	trans_calibrated = true;
}

bool Visio::loadCameraMatrix(string filename) {
	cout << "Loading camera data from " << path_to_conf+filename << endl;
	FileStorage fs(path_to_conf+filename, FileStorage::READ);
	if (!fs.isOpened()) {
		cerr << "ERROR : Couldn't find " << filename << endl;
		return false;
	}
	fs["D"] >> D;
	fs["CM"] >> CM;
	fs.release();
	cam_calibrated = true;
	return true;
}

void Visio::savePerspectiveMatrix(string filename) {
	cout << "Saving transformation matrix" << endl;
	if (!trans_calibrated) {
		cerr << "ERROR : Uncalibrated detection" << endl;
		return;
	}
	FileStorage fs(path_to_conf+filename, FileStorage::WRITE);
	fs << "Q" << perspectiveMatrix;
	fs.release();
}

void Visio::saveParams(string filename) {
	cout << "Saving detection params" << endl;
	FileStorage fs(path_to_conf+filename, FileStorage::WRITE);
	fs << "min_size" << min_size;
	fs << "real_min_size" << real_min_size;
	fs << "distort_mode" << (int)distort;
	fs << "epsilon_poly" << epsilon_poly;
	fs << "max_diff_triangle_edge" << max_diff_triangle_edge;
	fs << "use_mask" << use_mask;
	fs << "mask_name" << mask_name;
	fs << "width" << size_frame.width;
	fs << "height" << size_frame.height;
	fs << "fps" << cam_fps;
	fs.release();
}
void Visio::saveCameraMatrix(string filename) {
	cout << "Saving camera data" << endl;
	if (!cam_calibrated) {
		cerr << "ERROR : Uncalibrated camera" << endl;
		return;
	}
	FileStorage fs(path_to_conf+filename, FileStorage::WRITE);
	fs << "D" << D;
	fs << "CM" << CM;
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

void Visio::setRealMinSize(int size) {
	real_min_size = size;
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

void Visio::setDistortMode(DistortType mode) {
	distort = mode;
}

//GETTER

Mat Visio::getQ() {
	return perspectiveMatrix;
}

Mat Visio::getCM() {
	return CM;
}

Mat Visio::getD() {
	return D;
}

Mat Visio::getImg() {
	Mat img;
	frame_mutex.lock(); //Bloque le thread d'update
	img = last_image;
	frame_mutex.unlock();
	return img;
}

bool Visio::isCalibrated() {
	return cam_calibrated & trans_calibrated;
}

bool Visio::isReady() {
	return isready;
}

bool Visio::isOpened() {
	return is_opened;
}

DistortType Visio::getDistortMode() {
	return distort;
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
	Timings::startTimer(1);
	if ((detected_size = getDetectedPosition(img, detected_pts, contours)) > 0) {
		Timings::writeStepTime(1, "\t\tDetect position");
		vector<Point2f> points_real;
		vector<int> degree;
		//Transformation perspective des points detectes
		transformPts(detected_pts, points_real);
		//Calcul du nombre de polylignes
		polyDegree(contours, degree, contours);
		//Pour chaque contour
		for (int i=0; i < detected_size; i++) {
			//Si c'est un triangle
			if (color != black) {
				if (degree[i] == 3) {
					vector<Point2f> contour_real;
					transformPts(contours[i], contour_real);
					Moments moment = moments(contour_real);
					if (moment.m00 > real_min_size) {
						addTriangle(points_real[i], contour_real, triangles, moment.m00);
						nb_triangles++;
					}
				}
				else if (degree[i] > 3 && degree[i] < 8) {
					vector<Point2f> contour_real;
					transformPts(contours[i], contour_real);
					//Voir si on a pas plusieurs triangles collés
					nb_triangles += deduceTrianglesFromContour(contour_real, triangles);
				}
			}
			else if (ENABLE_BLK) { //black
				if (degree[i] >= 4){
					vector<Point2f> contour_real;
					transformPts(contours[i], contour_real);
					Moments moment = moments(contour_real);
					if (moment.m00 > real_min_size) {
						addTriangle(points_real[i], contour_real, triangles, moment.m00);
						nb_triangles++;
					}
				}
			}
		}
	}
	Timings::writeStepTime(1, "\t\tTransform");
	return nb_triangles;
}

void Visio::addTriangle(const Point2f& point_real, const vector<Point2f>& contour_real, vector<Triangle>& triangles, double size) {
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
	if (tri.color != black && isEqui(contour_real[0], contour_real[1], contour_real[2])) {
		tri.isDown = true;
	}
	else {
		tri.isDown = false;
	}
	tri.size = size;
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
					if (moment.m00 > real_min_size) {
						Triangle tri;
						float x = moment.m10 / moment.m00;
						float y = moment.m01 / moment.m00;
						addTriangle(Point2f(x,y), contour_tri, triangles, moment.m00);
						nb_triangles++;
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

void Visio::transformPts(const vector<Point>& pts_in, vector<Point2f>& pts_out) {
	transformPts(convertItoF(pts_in), pts_out);
}

void Visio::transformPts(const vector<Point2f>& pts_in, vector<Point2f>& pts_out) {
	if (distort == points) {
		undistortPoints(pts_in, pts_out, CM, D, Mat(), CM);
		perspectiveTransform(pts_out, pts_out, perspectiveMatrix);
	} else {
		perspectiveTransform(pts_in, pts_out, perspectiveMatrix);
	}
}

void Visio::refreshFrame() {
	Mat img;
	camera >> last_image;
	frame_mutex.unlock();
	isready = true;
	while(1) {
		camera.grab();
		frame_mutex.lock();
		camera.retrieve(last_image);
		if (save_video) {
			img = last_image;
		}
		frame_mutex.unlock();
		if (save_video) {
			writer << img;
		}
	}
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

#include "stereo.h"
#include <opencv2/opencv.hpp>
#include <opencv2/calib3d/calib3d_c.h>

using namespace std;

Stereo::Stereo(int index_left, int index_right):
	cam_left(), cam_right(), calibrated(false) {
	setAlphaROI(0.5);
	cam_left.open(index_left);
	cam_right.open(index_right);
	if (!cam_right.isOpened() || !cam_left.isOpened()) {
		cerr << "ERROR : Cameras not found" << endl;
		exit(EXIT_FAILURE);
	}
}

bool Stereo::calibrate(int nbr_of_views, Size size_chessboard) {
	namedWindow("ViewLeft");
	namedWindow("ViewRight");

	//points reels et image pour la calibration
	vector<vector<Point3f> > objectPoints;
	vector<vector<Point2f> > imagePoints_left, imagePoints_right;

	//position des points corners (dimension abstraite)
	vector<Point3f> obj;
	for (int j=0; j<size_chessboard.height * size_chessboard.width; j++)
	{
		obj.push_back(Point3f(j/size_chessboard.width, j%size_chessboard.width, 0.0f));
	}

	//On prend un certain nombre de vues de l'échiquier
	bool capture = false; 
	int key = 0;
	for(int success=0; success < nbr_of_views;) {
		Mat img[2], gray[2];
		vector<Point2f> corners[2];
		bool pattern_found[2];

		//A-t-on appuyé sur 'c' pour capturer cette frame ?
		if (key == 'c') {
			capture= true;
		}
		if (key == 'q') {
			cerr << "WARNING : Calibration failed" << endl;
			destroyWindow("ViewRight");
			destroyWindow("ViewLeft");
			return false;
		}
		//Capture d'image
		cam_left >> img[0];
		cam_right >> img[1];

		cameras_image_size = img[0].size(); //Les cameras sont identiques, leurs taille d'image aussi

		for(int i=0; i < 2; i++) {
			cvtColor(img[i], gray[i], CV_BGR2GRAY);
			pattern_found[i] = findChessboardCorners(gray[i], size_chessboard, corners[i], CALIB_CB_ADAPTIVE_THRESH + CALIB_CB_NORMALIZE_IMAGE + CALIB_CB_FAST_CHECK);
			//Amelioration de la precision
			if (pattern_found[i]) {
				cornerSubPix(gray[i], corners[i], Size(11, 11), Size(-1, -1), TermCriteria(CV_TERMCRIT_EPS + CV_TERMCRIT_ITER, 30, 0.1));
			}
			//Retour graphique
			drawChessboardCorners(img[i], size_chessboard, corners[i], pattern_found[i]);
			stringstream txt;
			txt << "Captures effectuées : " << success << "/" << nbr_of_views;
			putText(img[i], txt.str(), Point(10,10),1,1,Scalar(0,255,0),1);
		}

		//Si l'echiquier est détecté dans les deux images et que l'on souhaite capturer cette frame
		if (capture && pattern_found[0] && pattern_found[1]) {
			success++;
			objectPoints.push_back(obj);
			imagePoints_left.push_back(corners[0]);
			imagePoints_right.push_back(corners[1]);
			capture = false;
		}
		imshow("ViewLeft", img[0]);
		imshow("ViewRight", img[1]);
		key = waitKey(20);
	}
	destroyWindow("ViewRight");
	destroyWindow("ViewLeft");

	cout << "Views captured, computing data ..." << endl;

	//Un tas de matrices necessaires
	//Matrice de parametres intrinseques
	Mat CM1 = Mat(3, 3, CV_64FC1); 
    Mat CM2 = Mat(3, 3, CV_64FC1);
	//Matrices de distorsion
    Mat D1, D2;
	//Rotation, transformation, essential matrix, matrice fondamentale
    Mat R, T, E, F;
	//Rectificiation, transformation et disparity-to-depth matrices
	Mat R1, R2, P1, P2, Q;
	
	//Calibration des cameras
	stereoCalibrate(objectPoints, imagePoints_left, imagePoints_right,
		CM1, D1, CM2, D2, cameras_image_size, R, T, E, F,
		cvTermCriteria(CV_TERMCRIT_ITER+CV_TERMCRIT_EPS, 100, 1e-5), 
		CV_CALIB_SAME_FOCAL_LENGTH | CV_CALIB_ZERO_TANGENT_DIST);
	//Creation des matrices pour rectification des images
	stereoRectify(CM1, D1, CM2, D2, cameras_image_size, R, T, R1, R2, P1, P2, Q,
		CALIB_ZERO_DISPARITY, alpha_parameter_roi, cameras_image_size, &ROI_left, &ROI_right);
	//Creation des matrices de rectification des images *_remap_[1,2]
	initUndistortRectifyMap(CM1, D1, R1, P1, cameras_image_size, CV_32FC1, left_remap_1, left_remap_2);
	initUndistortRectifyMap(CM2, D2, R2, P2, cameras_image_size, CV_32FC1, right_remap_1, right_remap_2);

	cout << "Done !" << endl;
	calibrated = true;
	return true;
}

void Stereo::displayCalibration() {
	namedWindow("Views");
	Mat img_left, img_right;
	Scalar green(0,255,0), red(0,0,255);
	//Retour graphique des parametres
	int key = 0;
	while (key != 'q') {
		//Capture de frame
		cam_left >> img_left;
		cam_right >> img_right;

		//Remap suivant les parametres de la stereo
		remap(img_left, img_left, left_remap_1, left_remap_2,INTER_LINEAR);
		remap(img_right, img_right, right_remap_1, right_remap_2,INTER_LINEAR);

		//Dessin des ROI
		rectangle(img_left, ROI_left, green, 2);
		rectangle(img_right, ROI_right, green, 2);

		//Combinaison des images
		Mat combine(max(img_left.size().height, img_right.size().height), img_left.size().width + img_right.size().width, CV_8UC3);
		Mat left_roi(combine, Rect(0, 0, img_left.size().width, img_left.size().height));
		img_left.copyTo(left_roi);
		Mat right_roi(combine, Rect(img_left.size().width, 0, img_right.size().width, img_right.size().height));
		img_right.copyTo(right_roi);

		//Dessin de lignes horizontales
		int step = 40;
		for(int i=0; i < cameras_image_size.height; i+=step) {
			Point l(0, i), r(combine.size().width-1, i);
			line(combine, l, r, red);
		}

		//Display
		imshow("Views", combine);
		key = waitKey(20);
	}
}

void Stereo::setAlphaROI(double a) {
	alpha_parameter_roi = a;
}

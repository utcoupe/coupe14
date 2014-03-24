#include "stereo.h"
#include <opencv2/opencv.hpp>

using namespace std;

Stereo::Stereo(int left, int right){
	init(left, right);
}

void Stereo::init(int left, int right) {
	cam[l].open(left);
	cam[r].open(right);
	setAlphaROI(0.5);
	if (!cam[0].isOpened() || !cam[1].isOpened()) {
		cerr << "ERROR : Cameras not found" << endl;
		exit(EXIT_FAILURE);
	}
	if (!loadStereoCalibration()) {
		sbm.SADWindowSize = 5; sbm.numberOfDisparities = 192; sbm.preFilterCap = 4; sbm.minDisparity = -64; 
		sbm.uniquenessRatio = 1; sbm.speckleWindowSize = 150; sbm.speckleRange = 2; sbm.disp12MaxDiff = 10;
		sbm.P1 = 600; sbm.P2 = 2400;
		sbm.fullDP = false;
	}
		
	calibrated = false;
	size_chessboard = Size(7,6);
	Mat temp_img;
	cam[0] >> temp_img;
	cameras_image_size = temp_img.size(); //Les cameras sont identiques, leurs taille d'image aussi
}

bool Stereo::singleCamCalibrate(enum side side, int nbr_of_views) {
	string name;
	if (side == l)
		name = "Calibrating left camera";
	else
		name = "Calibrating right camera";

	//points reels et image pour la calibration
	vector<vector<Point3f> > objectPoints;
	vector<vector<Point2f> > imagePoints;

	//position des points corners (dimension abstraite)
	vector<Point3f> obj;
	for (int j=0; j<size_chessboard.height * size_chessboard.width; j++)
	{
		obj.push_back(Point3f(j/size_chessboard.width, j%size_chessboard.width, 0.0f));
	}
	//Calibration caméra gauche
	namedWindow(name);
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
			destroyWindow("Left");
			return false;
		}
		//Capture d'image
		cam[side] >> img;
		cvtColor(img, gray, CV_BGR2GRAY);
		pattern_found = findChessboardCorners(gray, size_chessboard, corners, CALIB_CB_ADAPTIVE_THRESH + CALIB_CB_NORMALIZE_IMAGE + CALIB_CB_FAST_CHECK);
		if (pattern_found) {
			cornerSubPix(gray, corners, Size(11, 11), Size(-1, -1), TermCriteria(CV_TERMCRIT_EPS + CV_TERMCRIT_ITER, 30, 0.1));
		}
		//Retour graphique
		drawChessboardCorners(img, size_chessboard, corners, pattern_found);
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
		imshow(name, img);
		key = waitKey(20);
	}
	cout << "Beginning processing" << endl;
	destroyWindow(name);
	vector<Mat> empty;
	calibrateCamera(objectPoints, imagePoints, cameras_image_size, CM[side], D[side], empty, empty);
	cout << "Done !" << endl;
	return true;
}

bool Stereo::calibrate(int nbr_of_views) {
	cout << "Beginning overall calibration" << endl;
	int key = 0;
	bool capture = false;
	//points reels et image pour la calibration
	vector<vector<Point3f> > objectPoints;
	vector<vector<Point2f> > imagePoints_left, imagePoints_right;

	//position des points corners (dimension abstraite)
	vector<Point3f> obj;
	for (int j=0; j<size_chessboard.height * size_chessboard.width; j++)
	{
		obj.push_back(Point3f(j/size_chessboard.width, j%size_chessboard.width, 0.0f));
	}

	singleCamCalibrate(l, nbr_of_views);
	singleCamCalibrate(r, nbr_of_views);

	namedWindow("ViewLeft");
	namedWindow("ViewRight");
	//On prend un certain nombre de vues de l'échiquier
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
		cam[l] >> img[l];
		cam[r] >> img[r];

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
		imshow("ViewLeft", img[l]);
		imshow("ViewRight", img[r]);
		key = waitKey(20);
	}
	destroyWindow("ViewRight");
	destroyWindow("ViewLeft");

	cout << "Views captured, computing data ..." << endl;

	//Rotation, transformation, essential matrix, matrice fondamentale
    Mat R, T, E, F;
	//Rectificiation, transformation
	Mat R1, R2, P1, P2;
	
	//Calibration des cameras
	rms_error = stereoCalibrate(objectPoints, imagePoints_left, imagePoints_right,
		CM[l], D[l], CM[r], D[r], cameras_image_size, R, T, E, F,
		cvTermCriteria(CV_TERMCRIT_ITER+CV_TERMCRIT_EPS, 100, 1e-5), 
		CV_CALIB_FIX_INTRINSIC);
	cout << "done with RMS error=" << rms_error << endl;
	//Creation des matrices pour rectification des images
	stereoRectify(CM[l], D[l], CM[r], D[r], cameras_image_size, R, T, R1, R2, P1, P2, Q,
		0, alpha_parameter_roi, cameras_image_size, &ROI[l], &ROI[r]);
	//Creation des matrices de rectification des images *_remap_[1,2]
	initUndistortRectifyMap(CM[l], D[l], R1, P1, cameras_image_size, CV_32FC1, remap_1[l], remap_2[l]);
	initUndistortRectifyMap(CM[r], D[r], R2, P2, cameras_image_size, CV_32FC1, remap_1[r], remap_2[r]);

	cout << "Done !" << endl;
	calibrated = true;
	return true;
}

void Stereo::displayCalibration() {
	cout << "Displaying calibration parameters" << endl;
	namedWindow("Views");
	namedWindow("Disparity");
	namedWindow("Parameters");
	int sad((sbm.SADWindowSize-1)/2), nbrdisp(sbm.numberOfDisparities/16), mindisp(sbm.minDisparity + 128);
	createTrackbar("Sad", "Parameters", &sad, 6);
	createTrackbar("nbrDisparities", "Parameters", &nbrdisp, 16);
	createTrackbar("prefilter", "Parameters", &sbm.preFilterCap, 10);
	createTrackbar("minDsp", "Parameters", &mindisp, 256);
	createTrackbar("uniqueness", "Parameters", &sbm.uniquenessRatio, 20);
	createTrackbar("specklesize", "Parameters", &sbm.speckleWindowSize, 500);
	createTrackbar("specklerange", "Parameters", &sbm.speckleRange, 5);
	createTrackbar("disp12", "Parameters", &sbm.disp12MaxDiff, 20);
	createTrackbar("p1", "Parameters", &sbm.P1, 1500);
	createTrackbar("p2", "Parameters", &sbm.P2, 5000);

	Mat img_left, img_right, disp;
	Mat gray_left, gray_right;
	Scalar green(0,255,0), red(0,0,255);
	//Retour graphique des parametres
	int key = 0;
	while (key != 'q') {
		if (key == 's') {
			saveStereoCalibration();
		}
		sbm.SADWindowSize = sad*2+1;
		sbm.numberOfDisparities = nbrdisp*16;
		sbm.minDisparity = mindisp - 128;

		//Capture de frame
		cam[l] >> img_left;
		cam[r] >> img_right;

		//Remap suivant les parametres de la stereo
		remap(img_left, img_left, remap_1[l], remap_2[l], INTER_LINEAR);
		remap(img_right, img_right, remap_1[r], remap_2[r], INTER_LINEAR);

		//Disparity
		sbm(img_left(overall_ROI), img_right(overall_ROI), disp);
		normalize(disp, disp, 0, 255, CV_MINMAX, CV_8U);
		

		//Dessin des ROI
		rectangle(img_left, ROI[l], red, 1);
		rectangle(img_left, overall_ROI, green, 2);
		rectangle(img_right, ROI[r], red, 1);
		rectangle(img_right, overall_ROI, green, 2);

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
		imshow("Disparity", disp);
		key = waitKey(20);
	}
}

void Stereo::saveCameraCalibration() {
	cout << "Saving camera calibration data" << endl;
	if (!calibrated) {
		cerr << "WARNING : Uncalibrated cameras, data not saved" << endl;
		return;
	}
	FileStorage fs("calibration_camera.yml", FileStorage::WRITE);
	//Camera calibration
	fs << "cameras_image_size" << cameras_image_size;
	fs << "alpha" << alpha_parameter_roi;
	fs << "Q" << Q;
	fs << "remap1_l" << remap_1[l];
	fs << "remap1_r" << remap_1[r];
	fs << "remap2_l" << remap_2[l];
	fs << "remap2_r" << remap_2[r];
	fs << "CM_l" << CM[l];
	fs << "CM_r" << CM[r];
	fs << "D_l" << D[l];
	fs << "D_r" << D[r];
	fs << "ROI_l" << ROI[l];
	fs << "ROI_r" << ROI[r];
	fs << "rms" << rms_error;
	fs.release();
}

void Stereo::saveStereoCalibration() {
	cout << "Saving stereo calibration data" << endl;
	FileStorage fs("calibration_stereo.yml", FileStorage::WRITE);
	//Stereo calibration
	fs << "sad_window" << sbm.SADWindowSize;
	fs << "nbr_disp" << sbm.numberOfDisparities;
	fs << "prefiltercad" << sbm.preFilterCap;
	fs << "mindisparity" << sbm.minDisparity;
	fs << "uniqueness" << sbm.uniquenessRatio;
	fs << "specklesize" << sbm.speckleWindowSize;
	fs << "specklerange" << sbm.speckleRange;
	fs << "disp12" << sbm.disp12MaxDiff;
	fs << "p1" << sbm.P1;
	fs << "p2" << sbm.P2;
	fs.release();
}

bool Stereo::loadCameraCalibration() {
	FileStorage fs("calibration_camera.yml", FileStorage::READ);
	if (!fs.isOpened()) {
		cerr << "ERROR : Couldn't find calibration_camera.yml" << endl;
		return false;
	}
	//Camera calibration
	fs["cameras_image_size"] >> cameras_image_size;
	fs["alpha"] >> alpha_parameter_roi;
	fs["Q"] >> Q;
	fs["remap1_l"] >> remap_1[l];
	fs["remap1_r"] >> remap_1[r];
	fs["remap2_l"] >> remap_2[l];
	fs["remap2_r"] >> remap_2[r];
	fs["CM_l"] >> CM[l];
	fs["CM_r"] >> CM[r];
	fs["D_l"] >> D[l];
	fs["D_r"] >> D[r];
	fs["ROI_l"] >> ROI[l];
	fs["ROI_r"] >> ROI[r];
	fs["rms"] >> rms_error;
	mulROI(ROI[l], ROI[r], overall_ROI);
	fs.release();
	cout << "Camera calibration data loaded" << endl;
	return true;
}
bool Stereo::loadStereoCalibration() {
	FileStorage fs("calibration_stereo.yml", FileStorage::READ);
	if (!fs.isOpened()) {
		cerr << "ERROR : Couldn't find calibration_stereo.yml" << endl;
		return false;
	}
	//Stereo calibration
	fs["sad_window"] >> sbm.SADWindowSize;
	fs["nbr_disp"] >> sbm.numberOfDisparities;
	fs["prefiltercad"] >> sbm.preFilterCap;
	fs["mindisparity"] >> sbm.minDisparity;
	fs["uniqueness"] >> sbm.uniquenessRatio;
	fs["specklesize"] >> sbm.speckleWindowSize;
	fs["specklerange"] >> sbm.speckleRange;
	fs["disp12"] >> sbm.disp12MaxDiff;
	fs["p1"] >> sbm.P1;
	fs["p2"] >> sbm.P2;
	sbm.fullDP = false;
	fs.release();
	cout << "Stereo calibration data loaded" << endl;
	return true;
}

void Stereo::mulROI(const Rect& roi1, const Rect& roi2, Rect& out) {
	out.x = max(roi1.x, roi2.x);
	out.y = max(roi1.y, roi2.y);
	out.width = min(roi1.x + roi1.width, roi2.x + roi2.width) - out.x;
	out.height = min(roi1.y + roi1.height, roi2.y + roi2.height) - out.y;
}

void Stereo::setAlphaROI(double a) {
	alpha_parameter_roi = a;
}

void Stereo::getDisparity(Mat& out) {
	sbm(left_img, right_img, out);
}

Mat Stereo::getQ() {
	return Q;
}

void Stereo::newImage() {
	cam[0] >> left_img;
	cam[1] >> right_img;
}

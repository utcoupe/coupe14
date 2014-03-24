#ifndef STEREO_H
#define STEREO_H

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/types_c.h>

using namespace cv;

enum side { l, r };

class Stereo {
	public:
	Stereo(int left, int right);
	bool calibrate(int nbr_of_views=10);
	void displayCalibration();

	bool loadCameraCalibration();
	bool loadStereoCalibration();
	void saveCameraCalibration();
	void saveStereoCalibration();

	void newImage();

	Mat left_img, right_img;
	//SETTER
	void setAlphaROI(double a);
	//GETTER
	void getDisparity(Mat& out);
	Mat getQ();
	private:
	void init(int left, int right);
	bool singleCamCalibrate(enum side side, int nbr_of_views=10);
	void mulROI(const Rect& roi1, const Rect& roi2, Rect& out);

	bool calibrated;
	Size cameras_image_size;
	Size size_chessboard;
	Mat Q; //disparity to depth matrix
	VideoCapture cam[2];
	Mat remap_1[2], remap_2[2]; //Matrices de rectification de l'image
	Mat CM[2], D[2];
	Rect ROI[2], overall_ROI;

	//parametre alpha de la fonction de detection des ROI
	double alpha_parameter_roi;
	double rms_error;

	//Parametres SGBM
	StereoSGBM sbm;
};


#endif

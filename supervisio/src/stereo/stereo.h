#ifndef STEREO_H
#define STEREO_H

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/types_c.h>

using namespace cv;

enum side { l, r };

class Stereo {
	public:
	Stereo();
	Stereo(int index_left, int index_right);
	bool calibrate(int nbr_of_views=10);
	void displayCalibration();
	bool loadCalibration();
	void saveCalibration();

	//SETTER
	void setAlphaROI(double a);
	//GETTER
	void getDisparity(Mat& out);
	private:
	void init(int index_left, int index_right);
	bool singleCamCalibrate(enum side side, int nbr_of_views=10);
	bool calibrated;
	Size cameras_image_size;
	Size size_chessboard;
	Mat Q; //disparity to depth matrix
	VideoCapture cam[2];
	Mat remap_1[2], remap_2[2]; //Matrices de rectification de l'image
	Mat CM[2], D[2];
	Rect ROI[2];

	//parametre alpha de la fonction de detection des ROI
	double alpha_parameter_roi;
};


#endif

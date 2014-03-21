#ifndef STEREO_H
#define STEREO_H

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/types_c.h>

using namespace cv;

class Stereo {
	public:
	Stereo();
	Stereo(int index_left=0, int index_right=1);
	bool calibrate(int nbr_of_views=8, Size size_chessboard=Size(7,6));
	void displayCalibration();
	bool loadCalibration();
	bool saveCalibration();

	//SETTER
	void setAlphaROI(double a);
	private:
	VideoCapture cam_left, cam_right;
	bool calibrated;
	Size cameras_image_size;
	Mat Q; //disparity to depth matrix
	Mat left_remap_1, left_remap_2, right_remap_1, right_remap_2; //Matrices de rectification de l'image
	Rect ROI_left, ROI_right;

	//parametre alpha de la fonction de detection des ROI
	double alpha_parameter_roi;
};

#endif

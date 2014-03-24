// Visio UTCoupe 2014
// Par Quentin CHATEAU

#ifndef TRAITEMENT_H
#define TRAITEMENT_H

#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

typedef vector<Point> Contour;
typedef vector<vector<Point> > Contours;

class Persp {
	public:
		Persp();
		Persp(Scalar min, Scalar max);
		void getDetectedPosition(const Mat& img, vector<Point2f>& detected_pts, Contours& detected_contours);
		bool computeTransformMatrix(const Mat &img, const vector<Point2f> real_positions, Mat *out=0);
		void warpPerspective(const Mat& frame, Mat& out, Size size);
		//SETTER
		void setParameters(Scalar min, Scalar max, int size=0);
	private:
		void init();
		void detectColor(const Mat& img, Mat& out);
		Contours getContour(const Mat& img);
		Scalar min, max;
		Size chessboard_size;
		Mat perspectiveMatrix;
		int min_size; //Taille minimal d'une zone de couleur valide
		bool calibrated;
};


#endif

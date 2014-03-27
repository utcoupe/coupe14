// Visio UTCoupe 2014
// Par Quentin CHATEAU

#ifndef TRAITEMENT_H
#define TRAITEMENT_H

#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

typedef enum color {red, yellow} Color;
typedef struct triangle {
	Point2f coords;
	Color color;
	bool isDown;
} Triangle;

class Visio {
	public:
		Visio();
		void detectColor(const Mat& img, Mat& out);
		void getContour(const Mat& img, vector<vector<Point> >& contours);
		int getDetectedPosition(const Mat& img, vector<Point2f>& detected_pts, vector<vector<Point> >& detected_contours);
		bool computeTransformMatrix(const Mat &img, const vector<Point2f> real_positions, Mat *out=0);
		void polyDegree(const vector<vector<Point> >& contours, vector<int>& degree, double epsilon=-1);
		void polyDegree(const vector<vector<Point> >& contours, vector<int>& degree, vector<vector<Point> >& approx, double epsilon=-1);
		int triangles(const Mat& img, vector<Triangle>& triangles, Rect area);
		//FILE
		bool loadTransformMatrix();
		void saveTransformMatrix();
		//SETTER
		void setRedParameters(Scalar min, Scalar max);
		void setYelParameters(Scalar min, Scalar max);
		void setMinSize(int size);
		void setColor(Color color);
		void setErodeDilateKernel(Mat kernel);
		void setEpsilonPoly(double ep);
		//GETTER
		Mat getQ();
		//DEBUG
		int getRealWorldPosition(const Mat& img, vector<Point2f>& detected_pts);
	private:
		void init();
		void setParameters(Scalar min, Scalar max, int size=-1);
		int trianglesColor(const Mat& img, vector<Triangle>& triangles, Color color);

		Scalar min, max;
		Scalar yel_min, yel_max, red_min, red_max;
		Size chessboard_size;
		Mat perspectiveMatrix;
		Mat erode_dilate_kernel; //kernel utilisé lors des erode/dilate
		int min_size; //Taille minimal d'une zone de couleur valide
		int min_down_size; //Seuil de taille au dessus duquel un triangl est considéré comme renversé
		double epsilon_poly; //Marge d'erreur lors de l'estimation de polyligne
		bool calibrated;
		Color color;
};

vector<vector<Point2f> > convertItoF(vector<vector<Point> > v);

#endif

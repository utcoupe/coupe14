// Visio UTCoupe 2014
// Par Quentin CHATEAU

#ifndef TRAITEMENT_H
#define TRAITEMENT_H

#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

typedef enum color {red, yellow, black} Color;
typedef struct triangle {
	Point2f coords;
	double angle;
	Color color;
	bool isDown;
	vector<Point2f> contour;
	double size;
} Triangle;

class Visio {
	public:
		Visio(VideoCapture& cam);
		void detectColor(const Mat& img, Mat& out);
		void getContour(const Mat& img, vector<vector<Point> >& contours);
		int getDetectedPosition(const Mat& img, vector<Point2f>& detected_pts, vector<vector<Point> >& detected_contours);
		void polyDegree(const vector<vector<Point> >& contours, vector<int>& degree, double epsilon=-1);
		void polyDegree(const vector<vector<Point> >& contours, vector<int>& degree, vector<vector<Point> >& approx, double epsilon=-1);
		int trianglesFromImg(const Mat& img, vector<Triangle>& triangles);
		int triangles(vector<Triangle>& triangles);
		//UI CALIBRATION
		bool computeTransformMatrix(const Mat &img, const vector<Point2f> real_positions, Mat *out=0);
		void camPerspective();
		bool camCalibrate(int nbr_of_views=10);
		//FILE
		bool loadTransformMatrix();
		bool loadCameraMatrix();
		void saveTransformMatrix();
		void saveCameraMatrix();
		//SETTER
		void setRedParameters(Scalar min, Scalar max);
		void setYelParameters(Scalar min, Scalar max);
		void setBlkParameters(Scalar min, Scalar max);
		void setMinSize(int size);
		void setColor(Color color);
		void setErodeDilateKernel(Mat kernel);
		void setEpsilonPoly(double ep);
		void setChessboardSize(Size s);
		void setMaxDiffTriangleEdget(int max);
		//GETTER
		Mat getQ();
	private:
		void init();
		void setParameters(Scalar min, Scalar max, int size=-1);
		int trianglesColor(const Mat& img, vector<Triangle>& triangles, Color color);
		void addTriangle(const Point2f& point_real, const vector<Point2f>& contour_real, vector<Triangle>& triangles);
		int deduceTrianglesFromContour(vector<Point2f>& contour_real, vector<Triangle>& triangles);
		bool isEqui(Point2f p1, Point2f p2, Point2f p3);

		VideoCapture camera;
		Scalar min, max;
		Scalar yel_min, yel_max, red_min, red_max, blk_min, blk_max;
		Size chessboard_size, size_frame;
		Mat perspectiveMatrix, CM, D;
		Mat erode_dilate_kernel; //kernel utilisé lors des erode/dilate
		int min_size; //Taille minimal d'une zone de couleur valide
		int min_down_size; //Seuil de taille au dessus duquel un triangl est considéré comme renversé
		int max_diff_triangle_edge;
		double epsilon_poly; //Marge d'erreur lors de l'estimation de polyligne
		bool trans_calibrated, cam_calibrated;
		Color color;
};

vector<vector<Point2f> > convertItoF(vector<vector<Point> > v);
vector<Point2f> convertItoF(vector<Point> v);
vector<Point> convertFtoI(vector<Point2f> v);

#endif

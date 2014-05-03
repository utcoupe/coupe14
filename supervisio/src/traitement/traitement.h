// Visio UTCoupe 2014
// Par Quentin CHATEAU

#ifndef TRAITEMENT_H
#define TRAITEMENT_H

#include <opencv2/opencv.hpp>
#include <mutex>
#include <thread>

using namespace cv;
using namespace std;

typedef enum color {red, yellow, black} Color;
typedef enum distortType { none, image, points } DistortType;
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
		Visio(int index, string path_to_conf="./", bool save_vid=false);
		void detectColor(const Mat& img, Mat& out);
		void getContour(const Mat& img, vector<vector<Point> >& contours);
		int getDetectedPosition(const Mat& img, vector<Point2f>& detected_pts, vector<vector<Point> >& detected_contours);
		void polyDegree(const vector<vector<Point> >& contours, vector<int>& degree, double epsilon=-1);
		void polyDegree(const vector<vector<Point> >& contours, vector<int>& degree, vector<vector<Point> >& approx, double epsilon=-1);
		int trianglesFromImg(const Mat& img, vector<Triangle>& triangles);
		int triangles(vector<Triangle>& triangles);
		//UI CALIBRATION
		bool computeTransformMatrix(const Mat &img, const vector<Point2f> real_positions, Mat *out=0);
		bool camPerspective();
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
		void setDistortMode(DistortType mode);
		//GETTER
		Mat getQ();
		Mat getCM();
		Mat getD();
		Mat getImg();
		bool isCalibrated();
		bool isReady();
		DistortType getDistortMode();
	private:
		void init();
		void init_writer();
		void setParameters(Scalar min, Scalar max, int size=-1);
		int trianglesColor(const Mat& img, vector<Triangle>& triangles, Color color);
		void addTriangle(const Point2f& point_real, const vector<Point2f>& contour_real, vector<Triangle>& triangles);
		int deduceTrianglesFromContour(vector<Point2f>& contour_real, vector<Triangle>& triangles);
		bool isEqui(Point2f p1, Point2f p2, Point2f p3);
		void transformPts(const vector<Point>& pts_in, vector<Point2f>& pts_out);
		void transformPts(const vector<Point2f>& pts_in, vector<Point2f>& pts_out);
		void refreshFrame();

		VideoCapture camera;
		VideoWriter writer;
		Scalar min, max;
		Scalar yel_min, yel_max, red_min, red_max, blk_min, blk_max;
		Size chessboard_size, size_frame;
		Mat perspectiveMatrix, CM, D, mask;
		Mat erode_dilate_kernel; //kernel utilisé lors des erode/dilate
		Mat last_image;
		int min_size; //Taille minimal d'une zone de couleur valide
		int max_diff_triangle_edge;
		int cam_fps;
		double epsilon_poly; //Marge d'erreur lors de l'estimation de polyligne
		bool trans_calibrated, cam_calibrated;
		bool save_video, isready;
		Color color;
		DistortType distort;
		string path_to_conf;
		mutex frame_mutex;
		thread thread_update;
};

vector<vector<Point2f> > convertItoF(vector<vector<Point> > v);
vector<Point2f> convertItoF(vector<Point> v);
vector<Point> convertFtoI(vector<Point2f> v);

#endif

// Visio UTCoupe 2014
// Par Quentin CHATEAU

#ifndef TRAITEMENT_H
#define TRAITEMENT_H

#include <opencv2/opencv.hpp>

using namespace cv;
using namespace std;

typedef vector<Point> Contour;
typedef vector<vector<Point> > Contours;

void getDetectedPosition(const Mat& img, vector<Point2f>& detected_pts, Contours& detected_contours, Scalar min, Scalar max, int min_size);
void detectColor(const Mat& img, Scalar min, Scalar max, Mat& out);
Contours getContour(const Mat& img, Scalar min, Scalar max);
Mat getTransformMatrix(const Mat &img, const vector<Point2f> real_positions);
Mat getTransformMatrix(const Mat &img, Mat& out, const vector<Point2f> real_positions);
vector<Point2f> orderPoints(const vector<Point2f> &pts);


#endif

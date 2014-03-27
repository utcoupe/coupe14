#ifndef GUI_H
#define GUI_H

#include <opencv2/opencv.hpp>
#include "traitement.h"

using namespace cv;

Mat getTransformMatrix(const Mat &img, Mat& out, const vector<Point2f> real_positions);
void showTransformedImage(const Mat& img, Mat& out, const Mat& transform);
void drawObject(int x, int y, Mat &frame, string addtxt="", Scalar color=Scalar(0,255,0));
string intToString(int number);

#endif

#ifndef GUI_H
#define GUI_H

#include <opencv2/opencv.hpp>
#include "traitement.h"

using namespace cv;

void showTransformedImage(const Mat& img, Mat& out, const Mat& transform);
void drawObject(int x, int y, Mat &frame, string addtxt="");
string intToString(int number);

#endif

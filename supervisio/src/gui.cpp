#ifdef VISUAL

#include "gui.h"
#include "traitement.h"

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/types_c.h>

Mat getTransformMatrix(const Mat &img, Mat& out, const vector<Point2f> real_positions) {
	Mat gray, perspectiveMatrix;
	bool pattern_found = false;
	vector<Point2f> corners, ext_corn, ordered_corn, ordered_real;
	cvtColor(img, gray, CV_BGR2GRAY);
	pattern_found = findChessboardCorners(gray, Size(7,7), corners, CALIB_CB_ADAPTIVE_THRESH + CALIB_CB_NORMALIZE_IMAGE + CALIB_CB_FAST_CHECK);
	if (pattern_found) {
		//On recupere les 4 points exterieurs de l'échiquier
		ext_corn.push_back(corners[0]);
		ext_corn.push_back(corners[6]);
		ext_corn.push_back(corners[0 + 6*7]);
		ext_corn.push_back(corners[6 + 6*7]);
		cornerSubPix(gray, ext_corn, Size(11, 11), Size(-1, -1), TermCriteria(CV_TERMCRIT_EPS + CV_TERMCRIT_ITER, 30, 0.1));
		//On reordonne les position
		ordered_corn = orderPoints(ext_corn);
		ordered_real = orderPoints(real_positions);

		perspectiveMatrix = getPerspectiveTransform(ordered_corn, ordered_real);

		for(int i=0; i<4; i++) {
			drawObject(ordered_corn[i].x, ordered_corn[i].y, out, intToString(i));
		}
	}
	else {
		drawChessboardCorners(out, Size(7,7), corners, pattern_found);
		perspectiveMatrix =  Mat::eye(3, 3, CV_64F);
	}
	return perspectiveMatrix;
}

void showTransformedImage(const Mat& img, Mat& out, const Mat& transform) {
	Mat trans = (Mat_<double>(3,3) << 1, 0, 400, 0, 1, 200, 0, 0, 1);
	warpPerspective(img, out, trans*transform, Size(img.cols+400, img.rows+200));
}

void drawObject(int x, int y, Mat &frame, string addtxt){
	circle(frame,Point(x,y),10,Scalar(0,255,0),1);
    if(y-10>0)
		line(frame,Point(x,y),Point(x,y-10),Scalar(0,255,0),1);
    else 
		line(frame,Point(x,y),Point(x,0),Scalar(0,255,0),1);
    if(y+10<frame.rows)
		line(frame,Point(x,y),Point(x,y+10),Scalar(0,255,0),1);
    else 
		line(frame,Point(x,y),Point(x,frame.rows),Scalar(0,255,0),1);
    if(x-10>0)
		line(frame,Point(x,y),Point(x-10,y),Scalar(0,255,0),1);
    else 
		line(frame,Point(x,y),Point(0,y),Scalar(0,255,0),1);
    if(x+10<frame.cols)
		line(frame,Point(x,y),Point(x+10,y),Scalar(0,255,0),1);
    else 
		line(frame,Point(x,y),Point(frame.rows,y),Scalar(0,255,0),1);

	string write = intToString(x)+","+intToString(y);
	if (addtxt != "") {
		write += " - " + addtxt;
	}
	putText(frame, write,Point(x,y+15),1,1,Scalar(0,255,0),1);

}

string intToString(int number)
{
	stringstream ss;//create a stringstream
	ss << number;//add number to the stream
	return ss.str();//return a string with the contents of the stream
}

#endif

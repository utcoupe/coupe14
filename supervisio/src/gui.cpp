#include "gui.h"
#include "traitement.h"

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/types_c.h>

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


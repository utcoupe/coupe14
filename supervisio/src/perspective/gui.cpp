#include "gui.h"
#include "traitement.h"

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/types_c.h>

void drawObject(int x, int y, Mat &frame, string addtxt, Scalar color, bool fill){
	circle(frame,Point(x,y),10,color,1);
    if(y-10>0)
		line(frame,Point(x,y),Point(x,y-10),color,1);
    else 
		line(frame,Point(x,y),Point(x,0),color,1);
    if(y+10<frame.rows)
		line(frame,Point(x,y),Point(x,y+10),color,1);
    else 
		line(frame,Point(x,y),Point(x,frame.rows),color,1);
    if(x-10>0)
		line(frame,Point(x,y),Point(x-10,y),color,1);
    else 
		line(frame,Point(x,y),Point(0,y),color,1);
    if(x+10<frame.cols)
		line(frame,Point(x,y),Point(x+10,y),color,1);
    else 
		line(frame,Point(x,y),Point(frame.rows,y),color,1);

	string write = intToString(x)+","+intToString(y);
	if (addtxt != "") {
		write += " - " + addtxt;
	}
	int baseline;
	Point pt(x,y+15);
	if (fill) {
		Size size_text = getTextSize(write, 1, 1, 1, &baseline);
		rectangle(frame, pt + Point(0, baseline), pt + Point(size_text.width, -size_text.height), CV_RGB(255,255,255), CV_FILLED);
	}
	putText(frame, write,pt,1,1,color,1);

}

string intToString(int number)
{
	stringstream ss;//create a stringstream
	ss << number;//add number to the stream
	return ss.str();//return a string with the contents of the stream
}

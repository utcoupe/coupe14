#include "gui.h"
#include "traitement.h"

#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/types_c.h>

void drawObject(int x, int y, Mat &frame, string addtxt){
	Scalar color(0,0,255);
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
	putText(frame, write,Point(x,y+15),1,1,color,1);

}

string intToString(int number)
{
	stringstream ss;//create a stringstream
	ss << number;//add number to the stream
	return ss.str();//return a string with the contents of the stream
}

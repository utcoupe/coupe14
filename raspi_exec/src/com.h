#ifndef COM_H
#define COM_H

#define MAX_TRI 10
#define NBR_ROBOTS 4

enum camArgs { x, y, a, size, color, isDown, end }; //ordonés

struct camData {
	int x, y, size, color, isDown;
	double a;
};

struct hokData {
	int x, y;
};

void com_loop(const char* cam_pipe, const char* hok_pipe) ;
void parseCamera(char *ori_line);
void parseHokuyo(char *ori_line);

#endif

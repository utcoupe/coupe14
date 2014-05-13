#ifndef COM_H
#define COM_H

struct camData {
};

struct hokData {
};

void com_loop(const char* cam_pipe, const char* hok_pipe) ;
void parseCamera(char *line);
void parseHokuyo(char *line);

#endif

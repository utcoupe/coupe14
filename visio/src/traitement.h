// Visio UTCoupe 2014
// Par Quentin CHATEAU
// Derniere edition le 04/12/13

#ifndef TRAITEMENT_H
#define TRAITEMENT_H

#include <highgui.h>
#include <cv.h>

void detect_color(IplImage *bgr_src, IplImage *mask, int h, int h_tol, int s_tol, int v_tol);
void detect_zone(IplImage *src_mask, IplImage *dest_mask, IplImage *zone_mask);
int get_weight(IplImage *mask);

#endif

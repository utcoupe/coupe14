// Visio UTCoupe 2014
// Par Quentin CHATEAU

#include "traitement.h"
#include <stdio.h>
#include <highgui.h>
#include <cv.h>

void detect_color(IplImage *bgr_src, IplImage *mask, int h, int h_tol, int s_tol, int v_tol){
	if(mask == NULL){
		printf("detect_color : mask doit être alloué\n");
		exit(EXIT_FAILURE);
	}
	else{
		IplImage* mask2 = NULL;
		mask2 = cvCreateImage(cvGetSize(bgr_src), bgr_src->depth, 1);

		IplImage* imgHSV = cvCreateImage(cvGetSize(bgr_src), IPL_DEPTH_8U, 3); 
		cvCvtColor(bgr_src, imgHSV, CV_BGR2HSV); //Change the color format from BGR to HSV

		int h_min = h - h_tol, h_max = h + h_tol;

		cvInRangeS(imgHSV, cvScalar(h_min, 255-s_tol, 255-v_tol, 0), cvScalar(h_max, 255, 255,0), mask);//Test de range standard
		if(h_min < 0){
			cvInRangeS(imgHSV, cvScalar(180+h_min, 255-s_tol, 255-v_tol, 0), cvScalar(180 , 255, 255,0), mask2);//rendre la teinte circulaire, étape1
			cvAdd(mask,mask2,mask,NULL);
		}
		if(h_max > 180){
			cvInRangeS(imgHSV, cvScalar(0, 255-s_tol, 255-v_tol, 0), cvScalar(h_max-180, 255, 255,0), mask2);//rendre la teinte circulaire, étape2
			cvAdd(mask,mask2,mask,NULL);
		}
		cvReleaseImage(&mask2);
		cvReleaseImage(&imgHSV);
	}
}

int get_weight(IplImage *mask){
	int i, weight=0;
	for(i=0;i<mask->width*mask->height;i++){
		if(mask->imageData[i] != 0)
			weight++;
	}
	return weight;
}

void detect_zone(IplImage *src_mask, IplImage *dest_mask, IplImage *zone_mask){
	cvMul(src_mask, zone_mask, dest_mask, 1);
}

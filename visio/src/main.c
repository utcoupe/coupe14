// Visio UTCoupe 2014
// Par Quentin CHATEAU

#include <stdio.h>
#include <cv.h>
#include <unistd.h>
#include <stdlib.h>

#include "traitement.h"
#include "global.h"
#include "serial_switch.h"
#include "protocole_serial.h"

#ifdef VISUAL
#include <highgui.h>
#endif

// $0=programme $1=h $2=h_tol $3=sv_tol
int main(int argc, char **argv){
	// Touche clavier
	char default_name[] = "./mask.jpg";
	char *mask_name = default_name;
	int h_yellow = H_YEL, h_yellow_tol = H_YEL_TOL, s_yellow_tol = S_YEL_TOL, v_yellow_tol = V_YEL_TOL;
	int h_red = H_RED, h_red_tol = H_RED_TOL, s_red_tol = S_RED_TOL, v_red_tol = V_RED_TOL;
	int weight_yellow, weight_red;
	int use_protocol = 0;

	// Capture vidéo
	CvCapture *capture=NULL;
	IplImage *image=NULL, *mask_red=NULL, *mask_yellow=NULL, *color_red_mask=NULL, *color_yellow_mask=NULL;
	IplImage *zone_mask = cvLoadImage(mask_name, 0);

	if (argc == 2 && strcmp(argv[1], "protocol") == 0) {
		printf("Utilisation du protcole\n");
		use_protocol = 1;
	}

	// Ouvrir le flux vidéo
	capture = cvCreateCameraCapture(CV_CAP_ANY);
	image = cvQueryFrame(capture);

	// Vérifier si l'ouverture du flux est ok
	if (!capture) {
		printf("Ouverture du flux vidéo impossible !\n");
		return 1;
	}

	//Resize mask
	IplImage *resized_mask = cvCreateImage(cvGetSize(image), image->depth, 1);
	cvResize(zone_mask, resized_mask, 0);

	//Ceation masques couleur
	color_yellow_mask = cvCreateImage(cvGetSize(image), image->depth, 1);
	mask_yellow = cvCreateImage(cvGetSize(image), image->depth, 1);
	color_red_mask = cvCreateImage(cvGetSize(image), image->depth, 1);
	mask_red = cvCreateImage(cvGetSize(image), image->depth, 1);


	//Lancement communication
	if (use_protocol) {
		printf("Lancement du thread protocole\n");
		init_protocol_thread();
	}
	printf("Lancement visio\n");

	// Boucle tant que l'utilisateur n'appuie pas sur la touche q (ou Q)
#ifdef VISUAL
	if(argc >= 2)
		h_yellow = atoi(argv[1]);
	if(argc >= 3)
		h_yellow_tol = atoi(argv[2]);
	if(argc >= 4){
		s_yellow_tol = atoi(argv[3]);
		v_yellow_tol = atoi(argv[3]);
	}
	// Définition de la fenêtre
	cvNamedWindow("Origine", CV_WINDOW_AUTOSIZE);
	cvNamedWindow("Mask_yellow", CV_WINDOW_AUTOSIZE);
	cvNamedWindow("Mask_red", CV_WINDOW_AUTOSIZE);

	char key = 0;
	while(key != 'q' && key != 'Q') {
		if(key == 'p'){
			h_yellow=(h_yellow+5)%180;
			printf("h=%d\n", h_yellow);
		}
		else if(key == 'm'){
			h_yellow=(h_yellow-5+180)%180;
			printf("h=%d\n", h_yellow);
		}
		if(key == 'o'){
			h_yellow_tol++;
			printf("tol=%d\n", h_yellow_tol);
		}
		else if(key == 'l'){
			h_yellow_tol--;
			printf("tol=%d\n", h_yellow_tol);
		}
		if(key == 'i'){
			s_yellow_tol++;
			printf("s_tol=%d\n", s_yellow_tol);
		}
		else if(key == 'k'){
			s_yellow_tol--;
			printf("s_tol=%d\n", s_yellow_tol);
		}
		if(key == 'u'){
			v_yellow_tol++;
			printf("v_tol=%d\n", v_yellow_tol);
		}
		else if(key == 'j'){
			v_yellow_tol--;
			printf("v_tol=%d\n", v_yellow_tol);
		}
#else
	while (1) {
#endif
		// On récupère une image
		image = cvQueryFrame(capture);

		//Processing
		detect_color(image, color_yellow_mask, h_yellow, h_yellow_tol, s_yellow_tol, v_yellow_tol);
		detect_zone(color_yellow_mask, mask_yellow, resized_mask);
		weight_yellow = get_weight(mask_yellow);

		detect_color(image, color_red_mask, h_red, h_red_tol, s_red_tol, v_red_tol);
		detect_zone(color_red_mask, mask_red, resized_mask);
		weight_red = get_weight(mask_red);

		//Affichage resultat
		pushData(weight_red, weight_yellow);

#ifdef VISUAL
		// On affiche l'image dans une fenêtre
		cvShowImage("Mask_yellow", mask_yellow);
		cvShowImage("Mask_red", mask_red);
		cvShowImage("Origine", image);

		// On attend 50ms
		key = cvWaitKey(50);
#endif
	}
	cvReleaseCapture(&capture);
	cvReleaseImage(&mask_yellow);
	cvReleaseImage(&mask_red);
	cvReleaseImage(&image);
	cvReleaseImage(&color_yellow_mask);
	cvReleaseImage(&color_red_mask);
#ifdef VISUAL
	cvDestroyWindow("Mask_yellow");
	cvDestroyWindow("Mask_red");
	cvDestroyWindow("Origine");
#endif
	return 0;
}

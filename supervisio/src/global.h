// Visio UTCoupe 2014
// Par Quentin CHATEAU

#ifndef GLOBAL_H
#define GLOBAL_H

#ifndef TIMEBENCH
#define TIMEBENCH false
#endif

#define MIN_SIZE 3000 //Attention, ici ce n'est pas la taille reelle mais la taille sur image originale
#define MIN_REAL_SIZE 4000

#define USE_MASK false

#define WIDTH 640
#define HEIGHT 480
#define CAM_FPS 30

#define EPSILON_POLY 0.07
#define MAX_DIFF_TRI_EDGE 50

#define YEL_HUE_MIN 15
#define YEL_HUE_MAX 40
#define YEL_SAT_MIN 80
#define YEL_SAT_MAX 255
#define YEL_VAL_MIN 200
#define YEL_VAL_MAX 255

#define RED_HUE_MIN 160
#define RED_HUE_MAX 15
#define RED_SAT_MIN 90
#define RED_SAT_MAX 255
#define RED_VAL_MIN 90
#define RED_VAL_MAX 255

#define ENABLE_BLK 0
#define BLK_HUE_MIN 0
#define BLK_HUE_MAX 180
#define BLK_SAT_MIN 0
#define BLK_SAT_MAX 255
#define BLK_VAL_MIN 0
#define BLK_VAL_MAX 60

#define DEFAULT_PERSPECTIVE_MATRIX_FILENAME "perspective_matrix.yml"
#define DEFAULT_CAMERA_MATRIX_FILENAME "calibration_camera.yml"
#define DEFAULT_PARAMS_FILENAME "params.yml"

#endif

# -*- coding: utf-8 -*-
"""
Ce fichier regroupe toutes les constantes de l'IA
"""

import math

TEST_MODE = True #Permet des tester l'IA sans avoir besoin d'être connecté aux robots




#====================Enable====================
ENABLE_TOURELLE =		True
ENABLE_FLUSSMITTEL = 	True #permet de desactiver Flussmitel
ENABLE_TIBOT =			True

#========================================Communication========================================
PORT_XBEE = 			"/dev/ttyUSB0"
VITESSE_XBEE = 			57600
PARITY_XBEE = 			"ODD"
PORT_OTHER = 			"/dev/ttyACM0"
VITESSE_OTHER = 		57600
PARITY_OTHER = 			"ODD"


#constantes réglables:
MAX_UNCONFIRMED_PACKET =2 # maximum 32
TIMEOUT = 				200
HIGH_PRIO_SPEED = 		20 #période d'execution en ms
LOW_PRIO_SPEED = 		3000 #période d'execution en ms
KEEP_CONTACT_TIMEOUT = 	8000
OFF_LIGNE_TIMEOUT = 	20000


#Systèmes arretable:
THREAD_ACTIF = 			True
WRITE_OUTPUT = 			True
READ_INPUT = 			True
PROBING_DEVICES = 		True
RENVOI_ORDRE = 			True
KEEP_CONTACT = 			True
renvoiImmediat = 		False # fonction non terminé, ne pas activer !


#=======================================IA========================================

#====================Variables globales====================
NUMBER_OF_ENEMY = 		2 #TODO
#si 1, on considère que l'ennemi est petit

#====================eventManager====================
PERIODE_EVENT_MANAGER =	2
ID_ACTION_MAX =			29999
DELAY_IGNORE_ASSER_BLOCKED = 2000

#====================timeManager====================
PERIODE_TIME_MANAGER =	100
END_OF_MATCH = 			89000
BEGIN_FUNNY_ACTION =	92000
END_OF_FUNNY_ACTION = 	94500
BEGIN_CHECK_COLLISION =	0

#====================Goal====================
FINISHED_THRESHOLD = 	50
OBJECTIF_SEARCH_PERIODE = 1000

#====================pullData====================
PULL_SYSTEM_PERIODE = 	10 #période du système de pull en ms
PULL_PERIODE = 			100


#====================NAVIGATION================
EMPTY_FIFO = 			True
POINTS_PAR_CERCLE = 	8
MARGE_PASSAGE_PATH = 	10
MARGE_COLLISION =		-20
COLLISION_THRESHOLD =	400
COLLISION_WARNING_THRESHOLD = 800







#=======================================Systemes physiques========================================
#====================tourelle====================
OUR_ROBOTS_VISIBLE_TOURELLE = True 	#True si une balise visible par l'hokuyo est presente sur nos robots 
TOURELLE_PULL_PERIODE = 100 		#ms
DISTANCE_MAX_ROBOT_FUSION = 300 #Différance max entre codeurs et hokuyo

#====================Flussmittel====================
START_POSITION_RED_FLUSSMITTEL = (205, 1878, -1.57079) # true start pos
LARGEUR_FLUSSMITTEL = 	270 # ok car centré en largeur
LONGUEUR_FLUSSMITTEL = 	330 # = 2 fois la distance entre le centre de rotation et le côté le plus loin
MAX_FRONT_TRIANGLE_STACK = 3
MAX_FRONT_TRIANGLE_STACK_STORE = 2
MAX_BACK_TRIANGLE_STACK = 1
GARDE_AU_SOL = 16
HAUTEUR_TRIANGLE = 30
MARGE_DROP_TRIANGLE = 0
HAUTEUR_TORCHE = 36
# TODO mesures avec précision
# Attention, prendre en compte le fait que la ventouse est décalée par rapport à la glissière (il faut décaler angle_min et angle_max, ça devrait suffire)
ANGLE_MIN = math.radians(-90)
ANGLE_MAX = math.radians(-3)
OUVERTURE_BRAS_MIN = 132
OUVERTURE_BRAS_MAX = 132+225
MARGE_OUVERTURE_BRAS_MAX_DEPLACEMENT = 20
MARGE_OUVERTURE_BRAS_MIN_DEPLACEMENT = 20
CENTRE_BRAS_X = 128
CENTRE_BRAS_Y = 130
NB_VISIO_TRY = 10
NB_VISIO_DATA_NEEDED = 3
VISIO_MAX_DIST_TRIANGLE = 400


#====================TIBOT====================
START_POSITION_RED_TIBOT = (55, 1475, 0.0)
LARGEUR_TIBOT = 		200
LONGUEUR_TIBOT = 		150


#====================VISIO====================
MIN_X_TRIANGLE = 190
MAX_X_TRIANGLE = 500
MIN_Y_TRIANGLE = -200
MAX_Y_TRIANGLE = 200
MAX_SIZE_TRIANGLE_TORCH = 22000
MAX_SIZE_TRIANGLE = 8000
MIN_SIZE_TRIANGLE_TORCH = 10000




#====================ENEMYs====================
FIRST_POSITION_BIG_RED_ENNEMY = (187, 1870)
FIRST_POSITION_SMALL_RED_ENNEMY = (193, 1542)

#====================BIG ENEMY====================
#Si un seul adversaire, on utilise les constantes de BIG ENEMY
RAYON_BIG_ENEMY = 		200

#====================SMALL ENEMY====================
RAYON_SMALL_ENEMY = 	120




#==================== Choix d'objectif ====================
ENNEMI_CAN_CLEAN_ZONE = True

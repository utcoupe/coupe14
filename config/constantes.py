# -*- coding: utf-8 -*-
"""
Ce fichier regroupe toutes les constantes de l'IA
"""

import math

TEST_MODE = False #Permet des tester l'IA sans avoir besoin d'être connecté aux robots




#====================Enable====================
ENABLE_TOURELLE = 		False
ENABLE_FLUSSMITTEL = 	True #permet de desactiver Flussmitel
ENABLE_TIBOT = 			False

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

#====================timeManager====================
PERIODE_TIME_MANAGER =	100
END_OF_MATCH = 			89500
BEGIN_FUNNY_ACTION =	90000
END_OF_FUNNY_ACTION = 	94000
BEGIN_CHECK_COLLISION =	3000 #TODO

#====================Goal====================
FINISHED_THRESHOLD = 	50

#====================pullData====================
PULL_SYSTEM_PERIODE = 	10 #période du système de pull en ms
PULL_PERIODE = 			100


#====================NAVIGATION================
EMPTY_FIFO = 			True
POINTS_PAR_CERCLE = 	8
MARGE_PASSAGE_PATH = 	0
MARGE_COLLISION =		-20
COLLISION_THRESHOLD =	150
COLLISION_WARNING_THRESHOLD = 500


#=======================================Systemes physiques========================================
#====================tourelle====================
OUR_ROBOTS_VISIBLE_TOURELLE = True 	#True si une balise visible par l'hokuyo est presente sur nos robots 
TOURELLE_PULL_PERIODE = 100 		#ms
DISTANCE_MAX_ROBOT_FUSION = 250 #Différance max entre codeurs et hokuyo

#====================Flussmittel====================
START_POSITION_RED_FLUSSMITTEL = (187, 1870, -1.57)
LARGEUR_FLUSSMITTEL = 	330 # ok car centré en largeur
LONGUEUR_FLUSSMITTEL = 	340 # = 2 fois la distance entre le centre de rotation et le côté le plus loin
MAX_FRONT_TRIANGLE_STACK = 3
MAX_BACK_TRIANGLE_STACK = 1
GARDE_AU_SOL = 16
HAUTEUR_TRIANGLE = 30
MARGE_DROP_TRIANGLE = 0
HAUTEUR_TORCHE = 36
# TODO mesures avec précision
# Marges 20mm, 5°
ANGLE_MIN = math.radians(-75)
ANGLE_MAX = math.radians(0)
OUVERTURE_BRAS_MIN = 125
OUVERTURE_BRAS_MAX = 235
CENTRE_BRAS_X = 128
CENTRE_BRAS_Y = 130

#====================TIBOT====================
START_POSITION_RED_TIBOT = (2813, 1870, -1.57)
LARGEUR_TIBOT = 		200
LONGUEUR_TIBOT = 		150

#====================ENEMYs====================
FIRST_POSITION_BIG_RED_ENNEMY = (-1000, -1000)
FIRST_POSITION_SMALL_RED_ENNEMY = (-1000, -1000)
FIRST_POSITION_BIG_YELLOW_ENNEMY = (-1000, -1000)
FIRST_POSITION_SMALL_YELLOW_ENNEMY = (-1000, -1000)

#====================BIG ENEMY====================
#Si un seul adversaire, on utilise les constantes de BIG ENEMY
RAYON_BIG_ENEMY = 		200

#====================SMALL ENEMY====================
RAYON_SMALL_ENEMY = 	120


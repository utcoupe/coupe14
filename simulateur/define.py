# -*- coding: utf-8 -*-

import os
import sys

current_path = os.getcwd()
sys.path.insert(0, os.path.join( current_path, "pymunk-4.0.0" ) )

from pymunk import inf as MASS_INF
from pygame.locals import *



#=========================================================
#=== Ces constantes ne concernent QUE le simulateur !! ===
#=========================================================



FPS					= 30
PX_TO_MM			= 4 #définit la résolution du simulateur à l'écran


#type de collision pour identifier les objets
COLLTYPE_DEFAULT		= 0
COLLTYPE_WALL			= 1
COLLTYPE_GROS_ROBOT		= 2
COLLTYPE_PETIT_ROBOT	= 3
COLLTYPE_BRAS			= 4
COLLTYPE_FEU			= 5
COLLTYPE_TORCHE			= 6
COLLTYPE_ARBRE			= 7
COLLTYPE_FRESQUE		= 8
COLLTYPE_MAMMOUTH		= 9
COLLTYPE_FOYER   		= 10
COLLTYPE_BAC			= 11
COLLTYPE_BRAS_OUVRIR	= 12
COLLTYPE_BRAS_FERMER	= 13
COLLTYPE_BRAS_PETIT		= 14

YELLOW		= 0
RED			= 1
BIG			= 0
MINI		= 1
LEFT		= 0
RIGHT		= 1

#constantes de contrôle du simulateur au clavier
KEY_CHANGE_TEAM		= K_LSHIFT		# changer d'equipe
KEY_CHANGE_ROBOT	= K_LCTRL		# changer de robot
KEY_STOP_RESUME		= K_SPACE		# apppui = stop, relache = resume
KEY_CANCEL			= K_ESCAPE		# cancel
KEY_DROP			= K_d			# vider le gros robot
KEY_BRAS			= K_b			# add or remove bras
KEY_BALAIS_LEFT		= K_q			# sortir le balais de gauche
KEY_BALAIS_RIGHT	= K_w			# sortir le balais de droite
KEY_BULDO			= K_x			# mode buldozer
KEY_TELEPORTATION	= K_t			# mode téléportation
KEY_RECUL			= K_r			# mode marche arrière
KEY_JACK			= K_j			# jack

# dimensions du petit robot
WIDTH_MINI 		= 200
HEIGHT_MINI 	= 138
# dimensions du gros robot
WIDTH_GROS 		= 330
HEIGHT_GROS 	= 270
#données du gros robot
LONGUEUR_BRAS	= 225

################################################
# CONSTANTES EXTERNES POUR COMMUNICATION
################################################

ADDR_FLUSSMITTEL_OTHER	= 1
ADDR_FLUSSMITTEL_ASSERV	= 2
ADDR_FLUSSMITTEL_CAM	= 3
ADDR_TIBOT_OTHER		= 4
ADDR_TIBOT_ASSERV		= 5
ADDR_TOURELLE			= 6

PINGPING		= 1
A_GOTOA			= 2
A_GOTO			= 3
A_GOTOAR		= 4
A_GOTOR			= 5
A_ROT			= 6
A_ROTR			= 7
A_KILLG 		= 8
A_CLEANG		= 9
A_PIDA			= 10
A_PIDD			= 11
A_GET_CODER		= 12
A_PWM			= 13
A_ACCMAX		= 14
A_RESET_POS		= 15
A_GET_POS		= 16
A_GET_POS_ID	= 17

O_BRAS_OUVRIR	= 30
O_BRAS_FERMER	= 31
O_RET_OUVRIR	= 32
O_RET_FERMER	= 33
O_MONTER_ASC	= 34
O_BAISSER_ASC	= 35

T_GET_CAM		= 50
T_GET_HOKUYO	= 51
GET_LAST_ID 	= 52

################################################
# CONSTANTES INTERNES AU SIMULATEUR
################################################

GOTO	= 1
GOTOR	= 2
GOTOA	= 3
GOTOAR	= 4
ROT		= 5
ROTR	= 6
CLEANG	= 7
PWM		= 8


################################################
# METHODES GENERIQUES DU SIMULATEUR
################################################

def mm_to_px(*args):
	"""
	Convertis une donnée en milimètres vers une donnée en pixels.
	@param args une liste ou un atom de valeurs ou de positions
	@param la valeur ou la liste convertie

	>>> mm_to_px(4) == int(4/PX_TO_MM)
	True

	>>> mm_to_px((4,8)) == (mm_to_px(4),mm_to_px(8))
	True

	>>> mm_to_px((4,8),(16,32)) == ((mm_to_px(4),mm_to_px(8)), (mm_to_px(16),mm_to_px(32)))
	True

	>>> mm_to_px([(4,8),(16,32)]) == mm_to_px((4,8),(16,32))
	True

	>>> mm_to_px(*[(4,8),(16,32)]) == mm_to_px((4,8),(16,32))
	True
	
	"""
	def f(a):
		if isinstance(a,tuple) or isinstance(a,list):
			return mm_to_px(*a)
		else:
			return int(a / PX_TO_MM)
	if len(args) == 1:
		return f(args[0])
	else:
		return tuple(map(lambda v: f(v), args))

def px_to_mm(*args):
	"""
	Convertis une donnée en pixels vers une donnée en milimètres
	@param args une liste ou un atom de valeurs ou de positions
	@param la valeur ou la liste convertie
	"""
	def f(a):
		if isinstance(a,tuple) or isinstance(a,list):
			return px_to_mm(*a)
		else:
			return int(a * PX_TO_MM)
	if len(args) == 1:
		return f(args[0])
	else:
		return tuple(map(lambda v: f(v), args))
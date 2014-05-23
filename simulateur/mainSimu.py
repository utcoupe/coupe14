#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simulateur permettant de simuler un match d'eurobot.

Déplacer gros robot: clic gauche
Déplacer petit robot: clic droit

Déplacer adversaire: idem + ctrl

@author Thomas Recouvreux
@author Pierre-Henry Fricot
@author Cédric Bache

Pour la version 2013, nous avons utilisé le nouveau protocole de communication zérobot. Les objets et engines sont également réécrit pour adapter au nouveau reglement.
@author Siqi LIU <me@siqi.fr>
@author Florent Thévenet <florent@fthevenet.fr>
@author Thomas Fuhrmann <tomesman@gmail.com>

"""


import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "map"))
sys.path.append(os.path.join(DIR_PATH, "..", "gui"))
sys.path.append(os.path.join(DIR_PATH, "../ia", "constantes"))


import optparse
import threading
import time

from engine import *
import match
from map import maploader
from objects import bigrobot, minirobot
import processIA
from constantes import *
from gui import mainGUI

if __name__ == "__main__":

#====================Activation des IA====================
		"""
		Mettre à Flase l'IA qu'on veut désactiver.
		Ne pas toucher au reste du code.
		"""

		redIA = True
		yellowIA = False

#=========================================================
#======= Pas besoin de toucher à la suite du code ========
#=========================================================

		engine = Engine()
		match = match.Match()

		# robots
		bigbotRed = bigrobot.BigRobot(engine = engine,
							posinit = mm_to_px(180, 200),
							team = RED)
		minibotRed = minirobot.MiniRobot(engine = engine,
							  posinit = mm_to_px(70, 570),
							  team = RED)
		bigbotYellow = bigrobot.BigRobot(engine = engine,
							 posinit = mm_to_px(3000-180,200),
							 team = YELLOW)
		minibotYellow = minirobot.MiniRobot(engine = engine,
							   posinit = mm_to_px(3000-100,690),
							   team = YELLOW)

		#ne pas toucher des drapaux !
		bigbotRed_flag = False
		minibotRed_flag = False
		bigbotYellow_flag = False
		minibotYellow_flag = False

		robots_red = None
		robots_yellow = None

		if redIA == True:
			if ENABLE_FLUSSMITTEL == True:
				if ENABLE_TIBOT == True:
					bigbotRed_flag = True
					minibotRed_flag = True
					robots_red = ("RED", bigbotRed, minibotRed, bigbotYellow, minibotYellow)
				else:
					bigbotRed_flag = True
					robots_red = ("RED", bigbotRed, None, bigbotYellow, minibotYellow)
			else:
				if ENABLE_TIBOT == True:
					minibotRed_flag = True
					robots_red = ("RED", None, minibotRed, bigbotYellow, minibotYellow)
			#lancement de l'IA
			processIA.ProcessIA(robots_red)
		else:
			bigbotRed_flag = True
			minibotRed_flag = True

		if yellowIA == True:
			if ENABLE_FLUSSMITTEL == True:
				if ENABLE_TIBOT == True:
					bigbotYellow_flag = True
					minibotYellow_flag = True
					robots_yellow = ("YELLOW", bigbotYellow, minibotYellow, bigbotRed, minibotRed)
				else:
					bigbotYellow_flag = True
					robots_yellow = ("YELLOW", bigbotYellow, None, bigbotRed, minibotRed)
			else:
				if ENABLE_TIBOT == True:
					minibotYellow_flag = True
					robots_yellow = ("YELLOW", None, minibotYellow, bigbotRed, minibotRed)
			#lancement de l'IA
			processIA.ProcessIA(robots_yellow)
		else:
			bigbotYellow_flag = True
			minibotYellow_flag = True

		if bigbotRed_flag == True:
			engine.add(bigbotRed)
		if minibotRed_flag == True:
			engine.add(minibotRed)
		if bigbotYellow_flag == True:
			engine.add(bigbotYellow)
		if minibotYellow_flag == True:
			engine.add(minibotYellow)

		#chargement de la map
		maploader.load_map("map/map.xml",engine)

		t=threading.Thread(target=engine.start)
		t.setDaemon(True)
		t.start()

		#start de la GUI
		if robots_red != None:
			threading.Thread(target=mainGUI.GUISimu,args=(robots_red,)).start()
		elif robots_yellow != None:
			threading.Thread(target=mainGUI.GUISimu,args=(robots_yellow,)).start()

		while not engine.e_stop.is_set():
				try:
						engine.e_stop.wait(3)
				except KeyboardInterrupt:
						engine.stop()
						break



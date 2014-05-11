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
sys.path.append(os.path.join(DIR_PATH, "../../ia", "constantes"))


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

#====================Activation des IA====================
		"""
		Mettre à Flase l'IA qu'on veut désactiver.
		Ne pas toucher au reste du code.
		"""
		redIA = True
		yellowIA= False

#=========================================================
		#ne pas toucher des drapaux !
		bigbotRed_flag = False
		minibotRed_flag = False
		bigbotYellow_flag = False
		minibotYellow_flag = False


		if redIA == True:
			if ENABLE_FLUSSMITTEL == True:
				if ENABLE_TIBOT == True:
					bigbotRed_flag = True
					minibotRed_flag = True
					robots_red = ("RED", bigbotRed, minibotRed, bigbotYellow, minibotYellow)
				else:
					bigbotRed_flag = True
					robots_red = ("RED", bigbotRed, bigbotYellow, minibotYellow)
			else:
				if ENABLE_TIBOT == True:
					minibotRed_flag = True
					robots_red = ("RED", minibotRed, bigbotYellow, minibotYellow)
			#robots_red = ("RED", bigbotRed, minibotRed, bigbotYellow, minibotYellow)
			#mainGUI.GUISimu(robots_red)
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
					robots_yellow = ("YELLOW", bigbotYellow, bigbotRed, minibotRed)
			else:
				if ENABLE_TIBOT == True:
					minibotYellow_flag = True
					robots_yellow = ("YELLOW", minibotYellow, bigbotRed, minibotRed)
			#robots_yellow = ("YELLOW", bigbotYellow, minibotYellow, bigbotRed, minibotRed)
			#mainGUI.GUISimu(robots_yellow)
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
		#guiRed = mainGUI.GUISimu(robots_red)
		#threading.Thread(target=guiRed.start).start()
		#guiRed.start()

		while not engine.e_stop.is_set():
				try:
						engine.e_stop.wait(3)
				except KeyboardInterrupt:
						engine.stop()
						break



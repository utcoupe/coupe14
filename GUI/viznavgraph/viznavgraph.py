# -*- coding: utf-8 -*-

import sys
import os
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(FILE_DIR, "../../ia"))
sys.path.append(os.path.join(FILE_DIR, "../../libs"))

import time
import threading

from graphview import *
from event.goals import navigation

class Bot(dict):
	def __init__(self):
		self["getRayon"] = 0
		self["getPosition"] = (-1000, -1000)

def startVizNavGraph(liste_bots):
	filename = os.path.join(FILE_DIR, "../../ia/event/goals/navigation/map.xml")
	try:
		offset = sys.argv[1]
	except:
		offset = 0
	start = time.time()
	#used = celui pour lequel on fait le calcule de trajectoire
	#other = l'autre de notre équipe
	#!! création des 4 robots
	other_bot = Bot()
	other_bot["getPosition"] = liste_bots[2].getPositionXY()
	other_bot["getRayon"] = 120
	used_bot = Bot()
	used_bot["getPosition"] = liste_bots[1].getPositionXY()
	used_bot["getRayon"] = 200
	ennemy1 = Bot()
	ennemy2 = Bot()
	ennemy1["getPosition"] = liste_bots[3].getPositionXY()
	ennemy1["getRayon"] = 200
	ennemy2["getPosition"] = liste_bots[4].getPositionXY()
	ennemy2["getRayon"] = 120
	liste_bots_nav = [used_bot,other_bot,ennemy1,ennemy2]
	ng = navigation.PathFinding([used_bot, other_bot, ennemy1, ennemy2], filename)
	print("init time : %s" % (time.time() - start))
	v = GraphView(ng, liste_bots_nav, liste_bots)
	#taille de la fenêtre et position sur l'écran (par défaut en haut à droite
	w_fen = v.winfo_screenwidth()
	h_fen = v.winfo_screenheight()
	x_fen = w_fen/10
	y_fen = h_fen/2
	my_w = w_fen/2.3
	my_h = h_fen/2
	v.geometry("%dx%d+%d+%d" % (my_w,my_h,x_fen,y_fen))

	v.mainloop()

if __name__ == "__main__":
	startVizNavGraph()


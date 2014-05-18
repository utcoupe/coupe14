# -*- coding: utf-8 -*-

import sys
import os
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(FILE_DIR, "../../ia"))
sys.path.append(os.path.join(FILE_DIR, "../../libs"))

import time

from .graphview import *
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
	other_bot = Bot()
	#other_bot["getRayon"] = 200
	used_bot = Bot()
	#used_bot["getRayon"] = 200
	ennemy1 = Bot()
	ennemy2 = Bot()
	"""ennemy1["getPosition"] = (1800, 1500)
	ennemy1["getRayon"] = 200
	ennemy2["getPosition"] = (2200, 500)
	ennemy2["getRayon"] = 120"""
	ng = navigation.PathFinding([used_bot, other_bot, ennemy1, ennemy2], filename)
	print("init time : %s" % (time.time() - start))
	
	v = GraphView(ng, other_bot, used_bot)
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


__author__ = 'furmi'

from tkinter import *
import gui_general
import gui_robots
import gui_actions
import gui_actionneurs
import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "objects"))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
from define import *

class GUISimu(Tk):
	def __init__(self, robots):
		Tk.__init__(self,None)
		#print('GUI trobots : ', robots)
		self.__liste_robots = robots
		self.title("GUI trop stylée pour le simulateur")
		#taille de la fenêtre et position sur l'écran (par défaut en haut à droite
		w_fen = self.winfo_screenwidth()
		h_fen = self.winfo_screenheight()
		x_fen = w_fen/1.7
		y_fen = 0
		my_w = w_fen/2.5
		my_h = h_fen/1.5
		self.geometry("%dx%d+%d+%d" % (my_w,my_h,x_fen,y_fen))
		# lancement des différentes frames de la GUI
		self.__wids = gui_general.general(self, self.__liste_robots)
		self.__robots = gui_robots.robots(self,self.__liste_robots)
		self.__actions = gui_actions.actions(self,self.__liste_robots)
		self.__effecteur = gui_actionneurs.actionneurs(self,self.__liste_robots)
		self.start()


	def start(self):
		"""
		Démarre la GUI
		"""
		self.mainloop()

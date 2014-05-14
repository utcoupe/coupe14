__author__ = 'furmi'

from tkinter import *
import gui_general
import gui_robots
import gui_actions
import gui_actionneurs

class GUISimu():
	def __init__(self, robots):
		self.__liste_robots = robots
		self.__fen = Tk()
		self.__fen.title("Test de GUI pour le simulateur")
		#taille de la fenêtre et position sur l'écran
		w_fen = self.__fen.winfo_screenwidth()
		h_fen = self.__fen.winfo_screenheight()
		x_fen = w_fen/1.7
		y_fen = 0
		my_w = w_fen/2.5
		my_h = h_fen/1.5
		self.__fen.geometry("%dx%d+%d+%d" % (my_w,my_h,x_fen,y_fen))
		# exemple d'utilisation:
		self.__wids = gui_general.general(self.__fen, self.__liste_robots)
		self.__robots = gui_robots.robots(self.__fen,self.__liste_robots)
		self.__actions = gui_actions.actions(self.__fen,self.__liste_robots)
		self.__effecteur = gui_actionneurs.actionneurs(self.__fen,self.__liste_robots)
		#self.__fen.mainloop()

	def start(self):
		self.__fen.mainloop()

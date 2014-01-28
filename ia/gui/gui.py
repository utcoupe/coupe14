from threading import Thread
from time import sleep
from tkinter import *

sys.path.append("..")
from constants import * 

GUI_TAILLE_FENETRE_X = 750
GUI_TAILLE_FENETRE_Y = 500

def calcRealPos(pos):
	return [pos[0]*GUI_TAILLE_FENETRE_X/TAILLE_TABLE_X, (TAILLE_TABLE_Y-pos[1])*GUI_TAILLE_FENETRE_Y/TAILLE_TABLE_Y]
def calcRealSize2(size):
	return [size[0]*GUI_TAILLE_FENETRE_X/(TAILLE_TABLE_Y*2), size[1]*GUI_TAILLE_FENETRE_Y/(TAILLE_TABLE_Y*2)]
def calcRealPosAndSize(pos, size) :
	"""print("calcRealPosAndSize")
	print("pos:"+str(pos))
	print("realpos"+str(calcRealPos((pos[0], pos[1]))))
	print("size:"+str(size))"""
	s = calcRealSize2(size)
	r = calcRealPos((pos[0]-s[0], pos[1]-s[1]))
	r.extend( calcRealPos((pos[0]+s[0], pos[1]+s[1])) )
	#print(str(r))
	return r
class GUI:
	def __init__ (self):
		self.thread = Thread(target = self.startGUI)
		self.thread.start()

	def startGUI (self):
		self.fen = Tk()
		self.fen.title("GUI Simulateur")

		self.can = Canvas(self.fen, bg='white', width=GUI_TAILLE_FENETRE_X, height=GUI_TAILLE_FENETRE_Y)
		self.can.pack()

		for i  in range(MAX_ROBOTS):
			self.can.create_oval(0, 0, 100, 100, fill="gray", width=0)

		self.fen.mainloop()

	def displayRobots(self, coords):
		for i in range(len(coords)):
			#print("displayRobots iteration "+str(i))
			#print(str(calcRealPosAndSize(coords[i], (ROBOTS_SIZE, ROBOTS_SIZE))))
			self.can.coords(i+1, *calcRealPosAndSize(coords[i], (ROBOTS_SIZE, ROBOTS_SIZE)))
		for i in range(len(coords), MAX_ROBOTS):
			self.can.coords(i+1, 0, 0, 0, 0)








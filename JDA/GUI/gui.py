# -*- coding: utf-8 -*-

from Tkinter import *
from ../../ia/communication import communicationGlobale

class GUI:
	def __init__(self):
		#defines
		self.widthfen = 800
		self.heightfen = 600

		self.areax = 3000
		self.areay = 2000

		#init comm
		self.com = communicationGlobale.communicationGlobale("/dev/ttyUSB0", 57600, "ODD", "/dev/ttymxc3", 115200, "NONE", "/dev/ttyACM0", 115200, "ODD")
		
		#init GUI
		self.fen = Tk()
		self.fen.title("Clique moi")
		self.cadre = Frame(fen, width = self.widthfen, height = self.heightfen, bg="light yellow")
		self.cadre.bind("<Button-1>", clic)
		self.cadre.pack()
		self.chaine = Label(fen)
		self.chaine.pack()
		self.fen.mainloop()

	def clic(self, event):
		gotox = (event.x/800.0)*self.areax
		gotoy = (event.y/800.0)*self.areay
		self.chaine.configure(text = "Goto : "+str(gotox)+" ; "+str(gotoy))
		#ENVOYER DATA PROTOCOLE
		argmuents = [gotox, gotoy]
		com.sendOrderAPI(2, 'A_GOTO', *arguments) 


if __name__ == '__main__':
	gui = GUI()

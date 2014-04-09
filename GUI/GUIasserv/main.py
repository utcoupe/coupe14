import sys
sys.path.append('../../ia/')

import communication
from tkinter import *
from math import cos, sin, pi, atan2


class GUI:
	def __init__(self):
		self.period = 100
		self.widthfen = 800
		self.heightfen = 400

		self.x_offset = 0
		self.y_offset = 0
		self.a_offset = 0
		self.x_scale = 1 
		self.y_scale = 1

		self.viz_y_scale = 1
		"""
		if ENABLE_FLUSSMITTEL and ENABLE_TIBOT:
			print("Les deux robots sont activé : un seul doit l'être")
			return
		if not ENABLE_FLUSSMITTEL and not ENABLE_TIBOT:
			print("Aucun robot actif")
			return
		if ENABLE_FLUSSMITTEL:
			robot = 'FLUSSMITTEL'
			self.robotaddr = 2
			print("Asservissement de FlussMittel")
		else:
			robot = 'TIBOT'
			self.robotaddr = 5
			print("Asservissement de Tibot")

		com = communication.CommunicationGlobale()
		arduino_constantes = com.getConst()
		self.Data = data.Data(Communication, arduino_constantes)
		#sleep ?
		self.robot_data = Data.dataToDico()[robot]

		self.last_pos = robot_data["getPositionAndAngle"]
		self.path = []
		"""
		robot =""
		self.fen = Tk()
		self.fen.title("Asservissement " + robot)
		self.goto_frame = Frame()
		self.goto_e = Entry(self.goto_frame)

		self.send_goto = Button(self.goto_frame, text="Goto", command=self.goto_handler).grid(column=1, row=0)
		self.reset_button = Button(self.goto_frame, text="Reset", command=self.resetPos).grid(column=2, row=0)
		self.goto_e.grid(column=0, row=0)
		self.goto_frame.pack()

		self.scale_frame = Frame()
		self.inc_scale_b = Button(self.scale_frame, text="+", command=incScale).grid(column=1, row=0)
		self.dec_scale_b = Button(self.scale_frame, text="-", command=decScale).grid(column=2, row=0)
		self.scale_txt = Label(self.scale_frame, text=str(self.viz_y_scale))


		self.zone = Canvas(self.fen, width=self.widthfen, height=self.heightfen, bg="white")
		self.zone.pack()

		self.drawRobot(400,300,0)

		self.resetPos()
		self.fen.mainloop()

	def drawRobot(self, x, y, a):
		size = 10
		pts = []
		try:
			self.zone.delete(self.poly)
		except:
			pass

		for i in range(3):
			size_temp = size
			if i == 0:
				size_temp = size*1.5
			pts.append((x+(size_temp*cos(a+self.a_offset+i*2*pi/3))+self.x_offset)*self.x_scale)
			pts.append(self.heightfen - (y+(size_temp*sin(a+self.a_offset+i*2*pi/3))+self.y_offset)*self.y_scale)

		self.poly = self.zone.create_polygon(*pts, fill='', outline='red', width=2)

	def resetPos(self):
		args = (0, 0, 0.0)
		self.com.sendOrderAPI(self.robotaddr, 'A_SET_POS', *args)

	def goto_handler(self):
		self.robot_data = self.Data.dataToDico()[robot]
		self.last_pos = robot_data["getPositionAndAngle"]
		self.path.append(self.last_pos)
		self.go = int(self.goto_e.get())
		xoff = 100

		self.x_offset = xoff/2 - self.last_pos[0]
		self.y_offset = self.heightfen/2

		self.x_scale = (self.widthfen - xoff)/(self.go - self.last_pos[0])
		self.y_scale = self.x_scale * self.viz_y_scale
		self.com.sendOrderAPI(self.robotaddr, 'A_GOTO', *self.go)

		#TODO draw direct line
		#self.looper()

	def drawPath(self):
		while len(self.lines) > 1:
			self.zone.delete(self.lines.pop())
		for (p1, p2) in zip(self.path[:-1], self.path[1:]):
			self.drawLine(p1[0], p1[1], p2[0], p2[1], color='red')

	def looper(self):
		self.robot_data = self.Data.dataToDico()[robot]
		new_pos = robot_data["getPositionAndAngle"]
		if (new_pos != last_pos):
			drawRobot(*new_pos)
			self.drawLine(last_pos[0], last_pos[1], new_pos[0], new_pos[1], color='red')
			#TODO draw lines
			last_pos = new_pos
		self.fen.after(self.period, looper)
	
	def incScale(self):
		self.viz_y_scale *= 2
		self.scale_txt.config(text=str(self.viz_y_scale))
		self.updateViz()

	def decScale(self):
		self.viz_y_scale /= 2
		self.scale_txt.config(text=str(self.viz_y_scale))
		self.updateViz()

	def updateViz(self):
		self.y_scale = self.x_scale * self.viz_y_scale
		self.drawPath()

if __name__ == '__main__':
	a = GUI()	

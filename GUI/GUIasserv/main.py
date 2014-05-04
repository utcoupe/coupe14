import sys
sys.path.append('../../ia/')

import communication
import data
from tkinter import *
from math import cos, sin, pi
from constantes import *
import logging
import os
import time


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

		robot = ""
		self.viz_y_scale = 1.0
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

		try:
			self.com = communication.CommunicationGlobale()
			arduino_constantes = self.com.getConst()
			self.Data = data.Data(self.com, arduino_constantes)
			self.robot_data = self.Data.dataToDico()[robot]
			self.last_pos = self.robot_data["getPositionAndAngle"]
			print("Wait, com is initializing")
			time.sleep(2)
			self.Data.startPullData()
			#sleep ?
		except:
			self.last_pos = (0, 0, 0)
			print("Pas de communication")

		self.path = []
		self.lines = []
		self.fen = Tk()
		self.fen.title("Asservissement " + robot)
		self.goto_frame = Frame()
		self.goto_e = Entry(self.goto_frame)
		self.robot = robot

		self.send_goto = Button(self.goto_frame, text="Goto", command=self.goto_handler).grid(column=1, row=0)
		self.reset_button = Button(self.goto_frame, text="Reset", command=self.resetPos).grid(column=2, row=0)
		self.goto_e.grid(column=0, row=0)

		self.scale_frame = Frame()
		self.inc_scale_b = Button(self.scale_frame, text="+", command=self.incScale)
		self.inc_scale_b.grid(column=1, row=0)
		self.dec_scale_b = Button(self.scale_frame, text="-", command=self.decScale)
		self.dec_scale_b.grid(column=2, row=0)
		self.scale_txt = Label(self.scale_frame, text=str(self.viz_y_scale))
		self.scale_txt.grid(column=0, row=0)

		self.zone = Canvas(self.fen, width=self.widthfen, height=self.heightfen, bg="white")
		self.zone.pack(side='bottom')
		self.scale_frame.pack(side='right')
		self.goto_frame.pack(side='left')

		self.xoff = 100
		self.x_scale = 1 
		self.y_scale = 1
		self.a_offset = 0
		self.x_offset = self.xoff/2 - (self.last_pos[0] * self.x_scale)
		self.y_offset = self.heightfen/2

		self.drawRobot(*self.last_pos)

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
			pts.append(x*self.x_scale+(size_temp*cos(a+self.a_offset+i*2*pi/3))+self.x_offset)
			pts.append(self.heightfen - (y*self.y_scale+(size_temp*sin(a+self.a_offset+i*2*pi/3))+self.y_offset))

		self.poly = self.zone.create_polygon(*pts, fill='', outline='red', width=2)

	def resetPos(self):
		args = (0, 0, 0.0)
		self.com.sendOrderAPI(self.robotaddr, 'A_SET_POS', *args)
		self.clearPath();

	def drawLine(self, x1, y1, x2, y2, color='gray'):
		args = (x1*self.x_scale+self.x_offset,
				self.heightfen - (y1*self.y_scale+self.y_offset),
				x2*self.x_scale+self.x_offset,
				self.heightfen - (y2*self.y_scale+self.y_offset))

		self.lines.append(self.zone.create_line(*args, fill=color))

	def goto_handler(self):
		try:
			self.robot_data = self.Data.dataToDico()[self.robot]
			self.last_pos = self.robot_data["getPositionAndAngle"]
		except:
			self.last_pos = (0, 0, 0)
			print("Warning : no com")

		self.path.append(self.last_pos)
		self.go = (0,int(self.goto_e.get()), 0)

		self.x_scale = (self.widthfen - self.xoff)/(self.go[1] - self.last_pos[0])
		self.y_scale = self.x_scale * self.viz_y_scale

		self.x_offset = self.xoff/2 - (self.last_pos[0] * self.x_scale)
		self.y_offset = self.heightfen/2

		self.com.sendOrderAPI(self.robotaddr, 'A_GOTO', *self.go)

		self.drawLine(self.last_pos[0], self.last_pos[1], *self.go[1:])
		self.drawLine(self.path[0][0], self.path[0][1] - 10, self.path[0][0], self.path[0][1] + 10)

		self.looper()

	def drawPath(self):
		while len(self.lines) > 1:
			self.zone.delete(self.lines.pop())
		for (p1, p2) in zip(self.path[:-1], self.path[1:]):
			self.drawLine(p1[0], p1[1], p2[0], p2[1], color='red')
		self.drawLine(self.path[0][0], self.path[0][1] - 10, self.path[0][0], self.path[0][1] + 10)

	def clearPath(self):
		for i in range(1, len(self.lines)):
			self.zone.delete(self.lines[i])

	def looper(self):
		try:
			self.robot_data = self.Data.dataToDico()[self.robot]
			new_pos = self.robot_data["getPositionAndAngle"]
		except:
			new_pos = (self.last_pos[0]+2, self.last_pos[1]+1, 0)
			print("Warning : no com while drawing path")

		if (new_pos != self.last_pos):
			self.drawRobot(*new_pos)
			self.drawLine(self.last_pos[0], self.last_pos[1], new_pos[0], new_pos[1], color='red')
			self.last_pos = new_pos
			self.path.append(self.last_pos)
		self.fen.after(self.period, self.looper)

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
		self.clearPath();
		self.drawPath()

if __name__ == '__main__':
	logging.basicConfig(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.log"), filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	a = GUI()	

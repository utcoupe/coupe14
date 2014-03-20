# -*- coding: utf-8 -*-

class Bot:
	def __init__(self):
		self.ray = 100
		self.x = 0
		self.y = 0
	def getPosition(self):
		return (self.x, self.y)
	def getRayon(self):
		return self.ray
	def setPosition(self, pos):
		self.x = pos[0]
		self.y = pos[1]

if __name__ == "__main__":
	import sys
	import os
	FILE_DIR = os.path.dirname(os.path.abspath(__file__))
	sys.path.append(os.path.join(FILE_DIR,"..","..","ia"))
	sys.path.append(os.path.join(FILE_DIR,"..","..","libs"))
	
	import time
	
	from graphview import *
	from geometry import Poly
	import event.navigation
	import data
	
	filename = os.path.join(FILE_DIR,"..","..","ia","event","navigation","map.xml")
	try:
		offset= sys.argv[1]
	except:
		offset = 0
	start = time.time()
	moving_bot = Bot()
	self_bot = Bot()
	ng = event.navigation.PathFinding([self_bot, Bot(), moving_bot, Bot()], filename)
	print("init time : %s" % (time.time() - start))
	
	v = GraphView(ng, moving_bot, self_bot)
	v.mainloop()


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
	import random
	
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

	ng.update(self_bot)
	start_time = time.time()
	for i in range(10):
		moving_bot.setPosition((random.randint(0,3000), random.randint(0,2000)))
		ng.update(self_bot)
	print("Average duration of update : "+str((time.time() - start_time)/10))
	start_time = time.time()
	for i in range(100):
		path = ng.getPath((random.randint(0,3000), random.randint(0,2000)), (random.randint(0,3000), random.randint(0,2000)))
	print("Average duration of pathfinding : "+str((time.time() - start_time)/100))
	

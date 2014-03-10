# -*- coding: utf-8 -*-


class Bot:
	def __init__(self):
		self.ray = 100
		self.x = -1000
		self.y = -1000

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
	sys.path.append(os.path.join(FILE_DIR, "../../ia"))
	sys.path.append(os.path.join(FILE_DIR, "../../libs"))
	
	import time
	
	from graphview import *
	from event import navigation
	
	filename = os.path.join(FILE_DIR, "../../ia/event/navigation/map.xml")
	try:
		offset = sys.argv[1]
	except:
		offset = 0
	start = time.time()
	other_bot = Bot()
	used_bot = Bot()
	ennemy1 = Bot()
	ennemy2 = Bot()
	ennemy1.x = 1800
	ennemy1.y = 1500
	ennemy1.ray = 200
	ennemy2.x = 2200
	ennemy2.y = 500
	ng = navigation.PathFinding([used_bot, other_bot, ennemy1, ennemy2], filename)
	print("init time : %s" % (time.time() - start))
	
	v = GraphView(ng, other_bot, used_bot)
	v.mainloop()


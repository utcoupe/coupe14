# -*- coding: utf-8 -*-


class Bot:
	def __init__(self):
		self.ray = 100
		self.x = -1000
		self.y = -1000
		self.traj = []
		self.name = "default"

	def getPosition(self):
		return (self.x, self.y)

	def getRayon(self):
		return self.ray

	def setPosition(self, pos):
		self.x = pos[0]
		self.y = pos[1]

	def getTrajectoires(self):
		return self.traj

	def __repr__(self):
		return self.name + " at %s:%s" % (self.x, self.y)

if __name__ == "__main__":
	import sys
	import os
	FILE_DIR = os.path.dirname(os.path.abspath(__file__))
	sys.path.append(os.path.join(FILE_DIR, "../../ia"))
	sys.path.append(os.path.join(FILE_DIR, "../../libs"))
	
	import time
	
	from graphview import GraphView
	from event import navigation
	
	filename = os.path.join(FILE_DIR, "../../ia/event/navigation/map.xml")
	try:
		offset = sys.argv[1]
	except:
		offset = 0
	start = time.time()
	other_bot = Bot()
	other_bot.name = 'other'
	used_bot = Bot()
	used_bot.name = 'used'
	ennemy1 = Bot()
	ennemy1.name = 'en1'
	ennemy2 = Bot()
	ennemy2.name = 'en2'
	ennemy1.x = 1800
	ennemy1.y = 1500
	ennemy1.ray = 200
	ennemy2.x = 2200
	ennemy2.y = 500
	ng = navigation.PathFinding([used_bot, other_bot, ennemy1, ennemy2], filename)
	col = navigation.Collision([used_bot, other_bot, ennemy1, ennemy2])
	print("init time : %s" % (time.time() - start))
	
	v = GraphView(ng, col, other_bot, used_bot)
	v.mainloop()


# -*- coding: utf-8 -*-


class Bot(dict):
	def __init__(self):
		self["getRayon"] = 0
		self["getPosition"] = (-1000, -1000)
		self.traj = []
	def getTrajectoires(self):
		return self.traj
	def getRayon(self):
		return self["getRayon"]
	def getPosition(self):
		return self["getPosition"]

if __name__ == "__main__":
	import sys
	import os
	FILE_DIR = os.path.dirname(os.path.abspath(__file__))
	sys.path.append(os.path.join(FILE_DIR, "../../ia"))
	sys.path.append(os.path.join(FILE_DIR, "../../libs"))
	
	import time
	
	from graphview import GraphView
	from event.goals import navigation
	from event import collision
	
	filename = os.path.join(FILE_DIR, "../../ia/event/goals/navigation/map.xml")
	try:
		offset = sys.argv[1]
	except:
		offset = 0
	start = time.time()
	other_bot = Bot()
	other_bot.name = 'other'
	other_bot["getRayon"] = 200
	used_bot = Bot()
	used_bot.name = 'used'
	used_bot["getRayon"] = 120
	ennemy1 = Bot()
	ennemy1.name = 'en1'
	ennemy2 = Bot()
	ennemy2.name = 'en2'
	ennemy1["getPosition"] = (1800, 1500)
	ennemy1["getRayon"] = 200
	ennemy2["getPosition"] = (2200, 500)
	ennemy1["getRayon"] = 120
	ng = navigation.PathFinding([used_bot, other_bot, ennemy1, ennemy2], filename)
	col = collision.Collision([used_bot, other_bot, ennemy1, ennemy2])
	print("init time : %s" % (time.time() - start))
	
	v = GraphView(ng, col, other_bot, used_bot)
	v.mainloop()


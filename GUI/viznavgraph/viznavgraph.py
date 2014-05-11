# -*- coding: utf-8 -*-


class Bot(dict):
	def __init__(self):
		self["getRayon"] = 0
		self["getPosition"] = (-1000, -1000)

if __name__ == "__main__":
	import sys
	import os
	FILE_DIR = os.path.dirname(os.path.abspath(__file__))
	sys.path.append(os.path.join(FILE_DIR, "../../ia"))
	sys.path.append(os.path.join(FILE_DIR, "../../libs"))
	
	import time
	
	from graphview import *
	from event.goals import navigation
	
	filename = os.path.join(FILE_DIR, "../../ia/event/goals/navigation/map.xml")
	try:
		offset = sys.argv[1]
	except:
		offset = 0
	start = time.time()
	other_bot = Bot()
	other_bot["getRayon"] = 200
	used_bot = Bot()
	used_bot["getRayon"] = 200
	ennemy1 = Bot()
	ennemy2 = Bot()
	ennemy1["getPosition"] = (1800, 1500)
	ennemy1["getRayon"] = 200
	"""ennemy2["getPosition"] = (2200, 500)
	ennemy2["getRayon"] = 120"""
	ng = navigation.PathFinding([used_bot, other_bot, ennemy1, ennemy2], filename)
	print("init time : %s" % (time.time() - start))
	
	v = GraphView(ng, other_bot, used_bot)
	v.mainloop()


from pathfinding2012 import *
from constantes import *

class PathFinding:
	def __init__(self, robot_list, xml_filename):
		self.__flussmittel = robot_list[0]
		self.__tibot = robot_list[1]
		self.__big_enemy_bot = robot_list[2]
		self.__small_enemy_bot = robot_list[3]
		#on cree le navgraph
		self.__ng = nav.NavGraph(MARGE_PASSAGE, xml_filename)
		self.__init_enemy_bot()
		#on compte nos robots
		self.__our_bot_count = 0
		if ENABLE_FLUSSMITTEL:
			self.__our_bot_count += 1
		if ENABLE_TIBOT:
			self.__our_bot_count += 1
		#on met a jour tout les robots

		if ENABLE_FLUSSMITTEL:
			self.__our_bot = self.__flussmittel
			self.__other_bot = self.__tibot
		elif ENABLE_TIBOT:
			self.__our_bot = self.__tibot
			self.__other_bot = self.__flussmittel
		else:
			raise Exception("Aucun robot actif")
		self.__update(self.__our_bot)

	def update(self, robot):
		self.__update_enemy_bot()
		if self.__our_bot_count == 2: #Si on a deux robots, il faut compte le deuxieme dans le pathfinding
			self.__update_our_bot(robot)
		self.__ng.update()

	def getPath(self, start, end):
		foo, bar, path = self.__ng.get_path(start,end)
		return path

	def __update_our_bot(self, robot):
		"""Update le navgraph pour calculer une trajectoire pour le robot en paramètre"""
		if robot == self.__our_bot: #on met juste la position a jour
			self.__other_bot_poly.move_to(self.__other_bot.getRayon())
		else: #il faut recreer un nouveau poly a la bonne taille
			#swap des robots
			self.__other_bot = self.__our_bot
			self.__our_bot = robot
			#nouveau poly
			self.__other_bot_poly = Poly().initFromCircle(self.__other_bot.getPosition(), self.__other_bot.getRayon(), POINTS_PAR_CERCLE)
			#maj navgraph
			self.__ng.pop_dynamic_obstable()
			self.__ng.add_dynamic_obstacle(self.__our_bot_poly)

	def __update_enemy_bot(self):
		if NUMBER_OF_ENEMY >= 1:
			self.__enemy_bot_poly.move_to(self.__big_enemy_bot.getPosition())
		if NUMBER_OF_ENEMY >= 2:
			self.__enemy_bot_poly.move_to(self.__small_enemy_bot.getPosition())

	def __init_enemy_bot(self):
		self.__enemy_bot_poly = []
		if NUMBER_OF_ENEMY >= 1:
			self.__enemy_bot_poly.append(Poly().initFromCircle((0,0), RAYON_BIG_ENEMY, POINTS_PAR_CERCLE))
		if NUMBER_OF_ENEMY >= 2:
			self.__enemy_bot_poly.append(Poly().initFromCircle((0,0), RAYON_SMALL_ENEMY, POINTS_PAR_CERCLE))
		#on lui ajoute les robots
		for i in range(NUMBER_OF_ENEMY):
			self.__ng.add_dynamic_obstacle(self.__enemy_bot_poly[i])
		self.__update_enemy_bot()

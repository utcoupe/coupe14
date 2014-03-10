# -*- coding: utf-8 -*-
from .pathfinding2012 import *
from constantes import *
from geometry import *
import logging
import time

class PathFinding:
	def __init__(self, robot_list, xml_filename, MARGE_PASSAGE=MARGE_PASSAGE):
		self.__log = logging.getLogger(__name__)
		flussmittel, tibot, big_enemy, small_enemy = robot_list
		self.__flussmittel = flussmittel
		self.__tibot = tibot
		self.__big_enemy_bot = big_enemy
		self.__small_enemy_bot = small_enemy
		#on cree le navgraph
		self.__ng = nav.NavGraph(MARGE_PASSAGE, xml_filename)
		self.__init_enemy_bot()
		#on compte nos robots
		self.__our_bot_count = 0
		if flussmittel is not None:
			self.__our_bot_count += 1
		if tibot is not None:
			self.__our_bot_count += 1
		self.__log.info(str(self.__our_bot_count) + " robots amis actifs")
		self.__number_of_enemy = 0
		if big_enemy is not None:
			self.__number_of_enemy += 1
		if small_enemy is not None:
			self.__number_of_enemy += 1
		self.__log.info(str(self.__number_of_enemy) + " robots ennemis actifs")
		#on met a jour tout les robots

		if flussmittel is not None:
			self.__our_bot = self.__flussmittel
			self.__other_bot = self.__tibot
		elif tibot is not None:
			self.__our_bot = self.__tibot
			self.__other_bot = self.__flussmittel
		else:
			self.__log.error("Aucun robot ami actif !")
			raise Exception("Aucun robot actif")
		self.__other_bot_poly = Poly().initFromCircle(self.__other_bot.getPosition(), self.__other_bot.getRayon(), POINTS_PAR_CERCLE)
		self.update(self.__our_bot)

	def update(self, robot):
		start_time = time.time()
		self.__update_enemy_bot()
		if self.__our_bot_count == 2: #Si on a deux robots, il faut compte le deuxieme dans le pathfinding
			self.__update_our_bot(robot)
		self.__ng.update()
		self.__log.info("Mise à jour des polygones convexes en " + str((time.time() - start_time) * 1000) + "ms")

	def getPath(self, start, end):
		start_time = time.time()
		foo, bar, path = self.__ng.get_path(start, end)
		self.__log.info("Calcul de trajectoire en " + str((time.time() - start_time) * 1000) + "ms : " + str(path))
		return path

	def getPolygons(self):
		return self.__ng.get_polygons()

	def __update_our_bot(self, robot):
		"""Update le navgraph pour calculer une trajectoire pour le robot en paramètre"""
		if robot == self.__our_bot: #on met juste la position a jour
			self.__other_bot_poly.move_to(self.__other_bot.getPosition())
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
		if self.__small_enemy_bot is not None:
			self.__big_enemy_poly.move_to(self.__big_enemy_bot.getPosition())
		if self.__big_enemy_bot is not None:
			self.__small_enemy_poly.move_to(self.__small_enemy_bot.getPosition())

	def __init_enemy_bot(self):
		if self.__big_enemy_bot is not None:
			self.__big_enemy_poly =Poly().initFromCircle((0,0), RAYON_BIG_ENEMY, POINTS_PAR_CERCLE)
			self.__ng.add_dynamic_obstacle(self.__big_enemy_poly)
		if self.__small_enemy_bot is not None:
			self.__small_enemy_poly = Poly().initFromCircle((0,0), RAYON_SMALL_ENEMY, POINTS_PAR_CERCLE)
			self.__ng.add_dynamic_obstacle(self.__small_enemy_poly)
		self.__update_enemy_bot()

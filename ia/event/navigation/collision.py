# -*- coding: utf-8 -*-
import logging
import math

from .constantes import *
from geometry import Segment


class Collison:
	def __init__(self, robot_list):
		self.__log = logging.getLogger(__name__)
		self.__flussmittel, self.__tibot, self.__big_enemy_bot, self.__small_enemy_bot = robot_list

	def getCollision(self, robot):
		#on etablit la liste des robots autres que celui pour lequel on calcule la trajectoire
		robot_list = [self.__big_enemy_bot, self.__small_enemy_bot]
		if robot is self.__flussmittel:
			robot_list.insert(0, self.__tibot)
			self.__log.info("Calcul de collision pour Flussmittel")
		elif robot is self.__tibot:
			robot_list.insert(0, self.__flussmittel)
			self.__log.info("Calcul de collision pour Tibot")
		else:
			self.__log.error("Le robot spécifié n'est ni Flussmittel ni Tibot")
			return None

		""" .getTrajectoires() - > (dataObjectif, ...)
			dataObjectif -> (id, (point, ...))
			point - > (x, y) """
		trajectoires = robot.getTrajectoires()
		collisions = []

		for data_obj in trajectoires:  # pour chaque trajectoire
			id = data_obj[0]
			traj = data_obj[1]
			checked_traj = [traj[0]]  # cela correspond a la trajectoire parcourue sans collision

			for a, b in zip(traj[:-1], traj[1:]):  # on parcours chaque segment de trajectoire
				for robot_el in robot_list:  # on regarde si l'un des robot est sur ce segment

					#pour la collision, on tracer un cercle de rayon (obstacle + rayon du robot) pour tenir compte de la taille des robots
					collision_pts = self.__circle_inter_seg(robot_el.getPosition(), robot_el.getRayon() + robot.getRayon(), a, b)  # s'il y a intersection
					if collision_pts:  # s'il y a intersection
						checked_traj.append(self.__get_closest(checked_traj[-1], collision_pts))  # on ajoute le premier pt d'intersection
						distance_to_collision = self.__traj_length(checked_traj)  # on calcule la longueur restante avant collsion
						collisions.append((id, distance_to_collision))
						return (id, distance_to_collision)
				checked_traj.append(b)  # on ajoute le point de depart a la trejctoire verifiee

	def __circle_inter_seg(self, center, radius, pta, ptb):
		"""return true if segment AB from points given as arguments crosses the circle given as argument defines from Poly"""
		#y=mx+c
		m = (ptb[1] - pta[1]) / (ptb[0] - pta[0])  # a coef
		c = ptb[1] - m * ptb[0]  # b coef
		# (x−p)2+(y−q)2=r2
		p = center[0]
		q = center[1]
		r = radius
		#ax² + bx + x = 0
		a = m ** 2 + 1
		b = 2 * (m * c - m * q - p)
		c = q ** 2 - r ** 2 + p ** 2 - 2 * c * q + c ** 2
		#delta = b² - 4ac
		delta = b ** 2 - 4 * a * c

		if delta < 0:
			return ()
		else:
			x1 = (-b + math.sqrt(delta)) / (2 * a)
			x2 = (-b - math.sqrt(delta)) / (2 * a)
			y1 = m * x1 + c
			y2 = m * x2 + c
			return ((x1, y1), (x2, y2))

	def __get_closest(self, p1, list_of_pt):
		closest = list_of_pt[0]
		closest_dist = Segment(p1, list_of_pt[0]).norm2()
		for pt in list_of_pt:
			dist = Segment(p1, pt).norm2()
			if dist < closest_dist:
				closest_dist = dist
				closest = pt
		return closest

	def __traj_length(self, traj):
		length = 0
		for a, b in zip(traj[:-1], traj[1:]):
			length += math.sqrt(Segment(a, b).norm2())
		return length

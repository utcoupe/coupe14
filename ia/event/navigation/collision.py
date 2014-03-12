# -*- coding: utf-8 -*-
import logging
import math

from .constantes import *
from geometry import Segment


class Collision:
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

		for data_obj in trajectoires:  # pour chaque trajectoire
			id = data_obj[0]
			traj = data_obj[1]
			checked_traj = [traj[0]]  # cela correspond a la trajectoire parcourue sans collision

			for a, b in zip(traj[:-1], traj[1:]):  # on parcours chaque segment de trajectoire
				for robot_el in robot_list:  # on regarde si l'un des robot est sur ce segment

					#pour la collision, on trace un cercle de rayon (obstacle + rayon du robot) pour tenir compte de la taille des robots
					collision_pts_on_line = self.__circle_inter_line(robot_el.getPosition(), robot_el.getRayon() + robot.getRayon(), a, b)  # s'il y a intersection
					collision_pts = self.__p_in_seg((a, b), collision_pts_on_line)  # on se restreint aux points sur le segment 
					if collision_pts:  # s'il y a intersection
						# cas particulier : 1er segment de trajectoire
						if len(checked_traj) == 1 and self.__p_in_circle(robot_el.getPosition(), robot_el.getRayon() + robot.getRayon(), a):
							distance_to_collision = 0
							return (id, distance_to_collision)

						checked_traj.append(self.__get_closest(checked_traj[-1], collision_pts))  # on ajoute le premier pt d'intersection
						distance_to_collision = self.__traj_length(checked_traj)  # on calcule la longueur restante avant collsion

						print("col : %dmm, robot :%s" % (distance_to_collision, robot_el))
						self.__log.info("Collision sur l'id %s a %s mm" % (id, distance_to_collision))
						return (id, distance_to_collision)
				checked_traj.append(b)  # on ajoute le point de depart a la trajctoire verifiee
		return None

	def __circle_inter_line(self, center, radius, pta, ptb):
		"""return true if segment AB from points given as arguments crosses the circle given as argument defines from Poly"""
		#y=mx+n
		p = center[0]
		q = center[1]
		r = radius
		ret = []
		try:
			m = (ptb[1] - pta[1]) / (ptb[0] - pta[0])  # a coef
			n = ptb[1] - m * ptb[0]  # b coef
			# (x−p)2+(y−q)2=r2
			#ax² + bx + x = 0
			a = m ** 2 + 1
			b = 2 * (m * n - m * q - p)
			c = q ** 2 - r ** 2 + p ** 2 - 2 * n * q + n ** 2
			#delta = b² - 4ac
			delta = b ** 2 - 4 * a * c

			if delta < 0:
				return ret
			else:
				x1 = (-b + math.sqrt(delta)) / (2 * a)
				x2 = (-b - math.sqrt(delta)) / (2 * a)
				y1 = m * x1 + n
				y2 = m * x2 + n

				ret = ((x1, y1), (x2, y2))
		except ZeroDivisionError:  # le segment est vertical
			x = pta[0]
			delta = r ** 2 - (x - p) ** 2
			y1 = q + delta
			y2 = q - delta
			if delta < 0:
				return ret
			else:
				ret = ((x, y1), (x, y2))
		return ret

	def __p_in_seg(self, seg, list_of_p):
		"""savoir si un point aligné avec un segment est dans lesegment ou en dehors"""
		ret = []
		a = seg[0]
		b = seg[1]
		for p in list_of_p:
			if min(a[0], b[0]) <= p[0] <= max(a[0], b[0]):
				if min(a[1], b[1]) <= p[1] <= max(a[1], b[1]):
					ret.append(p)
		return ret

	def __p_in_circle(self, center, radius, p):
			# (x−p)2+(y−q)2<r2
			if (p[0] - center[0]) ** 2 + (p[1] - center[1]) ** 2 < radius ** 2:
				return True
			else:
				return False

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

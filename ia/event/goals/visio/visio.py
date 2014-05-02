# -*- coding: utf-8 -*-
import logging
from subprocess import Popen, PIPE
import time
import atexit
from math import cos, sin


"""TODO : Post-traitement des positions des triangles pour corriger
la position des triangles en hauteur"""


class Triangle:
	"""Simple structure de stockage des infos triangles"""
	def __init__(self, coord, angle, size, color, isDown, abs_to_rel_angle):
		self.coord = [int(float(x)) for x in coord.split(':')]
		self.angle = float(angle)
		self.size = float(size)
		self.color = ''
		color = int(color)
		if color == 0:
			self.color = 'RED'
		elif color == 1:
			self.color = 'YELLOW'
		elif color == 2:
			self.color = 'BLACK'
		self.isDown = bool(isDown)

	def __repr__(self):
		if self.isDown:
			state = 'down'
		else:
			state = 'up'
		return str(self.coord) + '\ta=' + str(self.angle) + '\t' + str(self.size) + '\t' + self.color + '\t' + state


class Visio:
	def __init__(self, path_exec, index=0, path_config='./', big_bot=None, capture_vid=True):
		#Parameters
		self.__updatePeriod = 0.001  # période d'attente entre deux demandes au client
		self.__retry_count = 0
		self.__hplat = 30  # hauteur des plateformes
		self.__hcam = 300  # hauteur de la cam au sol
		self.__xcam = 190  # distance entre cam et milieu robot
		self.__ycam = 35  # devrait etre 0

		self.__log = logging.getLogger(__name__)
		self.path_exec = './' + path_exec
		self.__big_bot = big_bot

		if capture_vid:
			capture_vid = 'true'

		#Lancement du client
		self.__log.info("Executing C++ program")
		self.client = Popen([self.path_exec, str(index), 'com', path_config, capture_vid], stdin=PIPE, universal_newlines=True, stdout=PIPE)
		atexit.register(self.client.kill)
		stdout = ''
		while stdout != 'READY\n':
			#Attente des données client
			stdout = self.client.stdout.readline()
			#Sleep 1ms
			time.sleep(self.__updatePeriod)
		self.__log.info("Visio ready")

		self._triangles = []

	def getTriangles(self):
		return self._triangles

	def update(self):
		"""Demande au client de mettre à jour les triangles,
		puis renvoit les nouvelles données"""
		self.client.stdin.write('ASK_DATA\n')
		data = ''

		# On lit jusqu'à la fin de la tramme de retour
		while data[-4:] != 'END\n':
			#Attente des données client
			stdout = self.client.stdout.readline()
			data += stdout
			#Sleep 1ms
			time.sleep(self.__updatePeriod)

		# On supprime le END
		data = data[:-4]
		if data == "ERROR\n":
			if self.__retry_count < 3:
				self.__retry_count += 1
				self.__log.error("Erreur du CPP, retry : " + str(self.__retry_count))
				self.update()
			else:
				self.__log.error("Erreur du CPP, cancel")
				self._triangles = []
		else:
			# Maj des triangles
			self.__updateTriFromStr(data)
			self.__retry_count = 0
		return self._triangles

	def __updateTriFromStr(self, data):
		self._triangles.clear()
		try:
			triangles = data.split('\n')
			#Pour chaque triangle
			for triangle in triangles[:-1]:
				attr = triangle.split(' ')
				tri = Triangle(*attr)
				self._triangles.append(tri)
			self.__log.info("Received data from C++ : " + str(self._triangles))
		except:
			self.__log.error("Error parsing string from C++ : " + str(data))

		# En situation de test, big bot est None
		triangles = self._triangles
		try:
			if self.__big_bot is not None:
				self.__post_processing()
		except:
			self._triangles = triangles  # si echec, on ne corrige pas

	def __post_processing(self):
		if self.__big_bot is None:
			return

		for i in range(len(self._triangles)):
			tri = self._triangles[i]

			#calcul des coordonnées relatives dans le repère des coords absolues
			robot_angle = self.__big_bot.getPositionAndAngle()[2]
			tri.rel_in_abs = (tri.coords[0] * cos(robot_angle) - tri.coords[1] * sin(robot_angle), 
								tri.coords[0] * sin(robot_angle) + tri.coords[1] * cos(robot_angle))

			#calcul des coordonnées réelles du triangles, on le recalcule par la
			# suite si elles sont a modifier, mais on en a besoin pour savoir
			# s'i faut les modifier
			tri.real_coords = [i + j for i, j in zip(tri.rel_in_abs, self.__big_bot.getPosition())]

			#Traitement de la position pour modif si triangle en hauteur
			self.__highGroundProcess(tri)

	def __highGroundProcess(self, tri):
		"""Corrige les coordonnées des triangles en hauteurs à des positions connues
		exemple : triangle sur une plateforme de depot"""
		if self.__inHighGround(tri):
			#backup
			#modif coords
			tri.coords[0] = (1 - self.__hcam / self.__hplat) * tri.coords[0] \
								+ (self.__hcam / self.__hplat) * self.__xcam
			tri.coords[1] = (1 - self.__hcam / self.__hplat) * tri.coords[1] \
								+ (self.__hcam / self.__hplat) * self.__ycam
			#reconversion en coords reelles
			tri.real_coords = [i + j for i, j in zip(tri.rel_in_abs, self.__big_bot.getPosition())]

	def __inHighGround(self, tri):
		#plateformes
		if self.__p_in_circle((0, 0), 250, tri.real_coords) \
		or self.__p_in_circle((3000, 0), 250, tri.real_coords) \
		or self.__p_in_circle((1500, 950), 150, tri.real_coords):
			return True
		else:
			return False

	def __p_in_circle(self, center, radius, p):
			# (x−p)2+(y−q)2<r2
			if (p[0] - center[0]) ** 2 + (p[1] - center[1]) ** 2 < radius ** 2:
				return True
			else:
				return False

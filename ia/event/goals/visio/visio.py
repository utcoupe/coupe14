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
	def __init__(self, x, y, angle, size, color, isDown):
		self.coord = [float(x), float(y)]
		self.angle = float(angle)
		self.size = float(size)
		self.color = ''
		self.real_coord = [0, 0]
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

	def rel_in_abs(self, robot_angle):
		return (tri.coord[0] * cos(robot_angle) - tri.coord[1] * sin(robot_angle), 
				tri.coord[0] * sin(robot_angle) + tri.coord[1] * cos(robot_angle))

	def dist2(self, tri):
		dx = self.coord[0] - tri.coord[0]
		dy = self.coord[1] - tri.coord[1]
		return dx*dx + dy*dy


class Visio:
	def __init__(self, path_exec, index=0, path_config='./', big_bot=None, capture_vid=True):
		#Parameters
		self.__updatePeriod = 0.001  # période d'attente entre deux demandes au client
		self.__retry_count = 0
		self.__htri = 30
		self.__hplat = 30  # hauteur des plateformes
		self.__htorch = 126
		self.__hcam = 300  # hauteur de la cam au sol
		self.__xcam = 190  # distance entre cam et milieu robot
		self.__ycam = 0  # devrait etre 0

		self.__log = logging.getLogger(__name__)
		self.path_exec = './' + path_exec
		self.__big_bot = big_bot

		if capture_vid:
			capture_vid = 'true'
		else:
			capture_vid = 'false'

		#Lancement du client
		self.__log.info("Executing C++ program")
		self.client = Popen([self.path_exec, str(index), 'com', path_config, capture_vid], stdin=PIPE, universal_newlines=True, stdout=PIPE)
		self.__log.info("C++ Program executed, waiting till program is ready")
		atexit.register(self.client.kill)
		stdout = ''
		while stdout != 'READY\n' and stdout != 'FAILED\n':
			print(stdout, end='')
			#Attente des données client
			stdout = self.client.stdout.readline()
			#Sleep 1ms
			time.sleep(self.__updatePeriod)

		if stdout == 'FAILED\n':
			raise Exception('Visio failed')
			return

		self.__log.info("Visio ready")

		self._triangles = []

	def close(self):
		self.client.kill()
		self.client.wait()

	def getTriangles(self):
		return self._triangles

	def update(self, isTorch=False):
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
			self.__updateTriFromStr(data, isTorch)
			self.__retry_count = 0
		return self._triangles

	def __updateTriFromStr(self, data, isTorch=False):
		self._triangles = []
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
		if isTorch:
			try:
				for i in range(len(self._triangles)):
					tri = self._triangles[i]
					self.__highGroundProcess(tri, self.__htorch)
			except BaseException as e:
				self.__log.error("Failed to post-process datas (torches) : "+str(e))
				self._triangles = triangles  # si echec, on ne corrige pas

		triangles = self._triangles
		try:
			if self.__big_bot is not None:
				self.__post_processing()
		except BaseException as e:
			self.__log.error("Failed to post-process datas (generic) : "+str(e))
			self._triangles = triangles  # si echec, on ne corrige pas

	def __post_processing(self):
		if self.__big_bot is None:
			return

		for i in range(len(self._triangles)):
			tri = self._triangles[i]

			#calcul des coordonnées relatives dans le repère des coords absolues
			robot_angle = self.__big_bot["getPositionAndAngle"][2]

			#calcul des coordonnées réelles du triangles, on le recalcule par la
			# suite si elles sont a modifier, mais on en a besoin pour savoir
			# s'i faut les modifier
			tri.real_coords = [i + j for i, j in zip(tri.rel_in_abs(robot_angle), self.__big_bot["getPosition"])]

			#Traitement de la position pour modif si triangle en hauteur
			if self.__outOfMap(tri) or self.__inFruitZone(tri) or self.__inStartZone(tri):
				self._triangles.remove(tri)

			#elif self.__inHighGround(tri):
			#	self.__highGroundProcess(tri, self.__hplat)

	def __highGroundProcess(self, tri, hobj):
		"""Corrige les coordonnées des triangles en hauteurs à des positions connues
		exemple : triangle sur une plateforme de depot"""
		ho = hobj - self.__htri
		hcam = self.__hcam - self.__htri
		x = tri.coord[0] - self.__xcam
		y = tri.coord[1] - self.__ycam
		dx = x * (ho / hcam)
		dy = y * (ho / hcam)
		#modif coords
		tri.coord[0] -= dx
		tri.coord[1] -= dy
		#reconversion en coords reelles
		robot_angle = self.__big_bot["getPositionAndAngle"][2]
		tri.real_coords = [i + j for i, j in zip(tri.rel_in_abs(robot_angle), self.__big_bot["getPosition"])]

	def __outOfMap(self, tri):
		return tri.real_coords[0] > 3000 or tri.real_coords[0] < 0\
		or tri.real_coord[1] > 2000 or tri.real_coord[1] < 0

	def __inFruitZone(self, tri):
		return (tri.real_coords[0] > 400 and tri.real_coords[0] < 1100 and tri.real_coord[1] > 1700)\
		or (tri.real_coords[0] > 1900 and tri.real_coords[0] < 2600 and tri.real_coord[1] > 1700)


	def __inHighGround(self, tri):
		#plateformes
		return self.__p_in_circle((0, 0), 250, tri.real_coords) \
		or self.__p_in_circle((3000, 0), 250, tri.real_coords) \
		or self.__p_in_circle((1500, 950), 150, tri.real_coords)

	def __inStartZone(self, tri):
		return (tri.real_coords[0] < 400 and tri.real_coord[1] > 1700) or (tri.real_coords[0] > 2600 and tri.real_coord[1] > 1700) \
		or self.__p_in_circle((0,1700), 400, tri.real_coords) or self.__p_in_circle((3000, 1700), 400, tri.real_coords)

	def __p_in_circle(self, center, radius, p):
			# (x−p)2+(y−q)2<r2
			return (p[0] - center[0]) ** 2 + (p[1] - center[1]) ** 2 < radius ** 2

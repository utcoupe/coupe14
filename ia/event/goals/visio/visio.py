# -*- coding: utf-8 -*-
import logging
from subprocess import Popen, PIPE
import time
import atexit
import os
from math import cos, sin

from constantes import *

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
		return (self.coord[0] * cos(robot_angle) - self.coord[1] * sin(robot_angle), 
				self.coord[0] * sin(robot_angle) + self.coord[1] * cos(robot_angle))

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

		logging.basicConfig(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.log"), filemode='w', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		self.__log = logging.getLogger(__name__)
		self.path_exec = './' + path_exec
		self.__big_bot = big_bot

		if capture_vid:
			capture_vid = 'true'
		else:
			capture_vid = 'false'

		#Lancement du client
		self.__log.info("Executing C++ program at " + str(self.path_exec))
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

		print(data)

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
		self.__log.info("Got "+str(len(triangles))+" triangles, coords :")
		for tri in triangles:
			self.__log.info(tri)

		triangles = self._triangles
		try:
			if self.__big_bot is not None:
				self.__post_processing(isTorch)
		except BaseException as e:
			self.__log.error("Failed to post-process datas : "+str(e))
			if isTorch:
				self._triangles = []
			else:
				self._triangles = triangles  # si echec, on ne corrige pas

		self.__log.info("After post-process :")
		for tri in self._triangles:
			self.__log.info(tri)

	def __post_processing(self, isTorch=False):
		if self.__big_bot is None:
			return

		tri_to_remove = []

		for i in range(len(self._triangles)):
			if isTorch:
				self.__highGroundProcess(self._triangles[i], self.__htorch)
				if self._triangles[i].size < MIN_SIZE_TRIANGLE_TORCH:
					tri_to_remove.append(self._triangles[i])
				elif self._triangles[i].size > MAX_SIZE_TRIANGLE_TORCH:
					tri_to_remove.append(self._triangles[i])
			else:
				if self._triangles[i].size > MAX_SIZE_TRIANGLE:
					tri_to_remove.append(self._triangles[i])


			#calcul des coordonnées relatives dans le repère des coords absolues
			robot_angle = self.__big_bot["getPositionAndAngle"][2]

			#calcul des coordonnées réelles du self._triangles[i]angles, on le recalcule par la
			# suite si elles sont a modifier, mais on en a besoin pour savoir
			# s'i faut les modifier
			self._triangles[i].real_coords = [i + j for i, j in zip(self._triangles[i].rel_in_abs(robot_angle), self.__big_bot["getPosition"])]

			#Traitement de la position pour modif si self._triangles[i]angle en hauteur
			if self._triangles[i].coord[0] < MIN_X_TRIANGLE:
				tri_to_remove.append(self._triangles[i])
			elif self._triangles[i].coord[0] > MAX_X_TRIANGLE:
				tri_to_remove.append(self._triangles[i])
			elif self._triangles[i].coord[1] < MIN_Y_TRIANGLE:
				tri_to_remove.append(self._triangles[i])
			elif self._triangles[i].coord[1] > MAX_Y_TRIANGLE:
				tri_to_remove.append(self._triangles[i])
			elif self.__outOfMap(self._triangles[i]) or self.__inFruitZone(self._triangles[i]) or self.__inStartZone(self._triangles[i]):
				self.__log.info("Remove triangle in invalid zone")
				tri_to_remove.append(self._triangles[i])
			#elif self.__inHighGround(self._triangles[i]):
			#	self.__highGroundProcess(self._triangles[i], self.__hplat)

		for j in range(len(tri_to_remove)):
			self._triangles.remove(tri_to_remove[j])


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
		if tri.real_coords[0] > 3000 or tri.real_coords[0] < 0\
				or tri.real_coord[1] > 2000 or tri.real_coord[1] < 0:
			return True
		else:
			return False

	def __inFruitZone(self, tri):
		if (tri.real_coords[0] > 400 and tri.real_coords[0] < 1100 and tri.real_coord[1] > 1700)\
				or (tri.real_coords[0] > 1900 and tri.real_coords[0] < 2600 and tri.real_coord[1] > 1700):
			return True
		else:
			return False


	def __inHighGround(self, tri):
		#plateformes
		if self.__p_in_circle((0, 0), 250, tri.real_coords) \
		or self.__p_in_circle((3000, 0), 250, tri.real_coords) \
		or self.__p_in_circle((1500, 950), 150, tri.real_coords):
			return True
		else:
			return False

	def __inStartZone(self, tri):
		if (tri.real_coords[0] < 400 and tri.real_coord[1] > 1700) or (tri.real_coords[0] > 2600 and tri.real_coord[1] > 1700) \
				or self.__p_in_circle((0,1700), 400, tri.real_coords) or self.__p_in_circle((3000, 1700), 400, tri.real_coords):
			return True
		else:
			return False

	def __p_in_circle(self, center, radius, p):
			# (x−p)2+(y−q)2<r2
			return (p[0] - center[0]) ** 2 + (p[1] - center[1]) ** 2 < radius ** 2

# -*- coding: utf-8 -*-
import logging
from subprocess import Popen, PIPE
import time
import atexit


"""TODO : Post-traitement des positions des triangles pour corriger
la position des triangles en hauteur"""


class Triangle:
	"""Simple structure de stockage des infos triangles"""
	def __init__(self, coord, angle, color, isDown):
		self.coord = [int(float(x)) for x in coord.split(':')]
		self.angle = float(angle)
		self.color = ''
		color = int(color)
		if color == 0:
			self.color = 'RED'
		elif color == 1:
			self.color = 'YELLOW'
		elif color == 2:
			self.color = 'BLACK'
		self.isDown = bool(isDown)
		self.real_coords = (-1, -1)

	def __repr__(self):
		if self.isDown:
			state = ' down '
		else:
			state = ' up '
		return str(self.coord) + ' : a=' + str(self.angle) + ' - ' + self.color + state


class Visio:
	def __init__(self, path_exec, index=0, big_bot=None):
		#Parameters
		self.__updatePeriod = 0.001  # période d'attente entre deux demandes au client
		self.__offset_coords = (0, 0)  # changement de repère
		self.__retry_count = 0

		self.__log = logging.getLogger(__name__)
		self.path_exec = './' + path_exec
		self.__big_bot = big_bot

		#Lancement du client
		self.__log.info("Executing C++ program")
		self.client = Popen([self.path_exec, str(index)], stdin=PIPE, universal_newlines=True, stdout=PIPE)
		atexit.register(self.client.kill)
		stdout = ''
		time.sleep(1)
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
		triangles = data.split('\n')
		self._triangles.clear()
		#Pour chaque triangle
		for triangle in triangles[:-1]:
			attr = triangle.split(' ')
			tri = Triangle(*attr)
			self._triangles.append(tri)
		self.__log.info("Received data from C++ : " + str(self._triangles))

		if self.__big_bot is not None:
			self.__post_processing()

	def __post_processing(self):
		if self.__big_bot is None:
			return

		for i in range(len(self._triangles)):
			tri = self._triangles[i]
			#calcul des coordonnées des triangles detectées sur la carte
			tri.real_coords = tri.coords + self.__big_bot.getPosition()
			#transformation des coords envoyées par le C++ en coords relatives au bras
			tri.coords += self.__offset_coords

			#Traitement de la position pour modif si triangle en hauteur
			self.__highGroundProcess(tri)

	def __highGroundProcess(self, tri):
		"""Corrige les coordonnées des triangles en hauteurs à des positions connues
		exemple : triangle sur une plateforme de depot"""
		pass

# -*- coding: utf-8 -*-
import logging
from subprocess import Popen, PIPE
import time


"""TODO : Post-traitement des positions des triangles pour corriger
la position des triangles en hauteur"""


class Triangle:
	"""Simple structure de stockage des infos triangles"""
	def __init__(self, coord, angle, color, isDown):
		self.coord = [int(x) for x in coord.split(':')]
		self.angle = float(angle)
		self.color = str(color)
		self.isDown = bool(isDown)
		self.real_coords = (-1,-1)


class Visio:
	def __init__(self, path_exec, big_bot=None):
		#Parameters
		self.__updatePeriod = 0.001  # période d'attente entre deux demandes au client
		self.__offset_coords = (0, 0)  # changement de repère

		self.__log = logging.getLogger(__name__)
		self.path_exec = './' + path_exec
		self.__big_bot = big_bot

		#Lancement du client
		self.client = Popen(self.path_exec, stdin=PIPE, stdout=PIPE)

		self._triangles = []

	def getTriangles(self):
		return self._triangles

	def update(self):
		"""Demande au client de mettre à jour les triangles,
		puis renvoit les nouvelles données"""
		self.client.communicate('ASK_DATA')
		stdout = ''
		data = ''

		# On lit jusqu'à la fin de la tramme de retour
		while stdout != 'END\n':
			#Attente des données client
			stdout, stderr = self.client.communicate()
			data += stdout
			if stderr != '':  # Erreurs clients
				self.__log.warning('Erreurs C++ visio : ' + stderr)
				raise Exception(stderr)
			#Sleep 1ms
			time.sleep(self.__updatePeriod)

		# On supprime le END
		data = data[-4:]
		# Maj des triangles
		self.__updateTriFromStr(data)
		return self._triangles

	def __updateTriFromStr(self, data):
		triangles = data.split('\n')
		self._triangles.clear()
		#Pour chaque triangle
		for triangle in triangles:
			attr = triangles.split(' ')
			tri = Triangle(*attr)
			self._triangles.append(tri)

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

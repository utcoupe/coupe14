# -*- coding: utf-8 -*-

__author__ = 'furmi'

import time
import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "engine"))

class Hokuyo:
	"""
	Emule le comportement de l'hokuyo.
	Permet de répondre aux ordres envoyés à travers le protocole.
	"""
	def __init__(self, robots):
		self.__robots = robots
		#return le nombre de millisecondes depuis le temps d'origine
		self.__get_milli = lambda: int(round(time.time() * 1000))
		self.__last_time_stamp = self.__get_milli()

	def ping(self):
		return 'pong'

	def adresse (self):
		return 6

	def start(self):
		"""
		Set du premier timestamp quand le match a démarré
		"""
		self.__last_time_stamp = self.__get_milli()

	def getHokuyo(self):
		"""
		Renvoie la position de tous les robots
		@return int le temps depuis le lancement de l'hokuyo en millisecondes
		@return int position x de notre gros robot
		@return int position y de notre gros robot
		@return int position x de notre petit robot
		@return int position y de notre petit robot
		@return int position x du gros robot ennemi
		@return int position y du gros robot ennemi
		@return int position x du petit robot ennemi
		@return int position y du petit robot ennemi
		"""
		taille =len(self.__robots)

		ret = list()
		void_ret = list()
		ret.append(self.__get_milli()-self.__last_time_stamp)

		for i in range(taille):
			if self.__robots[i] is not None:
				ret.append(self.__robots[i].getXreal())
				ret.append(self.__robots[i].getYreal())
			else:
				void_ret.append(-1)
				void_ret.append(-1)

		ret.extend(void_ret)
		return ret

	def __getTimeStamp(self):
		current_time = self.__get_milli()
		diff_time = current_time - self.__last_time_stamp
		self.__last_time_stamp = current_time
		return diff_time
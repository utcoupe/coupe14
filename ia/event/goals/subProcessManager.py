# -*- coding: utf-8 -*-
"""
Cette classe permet de gèrer le sub-process en charge du choix d'objectif
"""

from xml.dom.minidom import parseString
import logging
from collections import deque
import time

from .goalsManager import *

class SubProcessManager():
	def __init__(self, connection, robot_name):
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__connection = connection
		self.__robot_name = robot_name

		self.__data = {}

		self.__GoalsManager = GoalsManager(self, connection, robot_name)

	def sendGoal(self, id_objectif_prev, id_objectif, elem_script):
		self.__connection.send((self.__robot_name, id_objectif_prev, id_objectif, elem_script))

	def getData(self):
		return self.__data

	def readPipe(self):
		while True:
			new_message = self.__connection.recv()
			if new_message[0] == "data":
				self.__updateData(new_message[1])
			else:
				self.__processStatus(new_message)

	def __updateData(self, data):
		self.__data = data

	def __processStatus(self, status):
		"""read new status and update objectif_list"""
		etat = status[0]
		id_objectif = status[1]

		if etat == "over":
			self.__GoalsManager.goalFinishedId(id_objectif)
		elif etat == "canceled":
			self.__GoalsManager.goalCanceledId(id_objectif)


def startSubprocess(connection, robot_name):
	a = SubProcessManager(connection, robot_name)
	a.readPipe()
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
		
		self.__connection = connection
		self.__robot_name = robot_name

		self.__logger = logging.getLogger(__name__.split('.')[0])

		self.__data = {}
		while self.__data == {}:
			self.readPipe(loop=False) #Normalement on ne peut pas recevoir over ni canaceled à ce stade
		
		self.__GoalsManager = GoalsManager(self, connection, robot_name)

	def sendGoal(self, id_objectif_prev, id_objectif, elem_script):
		self.__connection.send(("add", (self.__robot_name, id_objectif_prev, id_objectif, elem_script)))

	def sendDeleteGoal(self, id_objectif):
		self.__connection.send(("delete", self.__robot_name, id_objectif))

	def getData(self):
		return self.__data

	def readPipe(self, loop):
		if loop:
			while True:
				new_message = self.__connection.recv()
				if new_message[0] == "data":
					self.__updateData(new_message[1])
				else:
					self.__processStatus(new_message)
		else:
			new_message = self.__connection.recv()
			if new_message[0] == "data":
				self.__updateData(new_message[1])
			else:
				self.__processStatus(new_message)

	def __updateData(self, data):
		if self.__data == {}:
			self.__data = data
		else:
			for robot_name in data:
				for info_name in data[robot_name]:
					self.__data[robot_name][info_name] = data[robot_name][info_name]

	def __processStatus(self, status):
		"""read new status and update objectif_list"""
		etat = status[0]
		id_objectif = status[1]

		if etat == "STEP_OVER":
			self.__GoalsManager.goalStepOverId(id_objectif)
		elif etat == "DYNAMIQUE_OVER":
			self.__GoalsManager.goalDynamiqueFinishedId(id_objectif)
		elif etat == "BRAS_STATUS":
			if self.__robot_name == "FLUSSMITTEL":
				self.__GoalsManager.processBrasStatus(status[1], status[2])
		elif etat == "END":
			self.__GoalsManager.goalFinishedId(id_objectif)
		elif etat == "CANCELED":
			self.__GoalsManager.goalCanceledId(id_objectif)
		else:
			self.__logger.error("Status non géré status "+str(status))

def startSubprocess(connection, robot_name):
	a = SubProcessManager(connection, robot_name)
	a.readPipe(loop=True)
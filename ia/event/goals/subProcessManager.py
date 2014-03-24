# -*- coding: utf-8 -*-
"""
Cette classe permet de gèrer le sub-process en charge du choix d'objectif
"""

from xml.dom.minidom import parseString
import logging
from collections import deque
import time

from .goalsManager import *

class subProcessManager():
	def __init__(self, connection, robot_name):
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__connection = connection
		self.__robot_name = robot_name
		if self.__robot_name == 'FLUSSMITTEL':
			self.__script_filename = "data/script_flussmittel.xml"
		elif self.__robot_name == 'TIBOT':
			self.__script_filename = "data/script_tibot.xml"
		else:
			self.__logger.error("La variable robot_name n'a pas une valeur connu, self.__robot_name = " + str(self.__robot_name))

		self.__data = None
		self.__GoalsManager = GoalsManager(self.__robot_name)

		self.__processEvent()

	def __processEvent(self):
		self.__connection.send(self.__loadActionScript())
		while True:
			new_message = self.__connection.recv()
			if new_message[0] == "data":
				self.__updateData(new_message[1])
			else:
				self.__readStatus(new_message)

			#for i in range(10000000):
			#	pass
			#print(self.__robot_name)
			#TODO, si besoin retourner le dernier choix sinon relancer un choix
			
	def __loadActionScript(self):
		self.__logger.info("loading actionScript from: " + str(self.__script_filename))
		fd = open(self.__script_filename,'r')
		dom = parseString(fd.read())
		fd.close()

		objectif = deque()
		for xml_goal in dom.getElementsByTagName('objectif'):
			objectif_name	= xml_goal.attributes["objectif_name"].value #seulement pour information
			id_objectif		= int(xml_goal.getElementsByTagName('idd')[0].firstChild.nodeValue)

			data_objectif = deque()
			for xml_execution in xml_goal.getElementsByTagName('action'):
				ordre 		= (xml_execution.getElementsByTagName('ordre')[0].firstChild.nodeValue,)

				raw_arguments = xml_execution.getElementsByTagName('arguments')[0].firstChild
				if raw_arguments:
					arguments = (raw_arguments.nodeValue.split(','),)
				else:
					arguments = (None,)

				ordre += arguments
				data_objectif.append(ordre)

			objectif.append((self.__robot_name, 0, id_objectif, data_objectif))

		
		self.__logger.debug("Script chargé: " + str(objectif))
		return objectif

	def __updateData(self, data):
		self.__data = data

	def __readStatus(self, status):
		"""read new status and update objectif_list"""
		etat = status[0]
		id_objectif = status[1]

		if etat == "over":
			#TODO
			pass
		elif etat == "canceled":
			#TODO
			pass




def startSubprocess(connection, robot_name):
	a = subProcessManager(connection, robot_name)
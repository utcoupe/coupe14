# -*- coding: utf-8 -*-
"""
Cette classe permet de gèrer le sub-process en charge du choix d'objectif
"""

from xml.dom.minidom import parseString
import logging
from collections import deque
import time


#import goalsManager
#self.__GoalsManager = goalsManager.GoalsManager()

class subProcessManager():
	def __init__(self, connection):
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__connection = connection

		self.__processEvent()

	def __processEvent(self):
		script_loaded = False
		while True:
			time.sleep(0.1)
			if not script_loaded:
				script_loaded = True
				self.__connection.send(self.__loadActionScript())
			



	def __loadActionScript(self, filename="data/tibot.xml"):
		self.__logger.info("loading actionScript from: " + str(filename))
		fd = open(filename,'r')
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

			objectif.append(("TIBOT", 0, id_objectif, data_objectif))#TODO

		
		self.__logger.debug("Script chargé: " + str(objectif))
		return objectif

def startSubprocess(connection):
	a = subProcessManager(connection)
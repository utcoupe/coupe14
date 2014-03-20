# -*- coding: utf-8 -*-
"""
Cette classe permet de communiquer avec le subprocess de choix d'objectif
"""

from multiprocessing import Process, Pipe
import logging
from collections import deque
from xml.dom.minidom import parseString

from . import goals

class SubProcessCommunicate():
	def __init__(self):
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__parent_conn, self.__child_conn = Pipe()
		self.__process = Process(target=goals.processEvent, args=(self.__child_conn,))
		self.__process.start()
		self.__script_loaded = False

		
	def read(self):
		#print(self.__parent_conn.recv())
		if not self.__script_loaded:
			self.__script_loaded = True
			return self.__loadActionScript()
		else:
			return deque()

	def sendObjectifOver(self, id_objectif):
		pass

	def sendObjectifCanceled(self, id_objectifs_canceled):
		pass


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
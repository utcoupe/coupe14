# -*- coding: utf-8 -*-
"""
Classe pour nos robots
"""


from collections import deque
from xml.dom.minidom import parseString
from constantes import *
from math import sqrt
import logging

from .idRot import *

class OurBot():
	def __init__(self, name, communication, arduinoConstantes, addressOther, addressAsserv, largeur, longueur):
		#Constantes
		self.__name = name
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__communication = communication
		self.__addressOther = addressOther
		self.__addressAsserv = addressAsserv

		self.largeur = largeur 
		self.longueur = longueur


		#Valeurs récupérées (read-only)
		self.__positionX = 0
		self.__positionY = 0
		self.__angle = 0.0
		self.__last_id_executed_other = 29999
		self.__last_id_executed_asserv = 29999

		self.__last_id_stacked_action = IdRot()

		#Variables
		self.__objectifs = None #((id, ((id_action, ordre, arguments), (id_action, ordre, arguments), ...)), ...)

	#Getter
	def getPositon(self):
		return (self.positionX, self.positionY)

	def getName(self):
		return self.__name

	def getLastIdGlobale(self):
		return self.getMaxRot(self.__last_id_executed_other, self.__last_id_executed_asserv)

	def getAddressOther(self):
		return self.__addressOther

	def getAddressAsserv(self):
		return self.__addressAsserv


	def majLastId(self, address, idd):
		if address == 'ADDR_FLUSSMITTEL_OTHER' or address == 'ADDR_TIBOT_OTHER':
			if self.__last_id_executed_other != idd:
				self.__last_id_executed_other = idd
				print("changement d'id other " + str(idd))
		else:
			if self.__last_id_executed_asserv != idd:
				self.__last_id_executed_asserv = idd
				print("changement d'id asserv " + str(idd))

	#utilise les données en provenance de de l'asserv uniquement !
	def majPositionId(self, address, arguments):
		self.positionX = arguments[0]
		self.positionY = arguments[1]
		self.angle = arguments[2]
		self.majLastId(address, arguments[3])

	def getNextIdOrder(self):
		if self.__objectifs is not None:
			return (self.__objectifs[0][0], self.__objectifs[0][1][0]) #(id_objectif_0, id_action_0_de_objcetif_0)
		else:
			return None

	def getNextOrders(self):
		if self.__objectifs is not None:
			objectif_en_cours = self.__objectifs.popleft()
			order_of_objectif = objectif_en_cours[1] # type ((id_action, ordre, arguments),...)

			data_order = order_of_objectif.popleft() #type (id_action, ordre, arguments)
			output_temp = deque()
			output_temp.append(data_order)
			while data_order[1] != 'SLEEP' and data_order[1] != 'THEN' and data_order[1] != 'END':
				data_order = order_of_objectif.popleft()
				output_temp.append(data_order)

			if data_order[1] != 'END':
				self.__objectifs.appendleft(objectif_en_cours)

			return (objectif_en_cours[0], output_temp) # type ((id_action, ordre, arguments),...)

		else:
			return None

	def loadActionScript(self, filename):
		print(self.__name,": loading actionScript from:", filename)
		fd = open(filename,'r')
		dom = parseString(fd.read())
		fd.close()

		objectif = deque()
		for xml_goal in dom.getElementsByTagName('objectif'):
			objectif_name	= xml_goal.attributes["objectif_name"].value #seulement pour information
			idd				= xml_goal.getElementsByTagName('idd')[0].firstChild.nodeValue

			data_objectif = deque()
			for xml_execution in xml_goal.getElementsByTagName('action'):
				action 		= (xml_execution.getElementsByTagName('id_action')[0].firstChild.nodeValue,)
				action 		+= (xml_execution.getElementsByTagName('ordre')[0].firstChild.nodeValue,)
				action 		+= (xml_execution.getElementsByTagName('arguments')[0].firstChild.nodeValue,)
				data_objectif.append(action)

			objectif.append((idd, data_objectif))

		self.__objectifs = objectif
	

	def getMaxRot(self, id1, id2):
		"""Retourne le plus id de manière rotationnelle"""
		if id1 > id2 and (id1 - id2) < 255/2:
			return id1
		else:
			return id2

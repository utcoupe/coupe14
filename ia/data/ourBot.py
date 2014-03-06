# -*- coding: utf-8 -*-
"""
Classe pour nos robots
"""

from collections import deque
from xml.dom.minidom import parseString

class OurBot():
	def __init__(self, name, communication, arduinoConstantes, addressOther, addressAsserv, largeur, longueur):
		#Constantes
		self.communication = communication
		self.addressOther = addressOther
		self.addressAsserv = addressAsserv
		self.__name = name

		self.largeur = largeur 
		self.longueur = longueur


		#Valeurs récupérées (read-only)
		self.positionX = 0
		self.positionY = 0
		self.angle = 0.0
		self.__last_id_order_received = None

		#Variables
		self.__objectifs = None #((id, ((id_action, ordre, arguments), (id_action, ordre, arguments), ...)), ...)

	#Getter
	def getPositon(self):
		return (self.positionX, self.positionY)

	def getName(self):
		return self.__name

	def getLastIdOrderReceived(self):
		return self.__last_id_order_received


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

	#utilise les données en provenance de nos robots pour mettre à jour les données de la classe
	def majPosition(self, arguments):
		self.positionX = arguments[0]
		self.positionY = arguments[1]
		self.angle = arguments[2]

	def getNextIdOrder(self):
		if self.__objectifs != None:
			return (self.__objectifs[0][0], self.__objectifs[0][1][0]) #(id_objectif_0, id_action_0_de_objcetif_0)
		else:
			return None

	def getNextOrders(self):
		if self.__objectifs != None:
			objectif_en_cours = self.objectifs.popleft()
			order_of_objectif = objectif_en_cours[1] # type ((id_action, ordre, arguments),...)

			data_order = order_of_objectif.popleft() #type (id_action, ordre, arguments)
			output_temp = deque()
			output_temp.append(data_order)
			while data_order[1] != 'SLEEP' or data_order[1] != 'THEN' or data_order[1] != 'FIN':
				data_order = order_of_objectif.popleft()
				output_temp.append(data_order)

			if data_order[1] != 'FIN':
				self.__objectifs.appendleft(objectif_en_cours)
			else:
				#TODO tell objectifManager this objectif is over
				pass

			return output_temp # type ((id_action, ordre, arguments),...)

		else:
			return None

	


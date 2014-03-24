# -*- coding: utf-8 -*-
"""
Cette classe permet de communiquer avec le subprocess de choix d'objectif
"""

import threading
from multiprocessing import Process, Pipe
import logging
from collections import deque


from . import goals

class SubProcessCommunicate():
	def __init__(self, Data):
		self.__Data = Data
		self.__logger = logging.getLogger(__name__.split('.')[0])
		
		if self.__Data.Flussmittel is not None:
			self.__subprocess_flussmittel = MyProcess(self.__Data, self.__Data.Flussmittel.getName())
		if self.__Data.Tibot is not None:
			self.__subprocess_tibot = MyProcess(self.__Data, self.__Data.Tibot.getName())

		
	def readOrders(self):
		"""retourn les données des subprocess"""
		data = self.__Data.dataToDico()
		if self.__Data.Flussmittel is not None:
			self.__subprocess_flussmittel.sendPacket(("data", data)) #TODO: ça n'a rien à faire ici !
		if self.__Data.Tibot is not None:
			self.__subprocess_tibot.sendPacket(("data", data))#TODO: ça n'a rien à faire ici !

		input_list_1 = deque()
		if self.__Data.Flussmittel is not None:
			input_list_1 = self.__subprocess_flussmittel.readPacket()
		if self.__Data.Tibot is not None:
			input_list_2 = self.__subprocess_tibot.readPacket()
			for info in input_list_2:
				input_list_1.append(info)

		return input_list_1

	def sendObjectifOver(self, id_objectif):
		if self.__Data.Flussmittel is not None:
			self.__subprocess_flussmittel.sendPacket(("over", id_objectif))
		if self.__Data.Tibot is not None:
			self.__subprocess_tibot.sendPacket(("over", id_objectif))

	def sendObjectifCanceled(self, id_objectifs_canceled):
		if self.__Data.Flussmittel is not None:
			self.__subprocess_flussmittel.sendPacket(("over", id_objectifs_canceled))
		if self.__Data.Tibot is not None:
			self.__subprocess_tibot.sendPacket(("over", id_objectifs_canceled))


class MyProcess():
	def __init__(self, Data, robot_name):
		self.__Data = Data
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__input_buffer = deque()

		self.__parent_conn, self.__child_conn = Pipe()
		self.__process = Process(target=goals.startSubprocess, args=(self.__child_conn, robot_name) )
		self.__process.start()

		self.__Pull_thread = threading.Thread(target=self.__readPipe)
		self.__Pull_thread.start()
		

		
	def readPacket(self):
		if self.__input_buffer:
			return self.__input_buffer.popleft()
		else:
			return self.__input_buffer

	def sendPacket(self, packet):
		self.__parent_conn.send(packet)

	def __readPipe(self):
		while True:
			self.__input_buffer.append(self.__parent_conn.recv())


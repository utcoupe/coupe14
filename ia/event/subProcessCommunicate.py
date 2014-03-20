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
	def __init__(self):
		self.__logger = logging.getLogger(__name__.split('.')[0])
		self.__input_buffer = deque()

		self.__parent_conn, self.__child_conn = Pipe()
		self.__process = Process(target=goals.startSubprocess, args=(self.__child_conn,))
		self.__process.start()

		self.__Pull_thread = threading.Thread(target=self.__readPipe)
		self.__Pull_thread.start()
		

		
	def readBuffer(self):
		if self.__input_buffer:
			return self.__input_buffer.popleft()
		else:
			return self.__input_buffer

	def sendObjectifOver(self, id_objectif):
		pass

	def sendObjectifCanceled(self, id_objectifs_canceled):
		pass

	def __readPipe(self):
		self.__input_buffer.append(self.__parent_conn.recv())

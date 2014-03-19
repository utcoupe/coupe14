# -*- coding: utf-8 -*-
"""
Cette classe permet de communiquer avec le subprocess de choix d'objectif
"""

from multiprocessing import Process, Pipe

from . import goals

class SubProcessCommunicate():
	def __init__(self):
		self.__parent_conn, self.__child_conn = Pipe()
		self.__process = Process(target=goals.processEvent, args=(self.__child_conn,))
		self.__process.start()

		
	def read(self):
		#print(self.__parent_conn.recv())
		pass

	def sendObjectifOver(self, id_objectif):
		pass

	def sendObjectifCanceled(self, id_objectifs_canceled):
		pass
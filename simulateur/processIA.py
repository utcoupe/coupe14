__author__ = 'furmi'

import sys
import os
import time
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "ia"))

from comSimu import Communication
from hokuyo import Hokuyo
import threading
from multiprocessing import Process, Pipe
from define import *
import test
import main
from constantes import *

"""
Drapau qui permet de lancer :
- l'IA si TEST_MODE = False
- le programme de test si TEST_MODE = True
"""
TEST_MODE = True

class ProcessIA():
	"""
	Classe qui va lancer une IA en subprocess.
	Gère aussi la communication avec les IA lancées via un pipe.
	"""
	def __init__(self, color_and_robot_list):
		self.__color = color_and_robot_list[0]
		if color_and_robot_list[1] is not None:
			self.__bigrobot = color_and_robot_list[1]
			if color_and_robot_list[2] is not None:
				self.__minirobot = color_and_robot_list[2]
			else:
				self.__minirobot = None
		else:
			self.__bigrobot =None
			if color_and_robot_list[2] is not None:
				self.__minirobot = color_and_robot_list[2]
			else:
				self.__minirobot = None
		self.__robots = color_and_robot_list
		self.__hokuyo = Hokuyo(self.__robots[1:])
		self.__communication = Communication(self.__bigrobot, self.__minirobot, self.__hokuyo, self)
		#communication de data entre l'IA et le simu
		self.__parent_conn, self.__child_conn = Pipe()
		#lancement de l'ia
		if TEST_MODE == False:
			self.__process = Process(target=main.startIa, args=(self.__child_conn,self.__color))
		elif TEST_MODE == True :
			self.__process = Process(target=test.testIa, args=(self.__child_conn,self.__color)) #pour les tests
		self.__process.start()
		time.sleep(0.1)
		#on démarre le thread de lecture des données IA renvoyées à travers le pipe
		self.__read_thread = threading.Thread(target=self.__readPipe)
		self.__read_thread.start()

	def writePipe(self, addresse, ordre, args):
		"""
		Envoie des données à l'IA à travers le Pipe
		"""
		self.__parent_conn.send((addresse, ordre, args))

	def __readPipe(self):
		"""
		Méthode de lecture des données envoyées par l'IA via le pipe.
		recv est bloquant, donc lancé dans un thread
		"""
		while True:
			if self.__parent_conn.poll():
				message = self.__parent_conn.recv()
				self.__parseDataIa(message)



	def __parseDataIa(self, data):
		"""
		Formate les données IA reçues pour les adapter à la méthode
		sendOrderAPI de Communication
		"""
		self.__communication.orderBalancing(data[0],data[1],data[2])
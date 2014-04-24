__author__ = 'furmi'

import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "map"))

#pour importer les constantes des ordres et des robots
from define import *

from collections import deque
import time


class Communication():
	def __init__(self, bigrobot, minirobot, hokuyo, ia):
		self.__bigrobot = bigrobot	#objet robot, afin d'envoyer les ordres
		self.__minirobot = minirobot	#objet robot, afin d'envoyer les ordres
		self.__hokuyo = hokuyo #objet de type Hokuyo
		self.__ia = ia #objet processIA

	def orderBalancing(self, address, order, arguments):
		"""
		Méthode appelée par l'IA pour envoyer un ordre à travers le protocole
		@param enum de la partie du robot qui est appelée
		@param enum de l'ordre envoyé sur la partie
		@param args suivent l'ordre
		"""
		if (address == "ADDR_FLUSSMITTEL_OTHER"):
			self.__traitementFlussmittelOthers(order, arguments)
		elif (address == "ADDR_FLUSSMITTEL_ASSERV"):
			self.__traitementFlussmittelAsserv(order, arguments)
		elif (address == "ADDR_FLUSSMITTEL_CAM"):
			self.__traitementFlussmittelCam(order, arguments)
		elif (address == "ADDR_TIBOT_OTHER"):
			self.__traitementTibotOthers(order, arguments)
		elif (address == "ADDR_TIBOT_ASSERV"):
			self.__traitementTibotAsserv(order, arguments)
		elif (address == "ADDR_HOKUYO"):
			self.__traitementHokuyo(order, arguments)
		else:
			print('ordre non valide'+str(address))

	def __traitementFlussmittelOthers(self, order, args):
		"""
		Parse l'ordre envoyé à ADDR_FLUSSMITTEL_OTHER
		"""
		if (order == "O_BRAS_OUVRIR"):
			pos = ()
			self.__bigrobot.setlastIdActionOther(args[0])
			self.__addOrder("ADDR_FLUSSMITTEL_OTHER", order, pos)

		elif (order == "O_BRAS_FERMER"):
			pos = ()
			self.__bigrobot.setlastIdActionOther(args[0])
			self.__addOrder("ADDR_FLUSSMITTEL_OTHER", order, pos)

		elif (order == "GET_LAST_ID"):
			pos = (self.__bigrobot.getLastIdOther(),)
			self.__addOrder("ADDR_FLUSSMITTEL_OTHER", order, pos)

		elif (order == "RESET_ID"):
			pos = ()
			self.__bigrobot.resetIdOther()
			self.__addOrder("ADDR_FLUSSMITTEL_OTHER", order, pos)

		elif (order == "O_RET_OUVRIR"):
			pos = ()
			self.__bigrobot.setlastIdActionOther(args[0])
			self.__bigrobot.releaseFeu() #pour les tests
			self.__addOrder("ADDR_FLUSSMITTEL_OTHER", order, pos)

		elif (order == "O_RET_FERMER"):
			pos = ()
			self.__bigrobot.setlastIdActionOther(args[0])
			#TODO, implementer
			self.__addOrder("ADDR_FLUSSMITTEL_OTHER", order, pos)

		elif (order == "O_GET_TRIANGLE"):
			pos = ()
			self.__bigrobot.activerVisio()
			self.__bigrobot.setlastIdActionOther(args[0])
			self.__addOrder("ADDR_FLUSSMITTEL_OTHER", order, pos)

		elif (order == "O_STORE_TRIANGLE"):
			pos = ()
			self.__bigrobot.setlastIdActionOther(args[0])
			self.__addOrder("ADDR_FLUSSMITTEL_OTHER", order, pos)

		elif (order == "O_GET_BRAS_STATUS"):
			pos = (1,)
			self.__bigrobot.setlastIdActionOther(args[0])
			self.__addOrder("ADDR_FLUSSMITTEL_OTHER", order, pos)

		elif (order == "PINGPING"):
			pos = ()
			self.__bigrobot.setlastIdActionOther(args[0])
			self.__addOrder("ADDR_FLUSSMITTEL_OTHER", order, pos)

		else:
			print('Error : mauvais paramètre traitement Flussmittel other !')

	def __traitementFlussmittelAsserv(self, order, args):
		"""
		Parse l'ordre envoyé à ADDR_FLUSSMITTEL_ASSERV
		"""

		#on traite les ordres qui nécessitent de renvoyer des informations
		if (order == "A_GET_POS"):
			pos = self.__bigrobot.getPosition()
			fixed_pos = (pos[0], 2000-pos[1], pos[2])
			print('getPos : ', fixed_pos)
			self.__addOrder("ADDR_FLUSSMITTEL_ASSERV", order, fixed_pos)

		elif (order == "GET_LAST_ID"):
			pos = (self.__bigrobot.getLastIdAsserv(),)
			self.__addOrder("ADDR_FLUSSMITTEL_ASSERV", order, pos)

		elif (order == "A_GET_POS_ID"):
			pos = self.__bigrobot.getPositionId()
			pos_id = (pos[0], 2000-pos[1], pos[2], pos[3])
			self.__addOrder("ADDR_FLUSSMITTEL_ASSERV", order, pos_id)

		elif (order == "A_CLEANG"):
			pos = ()
			self.__bigrobot.cleanGoals()
			self.__addOrder("ADDR_FLUSSMITTEL_ASSERV", order, pos)

		elif (order == "RESET_ID"):
			pos = ()
			self.__bigrobot.resetIdAsserv()
			self.__addOrder("ADDR_FLUSSMITTEL_ASSERV", order, pos)

		elif (order == "A_SET_POS"):
			pos = ()
			self.__bigrobot.setPosition(args[0],2000-args[1], args[2])
			self.__addOrder("ADDR_FLUSSMITTEL_ASSERV", order, pos)

		elif (order == "PINGPING"):
			pos = ()
			self.__addOrder("ADDR_FLUSSMITTEL_ASSERV", order, pos)

		else:
			#on ajoute l'ordre reçu à la structure de renvoie
			self.__addOrder("ADDR_FLUSSMITTEL_OTHER", order, args)
			if (order == "PINGPING"):
				self.__bigrobot.ping()
			elif (order == "A_GOTOA"):
				self.__bigrobot.addGoalOrder(GOTOA, args)
			elif (order == "A_GOTO"):
				self.__bigrobot.addGoalOrder(GOTO, args)
			elif (order == "A_GOTOAR"):
				self.__bigrobot.addGoalOrder(GOTOAR, args)
			elif (order == "A_GOTOR"):
				self.__bigrobot.addGoalOrder(GOTOR, args)
			elif (order == "A_ROT"):
				self.__bigrobot.addGoalOrder(ROT, args)
			elif (order == "A_ROTR"):
				self.__bigrobot.addGoalOrder(ROTR, args)
			elif (order == "A_PWM"):
				self.__bigrobot.addGoalOrder(PWM, args)
			else:
				print('Error : mauvais paramètre traitement Flussmittel asserv !')

	def __traitementFlussmittelCam(self, order, args):
		"""
		Parse l'ordre envoyé à ADDR_FLUSSMITTEL_CAM
		"""
		pass

	def __traitementTibotOthers(self, order, args):
		"""
		Parse l'ordre envoyé à ADDR_TIBOT_OTHER
		"""
		if (order == "O_BRAS_OUVRIR"):
			pos = ()
			self.__minirobot.setlastIdActionOther(args[0])
			self.__addOrder("ADDR_TIBOT_OTHER", order, pos)

		elif (order == "O_BRAS_FERMER"):
			pos = ()
			self.__minirobot.setlastIdActionOther(args[0])
			self.__addOrder("ADDR_TIBOT_OTHER", order, pos)

		elif (order == "GET_LAST_ID"):
			pos = (self.__minirobot.getLastIdOther(),)
			self.__addOrder("ADDR_TIBOT_OTHER", order, pos)

		elif (order == "RESET_ID"):
			pos = ()
			self.__minirobot.resetIdOther()
			self.__addOrder("ADDR_TIBOT_OTHER", order, pos)

		elif (order == "O_RET_OUVRIR"):
			pos = ()
			self.__minirobot.setlastIdActionOther(args[0])
			#TODO, implementer
			self.__addOrder("ADDR_TIBOT_OTHER", order, pos)

		elif (order == "O_RET_FERMER"):
			pos = ()
			self.__minirobot.setlastIdActionOther(args[0])
			#TODO, implementer
			self.__addOrder("ADDR_TIBOT_OTHER", order, pos)

		elif (order == "PINGPING"):
			pos = ()
			self.__minirobot.setlastIdActionOther(args[0])
			self.__addOrder("ADDR_TIBOT_OTHER", order, pos)

		else:
			print('Error : mauvais paramètre traitement Tibot other !')

	def __traitementTibotAsserv(self, order, args):
		"""
		Parse l'ordre envoyé à ADDR_TIBOT_ASSERV
		"""
		#on traite les ordres qui nécessitent de renvoyer des informations
		if (order == "A_GET_POS"):
			pos = self.__minirobot.getPosition()
			fixed_pos = (pos[0], 2000-pos[1], pos[2])
			self.__addOrder("ADDR_TIBOT_ASSERV", order, fixed_pos)

		elif (order == "GET_LAST_ID"):
			pos = (self.__minirobot.getLastIdAsserv(),)
			self.__addOrder("ADDR_TIBOT_ASSERV", order, pos)

		elif (order == "A_GET_POS_ID"):
			pos = self.__minirobot.getPositionId()
			pos_id = (pos[0], 2000-pos[1], pos[2], pos[3])
			self.__addOrder("ADDR_TIBOT_ASSERV", order, pos_id)

		elif (order == "A_CLEANG"):
			pos = ()
			self.__minirobot.cleanGoals()
			self.__addOrder("ADDR_TIBOT_ASSERV", order, pos)

		elif (order == "RESET_ID"):
			pos = ()
			self.__minirobot.resetIdAsserv()
			self.__addOrder("ADDR_TIBOT_ASSERV", order, pos)

		elif (order == "A_SET_POS"):
			pos = ()
			self.__minirobot.setPosition(args[0],2000-args[1], args[2])
			self.__addOrder("ADDR_TIBOT_ASSERV", order, pos)

		elif (order == "PINGPING"):
			pos = ()
			self.__addOrder("ADDR_TIBOT_ASSERV", order, pos)

		else:
			if (order == "PINGPING"):
				self.__minirobot.ping()
			elif (order == "A_GOTOA"):
				self.__minirobot.addGoalOrder(GOTOA, args)
			elif (order == "A_GOTO"):
				self.__minirobot.addGoalOrder(GOTO, args)
			elif (order == "A_GOTOAR"):
				self.__minirobot.addGoalOrder(GOTOAR, args)
			elif (order == "A_GOTOR"):
				self.__minirobot.addGoalOrder(GOTOR, args)
			elif (order == "A_ROT"):
				self.__minirobot.addGoalOrder(ROT, args)
			elif (order == "A_ROTR"):
				self.__minirobot.addGoalOrder(ROTR, args)
			elif (order == "A_CLEANG"):
				self.__minirobot.cleanGoals()
			elif (order == "A_PWM"):
				self.__minirobot.addGoalOrder(PWM, args)
			else:
				print('Error : mauvais paramètre traitement Tibot asserv !')

	def __traitementHokuyo(self, order, args):
		"""
		Parse l'ordre envoyé à ADDR_HOKUYO
		"""
		if(order == "GET_HOKUYO"):
			data = tuple(self.__hokuyo.getHokuyo())
			data_to_ret = data
			self.__addOrder("ADDR_HOKUYO", order, data_to_ret)

	def __addOrder(self, addr, ordre, args):
		self.__ia.writePipe(addr, ordre, args)


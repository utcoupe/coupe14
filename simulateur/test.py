__author__ = 'furmi'

from define import *

def testIa(conn):
	"""
	self.__color = self.__bigrobot.getTeam()
	if self.__color == RED:
		conn.send((ADDR_TIBOT_ASSERV,A_GOTO,49,2000,400))
	elif self.__color == YELLOW:
		conn.send((ADDR_TIBOT_ASSERV,A_GOTO,36,1000,800))
	"""
	conn.send((ADDR_TIBOT_ASSERV,A_GOTO,36,1000,800))

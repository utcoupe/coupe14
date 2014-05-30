# -*- coding: utf-8 -*-
"""
Class used to reprsent a goal
goal<-ElemGoal<-script
"""

from .constantes import *
from collections import deque

class Goal:
	def __init__(self, id, name, type, concerned_robot, x, y):
		self.__id 				= id
		self.__name 			= name
		self.__type				= type
		self.__concerned_robot 	= concerned_robot
		self.__x 				= x
		self.__y 				= y
		self.__elem_goal = []
		self.__elem_goal_locked = None
		self.__area_status = "EMPTY" #type "EMPTY", "FULL", "ENEMY"
		#données pour la gestion UpdateAlreadyDone
		self.__est_ce_qu_on_m_ait_passé_dessus		= False
		self.__time_stamp_proximity = -1
		self.__already_done		= 0 # From 0 (not finished) to 100 (finished)

		self.__color_for_script_torche = deque()# 1: ma_couleur, 0: pas ma couleur
		self.__color_for_script_torche.append("HACK")# HACK, sup au STEP_OVER
		self.__color_for_script_torche.append(1)
		self.__color_for_script_torche.append(0)
		self.__color_for_script_torche.append(1)

	def getColorForScriptTorche(self):
		return self.__color_for_script_torche[0]

	def getId(self):
		return self.__id

	def getName(self):
		return self.__name

	def getType(self):
		return self.__type

	def getPosition(self):
		return (self.__x, self.__y)

	def getLenElemGoal(self):
		return len(self.__elem_goal)

	def getElemGoalOfId(self, elem_goal_id):
		return self.__elem_goal[elem_goal_id]

	def getElemGoalLocked(self):
		return self.__elem_goal_locked

	def getAreaStatus(self):
		return self.__area_status

	def setAreaStatus(self, status):
		if status in ("EMPTY", "FULL", "ENEMY"):
			self.__area_status = status
		else:
			self.__logger.error("Status impossible status, "+str(status))

	def setElemGoalLocked(self, elem_goal):
		self.__elem_goal_locked = elem_goal


	def isFinished(self):
		return (self.__already_done > FINISHED_THRESHOLD)

	def appendElemGoal(self, ElemGoal):
		self.__elem_goal.append(ElemGoal)

	def getColorElemLock(self):
		return self.__elem_goal_locked.getColor()

	def switchColor(self):
		for elem_goal_temp in self.__elem_goal:
			elem_goal_temp.switchColor()

	#Gestion des actions elementaires
	def getFirstElemAction(self):
		action_objectif = self.__elem_goal_locked.getNextElemAction()
		action_list = deque()
		for action in action_objectif:
			action_list.append(action)
			if action[0] == "END" or action[0] == "STEP_OVER":
				break
		return action_list

	def removeFirstElemAction(self):
		self.__color_for_script_torche.popleft()
		for elem in self.__elem_goal:
			action_objectif = elem.getNextElemAction()
			if action_objectif:
				action = action_objectif.popleft()
				while action[0] != "END" and action[0] != "STEP_OVER":
					action = action_objectif.popleft()

	def resetElemAction(self):
		for elem in self.__elem_goal:
			elem.reset_elem_action()

	def getAlreadyDone(self):
		return self.__already_done

	def setAlreadyDone(self, pourcentage):
		self.__already_done = pourcentage

	def setGoalDone(self,value):
		self.__est_ce_qu_on_m_ait_passé_dessus = value

	def getGoalDone(self):
		return self.__est_ce_qu_on_m_ait_passé_dessus

	def setTSProximiy(self,value):
		self.__time_stamp_proximity = value

	def getTSProximiy(self):
		return self.__time_stamp_proximity
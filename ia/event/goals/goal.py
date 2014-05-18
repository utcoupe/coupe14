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
		self.__finished			= 0 # From 0 (not finished) to 100 (finished)

		self.__elem_goal = []
		self.__elem_goal_locked = None

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

	def setElemGoalLocked(self, elem_goal):
		self.__elem_goal_locked = elem_goal

	def incrementFinished(self, by_value):
		self.__finished += int(by_value)

	def isFinished(self):
		return (self.__finished > FINISHED_THRESHOLD)

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
		for elem in self.__elem_goal:
			action_objectif = elem.getNextElemAction()
			if action_objectif:
				action = action_objectif.popleft()
				while action[0] != "END" and action[0] != "STEP_OVER":
					action = action_objectif.popleft()

	def resetElemAction(self):
		#TODO verifier qu'on ne veut pas reset les objectifs
		pass


	"""def toXml(self):
		string =  "<goal name='" + self.__name + "'>\n\t<type>" + self.__type + "</type>\n"
		string += "\t<location-x>" + str(self.__location[0]) +"</location-x>\n\t<location-y>" + str(self.__location[1]) +"</location-y>\n"
		string += "\t<finished>" + str(self.__finished) + "</finished>\n\t<executions>\n\t"
		for execution in self.executions:
			string += execution.toXml()
		string += "\t</executions>\n</goal>\n"
		return string"""

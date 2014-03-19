# -*- coding: utf-8 -*-
"""
Cette classe permet de gèrer le sub-process en charge du choix d'objectif
"""

import time


#import goalsManager

#self.__GoalsManager = goalsManager.GoalsManager()
def processEvent(conn):
	i = 42;
	while True:
		conn.send([i, None, 'hello'])
		i = i+1
		time.sleep(2)
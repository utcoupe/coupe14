#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	Simulateur UTCoupe 2014 : GUI
	Fichier : gui_actions.py
	Fonction : Création du frame "actions"

	Permet de créer le frame "actions". (cf la doc sur le wiki UTCoupe)
	Frame qui gère :
	- la liste des actions à accomplir (big_robot)
	- la liste des actions accomplies (big_robot)
	- la liste des actions à accomplir (mini_robot)
	- la liste des actions accomplies (mini_robot)
"""

__author__ = "Thomas Fuhrmann"
__copyright__ = "Copyright 2013, UTCoupe 2014"

from tkinter import *
import threading
import time

class actions(Frame):
	""" Frame qui regroupe les widgets du frame actions.
	Hérite de Frame."""
	def __init__(self, fenetre, bots, **kwargs):
		"""
		@param fenetre : frame de la fenêtre principale
		"""
		Frame.__init__(self, fenetre, width=300, height=700, bg="green")
		self.__bigrobot_us = bots[1]
		self.__minirobot_us = bots[2]
		self.__bigrobot_en = bots[3]
		self.__minirobot_en = bots[4]

		#view
		self.grid()
		self.__liste_todo_big = []
		self.__liste_todo_mini = []
		self.frame_actions(robot="big", liste="todo")
		self.frame_actions(robot="mini", liste="todo")

		self.__autoscroll_on = True
		threading.Thread(target=self.__pullOrders).start()

	def __pullOrders(self):
		while 1:
			#pour le gros
			if len(self.__liste_todo_big) == 0: #cas où la liste est vide
				for item in self.__liste_todo_big:
					self.__listebox_big.insert(END, item)
			#liste complète du robot
			big_all = self.__bigrobot_us.getSaveOrder()
			diff_taille_big = len(big_all) - len(self.__liste_todo_big)
			to_ret_big = [] #liste de la différence entre la liste affichée et celle du robot
			taille_big_liste = len(self.__liste_todo_big)
			for i in range(diff_taille_big):
				#on les ajoute à la liste des ajouts
				self.__liste_todo_big.append(big_all[taille_big_liste + i - 1])
				to_ret_big.append(big_all[taille_big_liste + i - 1])
			for item in to_ret_big:
				#on les ajoute à la GUI
				self.__listebox_big.insert(END, item)
			#autoscroll
			if self.__autoscroll_on == True:
				self.__listebox_big.select_set(END)
				self.__listebox_big.yview(END)
			#pour le petit test
			if len(self.__liste_todo_mini) == 0:
				for item in self.__liste_todo_mini:
					self.__listebox_mini.insert(END, item)
			mini_all = self.__minirobot_us.getSaveOrder()
			diff_taille_mini = len(mini_all) - len(self.__liste_todo_mini)
			to_ret_mini = []
			taille_mini_liste = len(self.__liste_todo_mini)
			for i in range(diff_taille_mini):
				self.__liste_todo_mini.append(mini_all[taille_mini_liste + i - 1])
				to_ret_mini.append(mini_all[taille_mini_liste + i - 1])
			for item in to_ret_mini:
				self.__listebox_mini.insert(END, item)
			#autoscroll
			if self.__autoscroll_on == True:
				self.__listebox_mini.select_set(END)
				self.__listebox_mini.yview(END)
			time.sleep(0.5)

	def frame_actions(self, robot, liste):
		"""
		Permet de créer le frame nommé d'une liste d'action d'un robot.
		@param robot = {big, mini}
		@param liste = {todo, done}
		"""
		Factions = LabelFrame(self, text=robot+"_"+liste, bg="yellow")
		self.liste_actions(robot=robot, type_liste=liste, parent=Factions)
		Factions.grid(column=self.position(robot, liste), row=0)

	def position(self, robot, liste):
		"""
		Permet de parser les données robot et liste.
		@param robot = {big, mini}
		@param liste = {todo, done}
		"""
		if (robot == "big"):
			if(liste == "todo"):
				return 0
			else:
				return 0
		else:
			if(liste == "todo"):
				return 1
			else:
				return 1

	def __listbox_cliqued(self, event):
		self.__autoscroll_on = False

	def liste_actions(self, robot, type_liste, parent):
		"""
		Permet d'afficher les données actions d'un de nos robots.
		@param robot : type de robot (big, mini)
		@param type_liste : type de la liste (todo, done)
		@param parent : frame parent
		"""
		#! ajouter l'accès aux données de l'IA !
		#creation de la scrollbar
		scroll = Scrollbar(parent)
		scroll.grid(column=1, row=0, sticky=N+S)
		#creation des listes
		if robot == "big":
			self.__listebox_big = Listbox(parent, width=30)
			self.__listebox_big.bind('<<ListboxSelect>>', self.__listbox_cliqued)
			self.__listebox_big.grid(column=0, row=0)
			self.__listebox_big.config(yscrollcommand=scroll.set)
			scroll.config(command=self.__listebox_big.yview)
		else:
			self.__listebox_mini = Listbox(parent, width=30)
			self.__listebox_mini.bind('<<ListboxSelect>>', self.__listbox_cliqued)
			self.__listebox_mini.grid(column=0, row=0)
			self.__listebox_mini.config(yscrollcommand=scroll.set)
			scroll.config(command=self.__listebox_mini.yview)


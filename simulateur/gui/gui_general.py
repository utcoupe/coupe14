#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	Simulateur UTCoupe 2014 : GUI
	Fichier : gui_general.py
	Fonction : Création du frame "général"

	Permet de créer le frame "général". (cf la doc sur le wiki UTCoupe)
	Frame qui gère :
	- modes de fonctionnement du simulateur
	- boutons start/stop/pause
	- temps écoulé/restant
	- team
	- nombre de points
"""

__author__ = "Thomas Fuhrmann"
__copyright__ = "Copyright 2013, UTCoupe 2014"

from tkinter import *
import threading
import time
import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "../../GUI/viznavgraph"))
from define import *
import viznavgraph as nav

class general(Frame):
	""" Frame qui regroupe les widgets du frame général.
	Hérite de Frame."""

	def __init__(self, fenetre, bots, **kwargs):
		"""
		@param fenetre : frame de la fenêtre principale
		@param bots : liste des robots (our_big,our_mini,en_big,en_mini)
		"""
		Frame.__init__(self, fenetre, width=300, height=700, bg="yellow")
		#données
		self.__time_count = 0
		self.__temps_ecoule = StringVar()
		self.__temps_restant= StringVar()
		self.__bigrobot_us = bots[1]
		self.__minirobot_us = bots[2]
		self.__bigrobot_en = bots[3]
		self.__minirobot_en = bots[4]
		self.__bots = bots
		self.__match_started = False

		#frames
		self.grid()
		self.mode()
		self.boutons()
		self.temps()
		self.team()
		self.nbrPts()

	def __timeThread(self):
		"""
		Thread qui compte le temps (pour l'affichage)
		"""
		while 1:
			self.__temps_ecoule.set(str(self.__time_count))
			self.__temps_restant.set(str(90 - self.__time_count))
			time.sleep(1)
			self.__time_count += 1

	def mode(self):
		"""
		Permet de sélectionner le mode de fonctionnement du simulateur.
		"""
		#! ajouter les traitements !
		Fmode = LabelFrame(self, text="Mode de fonctionnement du simulateur", bg="red")
		liste_mode = ["Normal", "Reply", "Coupe", "Vizgraph"]
		self.choix_mode = StringVar()
		self.choix_mode.set(liste_mode[0])
		for n in range(4):
			bout = Radiobutton(Fmode,
							   text = liste_mode[n],
							   variable = self.choix_mode,
							   value = liste_mode[n])
			if n == 3:
				bout.config(command=self.__startViz)
			bout.grid(column = n, row = 0)
		Fmode.grid(column = 0, row = 0, sticky=N+S+W+E, columnspan=2)

	def __startViz(self):
		nav.startVizNavGraph(self.__bots)

	def boutons(self):
		"""
		Création des boutons start/stop/pause.
		"""
		#! ajouter les traitements !
		Fbouton = LabelFrame(self, text="Bouton de contrôle", bg="blue")
		liste_button = ["Start", "Stop", "Pause"]
		for n in range(3):
			bout = Button(Fbouton, text = liste_button[n])
			if n == 0: #bouton start
				if self.__minirobot_us is not None:
					bout.config(command=self.__startMatchMini)
				elif self.__bigrobot_us is not None:
					bout.config(command=self.__startMatchBig)
			bout.grid(column = n, row = 0)
		Fbouton.grid(column = 2, row = 0, sticky=N+S+W+E)

	def __startMatchMini(self):
		if self.__match_started is False:
			threading.Thread(target=self.__timeThread).start()
			self.__minirobot_us.setStateJack()
			self.__minirobot_en.setStateJack()

	def __startMatchBig(self):
		if self.__match_started is False:
			threading.Thread(target=self.__timeThread).start()
			self.__bigrobot_us.setStateJack()
			self.__bigrobot_en.setStateJack()

	def temps(self):
		"""
		Permet d'afficher le temps restant et le temps écoulé.
		"""
		#! ajouter l'accès aux données de l'IA !
		Ftemps = LabelFrame(self, text="Gestion du temps", bg="green")
		tpsE = Label(Ftemps, text="Temps écoulé")
		tpsE.grid(column=0, row=0)
		tpsR = Label(Ftemps, text="Temps restant")
		tpsR.grid(column = 1, row = 0)
		Ftemps.grid(column = 1, row = 1)
		secE = Label(Ftemps, textvariable=self.__temps_ecoule)
		secE.grid(column=0, row=1)
		secR = Label(Ftemps, textvariable=self.__temps_restant)
		secR.grid(column = 1, row = 1)
		Ftemps.grid(column = 0, row = 2, sticky=N+S)

	def team(self):
		"""
		Permet d'afficher la team actuelle.
		"""
		#! ajouter l'accès aux données de l'IA !
		Fteam = LabelFrame(self, text="Team", bg="white")
		labelfont = ('times', 20, 'bold')
		if self.__bigrobot_us is not None:
			if self.__bigrobot_us.getTeam() == RED:
				equipe = Label(Fteam, text="Red", bg="red")
			elif self.__bigrobot_us.getTeam() == YELLOW:
				equipe = Label(Fteam, text="Yellow", bg="yellow")
		elif self.__minirobot_us is not None:
			if self.__minirobot_us.getTeam() == RED:
				equipe = Label(Fteam, text="Red", bg="red")
			elif self.__minirobot_us.getTeam() == YELLOW:
				equipe = Label(Fteam, text="Yellow", bg="yellow")
		else:
			equipe = Label(Fteam, text="None", bg="grey")
		equipe.config(font=labelfont, anchor=CENTER)
		equipe.grid()
		Fteam.grid(column = 1, row = 2, sticky=N+S)

	def nbrPts(self):
		"""
		Permet d'afficher le tnombre de points.
		"""
		#! ajouter l'accès aux données de l'IA !
		Fpoints = LabelFrame(self, text="Nombre de points", bg="pink")
		labelfont = ('times', 20, 'bold')
		points = Label(Fpoints, text="xx")
		points.config(font=labelfont, anchor=CENTER)
		points.grid(column=0, padx=35)
		Fpoints.grid(column = 2, row = 2, sticky=N+S)

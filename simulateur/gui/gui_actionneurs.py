#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	Simulateur UTCoupe 2014 : GUI
	Fichier : gui_actionneurs.py
	Fonction : Création du frame "actionneurs"

	Permet de créer le frame "actionneurs". (cf la doc sur le wiki UTCoupe)
	Frame qui gère :
	- affichage de l'état des actionneurs
	- affichage des données des capteurs

	Note : A compléter ! Actuellement vide.
"""

__author__ = "Thomas Fuhrmann"
__copyright__ = "Copyright 2013, UTCoupe 2014"

from tkinter import *
import threading
import time

class actionneurs(LabelFrame):
	""" Frame qui regroupe les widgets du frame actionneurs.
	Hérite de Frame."""
	def __init__(self, fenetre, bots, *args):
		"""
		@param fenetre : frame de la fenêtre principale
		@param bots : liste des robots (our_big,our_mini,en_big,en_mini)
		"""
		LabelFrame.__init__(self, fenetre, text="Actionneurs et capteurs", width=300, height=100, bg="white")
		self.grid(sticky=W+E)
		#données
		self.__bigrobot_us = bots[1]
		self.__minirobot_us = bots[2]
		self.__feu_av_big = StringVar()
		self.__feu_ar_big = StringVar()
		self.__balles_mini = StringVar()
		self.__filet_mini = StringVar()
		self.__fresques_mini = StringVar()
		self.display_actionneurs_big(0, self)
		self.display_actionneurs_mini(1, self)
		threading.Thread(target=self.__pullDataRobots).start()

	def __pullDataRobots(self):
		"""
		Thread pour pull les données du robot
		"""
		while 1:
			self.__feu_av_big.set('N feu av : ' + str(self.__bigrobot_us.getFeuxAvant()))
			self.__feu_ar_big.set('N feu ar : ' + str(self.__bigrobot_us.getFeuxArriere()))
			self.__balles_mini.set('Nbr lances : ' + str(self.__minirobot_us.getNbrLances()))
			self.__filet_mini.set('Filet : ' + str(self.__minirobot_us.getFilet()))
			self.__fresques_mini.set('Nbr fresques : ' + str(self.__minirobot_us.getNbrFresques()))
			time.sleep(1)

	def display_actionneurs_big(self, colonne, parent):
		"""
		Permet d'afficher les données d'un de nos robots.
		@param colonne : numéro de la colonne
		@param parent : frame parent
		"""
		Frobot = LabelFrame(self, text='Données gros', bg="blue")
		self.__feu_av_big_label = Label(Frobot, textvariable=self.__feu_av_big)
		self.__feu_av_big_label.grid(row=0)
		self.__feu_ar_big_label = Label(Frobot, textvariable=self.__feu_ar_big)
		self.__feu_ar_big_label.grid(row=1)
		Frobot.grid(column=colonne, row=0, in_=parent)

	def display_actionneurs_mini(self, colonne, parent):
		"""
		Permet d'afficher les données d'un de nos robots.
		@param colonne : numéro de la colonne
		@param parent : frame parent
		"""
		Frobot = LabelFrame(self, text='Données mini', bg="yellow")
		self.__balles_mini_label = Label(Frobot, textvariable=self.__balles_mini)
		self.__balles_mini_label.grid(row=0)
		self.__filet_mini_label = Label(Frobot, textvariable=self.__filet_mini)
		self.__filet_mini_label.grid(row=1)
		self.__fresques_mini_label = Label(Frobot, textvariable=self.__fresques_mini)
		self.__fresques_mini_label.grid(row=2)
		Frobot.grid(column=colonne, row=0, in_=parent)
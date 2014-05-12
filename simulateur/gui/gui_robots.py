#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	Simulateur UTCoupe 2014 : GUI
	Fichier : gui_robots.py
	Fonction : Création du frame "robots"

	Permet de créer le frame "robots". (cf la doc sur le wiki UTCoupe)
	Frame qui gère :
	- position et état de nos robots
	- position et état des robots ennemis
"""

__author__ = "Thomas Fuhrmann"
__copyright__ = "Copyright 2013, UTCoupe 2014"

from tkinter import *
import threading
import time


class robots(Frame):
	""" Frame qui regroupe les widgets du frame robots.
	Hérite de Frame."""

	def __init__(self, fenetre, bots, **kwargs):
		"""
		@param fenetre : frame de la fenêtre principale
		"""
		Frame.__init__(self, fenetre, width=300, height=700, bg="red")
		self.__bigrobot_us = bots[1]
		self.__minirobot_us = bots[2]
		self.__bigrobot_en = bots[3]
		self.__minirobot_en = bots[4]
		#données
		self.fen = fenetre
		self.__x_big = StringVar()
		self.__y_big = StringVar()
		self.__a_big = StringVar()
		self.__id_big = StringVar()
		self.__x_mini = StringVar()
		self.__y_mini = StringVar()
		self.__a_mini = StringVar()
		self.__id_mini = StringVar()
		self.__x_big_en = StringVar()
		self.__y_big_en = StringVar()
		self.__x_mini_en = StringVar()
		self.__y_mini_en = StringVar()
		#affichage
		self.grid(sticky=E + W)
		self.robots_us()
		self.robots_enemy()
		threading.Thread(target=self.__pullDataRobots).start()

	def __pullDataRobots(self):
		while 1:
			self.__x_big.set(str(self.__bigrobot_us.getXreal()))
			self.__y_big.set(str(self.__bigrobot_us.getYreal()))
			self.__a_big.set(str(round(self.__bigrobot_us.getAreal(),3)))
			self.__id_big.set(str(self.__bigrobot_us.getLastId()))
			self.__x_mini.set(str(self.__minirobot_us.getXreal()))
			self.__y_mini.set(str(self.__minirobot_us.getYreal()))
			self.__a_mini.set(str(round(self.__minirobot_us.getAreal(),3)))
			self.__id_mini.set(str(self.__minirobot_us.getLastId()))
			self.__x_big_en.set(str(self.__bigrobot_en.getXreal()))
			self.__y_big_en.set(str(self.__bigrobot_en.getYreal()))
			self.__x_mini_en.set(str(self.__minirobot_en.getXreal()))
			self.__y_mini_en.set(str(self.__minirobot_en.getYreal()))
			time.sleep(0.25)

	def robots_us(self):
		"""
		Permet d'afficher le frame général regroupant nos 2 robots.
		"""
		Frobots_us = LabelFrame(self, text="Donnees sur nos robots", bg="blue")
		self.display_big(0, Frobots_us)
		self.display_mini(1, Frobots_us)
		Frobots_us.grid(column=0, row=0, sticky=E + W)

	def display_big(self, colonne, parent):
		"""
		Permet d'afficher les données d'un de nos robots.
		@param colonne : numéro de la colonne
		@param parent : frame parent
		"""
		#! ajouter l'accès aux données de l'IA !
		Frobot = LabelFrame(self, text='Données gros')
		self.__x_big_label = Label(Frobot, textvariable=self.__x_big)
		self.__x_big_label.grid(row=0)
		self.__y_big_label = Label(Frobot, textvariable=self.__y_big)
		self.__y_big_label.grid(row=1)
		self.__a_big_label = Label(Frobot, textvariable=self.__a_big)
		self.__a_big_label.grid(row=2)
		self.__id_big_label = Label(Frobot, textvariable=self.__id_big)
		self.__id_big_label.grid(row=3)
		Frobot.grid(column=colonne, row=0, in_=parent)

	def display_mini(self, colonne, parent):
		"""
		Permet d'afficher les données d'un de nos robots.
		@param colonne : numéro de la colonne
		@param parent : frame parent
		"""
		#! ajouter l'accès aux données de l'IA !
		Frobot = LabelFrame(self, text='Données mini')
		self.__x_mini_label = Label(Frobot, textvariable=self.__x_mini)
		self.__x_mini_label.grid(row=0)
		self.__y_mini_label = Label(Frobot, textvariable=self.__y_mini)
		self.__y_mini_label.grid(row=1)
		self.__a_mini_label = Label(Frobot, textvariable=self.__a_mini)
		self.__a_mini_label.grid(row=2)
		self.__id_mini_label = Label(Frobot, textvariable=self.__id_mini)
		self.__id_mini_label.grid(row=3)
		Frobot.grid(column=colonne, row=0, in_=parent)

	def robots_enemy(self):
		"""
		Permet d'afficher le frame général regroupant les 2 robots adverses.
		"""
		Frobots_enemy = LabelFrame(self, text="Donnees sur les robots adverses", bg="pink")
		self.display_big_enemy(0, Frobots_enemy)
		self.display_mini_enemy(1, Frobots_enemy)
		Frobots_enemy.grid(column=1, row=0, sticky=N + S + E + W)

	def display_big_enemy(self, colonne, parent):
		"""
		Permet d'afficher les données d'un des robots adverses.
		@param colonne : numéro de la colonne
		@param parent : frame parent
		"""
		#! ajouter l'accès aux données de l'IA !
		FrobotsE = LabelFrame(self, text='Big ennemy')
		self.__x_big_en_label = Label(FrobotsE, textvariable=self.__x_big_en)
		self.__x_big_en_label.grid(row=0)
		self.__y_big_en_label = Label(FrobotsE, textvariable=self.__y_big_en)
		self.__y_big_en_label.grid(row=1)
		FrobotsE.grid(column=colonne, row=0, in_=parent)

	def display_mini_enemy(self, colonne, parent):
		"""
		Permet d'afficher les données d'un des robots adverses.
		@param colonne : numéro de la colonne
		@param parent : frame parent
		"""
		#! ajouter l'accès aux données de l'IA !
		FrobotsE = LabelFrame(self, text='Mini ennemy')
		self.__x_mini_en_label = Label(FrobotsE, textvariable=self.__x_mini_en)
		self.__x_mini_en_label.grid(row=0)
		self.__y_mini_en_label = Label(FrobotsE, textvariable=self.__y_mini_en)
		self.__y_mini_en_label.grid(row=1)
		FrobotsE.grid(column=colonne, row=0, in_=parent)

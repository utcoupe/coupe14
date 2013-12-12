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

class robots(Frame):
    """ Frame qui regroupe les widgets du frame robots.
    Hérite de Frame."""
    def __init__(self, fenetre, **kwargs):
        """
        @param fenetre : frame de la fenêtre principale
        """
        Frame.__init__(self, fenetre, width=300, height=700, bg="red")
        self.grid(sticky=E+W)
        self.robots_us()
        self.robots_enemy()

    def robots_us(self):
        """
        Permet d'afficher le frame général regroupant nos 2 robots.
        """
        Frobots_us = LabelFrame(self, text="Donnees sur nos robots", bg="blue")
        self.robots("big", 0, Frobots_us)
        self.robots("mini", 1, Frobots_us)
        Frobots_us.grid(column=0, row=0, sticky=E+W)

    def robots_enemy(self):
        """
        Permet d'afficher le frame général regroupant les 2 robots adverses.
        """
        Frobots_enemy = LabelFrame(self, text="Donnees sur les robots adverses", bg="pink")
        self.robotsE("enemy1", 0, Frobots_enemy)
        self.robotsE("enemy2", 1, Frobots_enemy)
        Frobots_enemy.grid(column=1, row=0, sticky=N+S+E+W)

    def robots(self, type, colonne, parent):
        """
        Permet d'afficher les données d'un de nos robots.
        @param type : type de robot (big, mini), sert au titre
        @param colonne : numéro de la colonne
        @param parent : frame parent
        """
        #! ajouter l'accès aux données de l'IA !
        Frobot = LabelFrame(self, text=type)
        Label(Frobot, text="Pos x : 150").grid(row=0)
        Label(Frobot, text="Pos y : 257").grid(row=1)
        Label(Frobot, text="Angle : 10").grid(row=2)
        Label(Frobot, text="State : action").grid(row=3)
        Frobot.grid(column=colonne, row=0, in_=parent)

    def robotsE(self, type, colonne, parent):
        """
        Permet d'afficher les données d'un des robots adverses.
        @param type : type de robot (enemy1, enemy2), sert au titre
        @param colonne : numéro de la colonne
        @param parent : frame parent
        """
        #! ajouter l'accès aux données de l'IA !
        FrobotsE = LabelFrame(self, text=type)
        Label(FrobotsE, text="Pos x : 2000").grid(row=0)
        Label(FrobotsE, text="Pos y : 350").grid(row=1)
        FrobotsE.grid(column=colonne, row=0, in_=parent)

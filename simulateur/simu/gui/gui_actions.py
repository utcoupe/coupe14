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

class actions(Frame):
    """ Frame qui regroupe les widgets du frame actions.
    Hérite de Frame."""
    def __init__(self, fenetre, **kwargs):
        """
        @param fenetre : frame de la fenêtre principale
        """
        Frame.__init__(self, fenetre, width=300, height=700, bg="green")
        self.grid()
        self.liste_todo = ["atchoum", "aie", "test", "carnage", "bleu", "blanc", "violet", "rouge", "bleu", "blanc", "violet", "rouge"]
        self.liste_done = ["bleu", "blanc", "violet", "rouge"]
        self.frame_actions(robot="big", liste="todo")
        self.frame_actions(robot="big", liste="done")
        self.frame_actions(robot="mini", liste="todo")
        self.frame_actions(robot="mini", liste="done")
        
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
                return 1
        else:
            if(liste == "todo"):
                return 2
            else:
                return 3

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
        liste = Listbox(parent, width=12)
        if (type_liste == "todo"):
            for item in self.liste_todo:
                liste.insert(END, item)
        else:
            for item in self.liste_done:
                liste.insert(END, item)
        liste.grid(column=0, row=0)
        #on attache les deux
        liste.config(yscrollcommand=scroll.set)
        scroll.config(command=liste.yview)
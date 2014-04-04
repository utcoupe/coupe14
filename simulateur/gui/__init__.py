#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Simulateur UTCoupe 2014 : GUI
    Fichier : main.py
    Fonction : lancer la GUI, créer le frame principal

    C'est le point d'entrée du package gui pour le simulateur.
    Permet d'importer l'ensemble des modules et de lancer la GUI.

    Note : le fonctionnement du package est expliqué dans le wiki UTCoupe.
"""

__author__ = "Thomas Fuhrmann"
__copyright__ = "Copyright 2013, UTCoupe 2014"

from tkinter import *
import gui_general
import gui_robots
import gui_actions
import gui_actionneurs

if __name__ == '__main__':
    fen = Tk()
    fen.title("Test de GUI pour le simulateur")
    wids = gui_general.general(fen)
    robots = gui_robots.robots(fen)
    actions = gui_actions.actions(fen)
    effecteur = gui_actionneurs.actionneurs(fen)
    fen.mainloop()
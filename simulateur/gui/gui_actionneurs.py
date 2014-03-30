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

class actionneurs(LabelFrame):
    """ Frame qui regroupe les widgets du frame actionneurs.
    Hérite de Frame."""
    def __init__(self, fenetre, *args):
        """
        @param fenetre : frame de la fenêtre principale
        """
        LabelFrame.__init__(self, fenetre, text="Actionneurs et capteurs", width=300, height=100, bg="white")
        self.grid(sticky=W+E)
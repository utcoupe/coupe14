#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Simulateur UTCoupe 2014 : simuscreen
    Fichier : __init__.py
    Fonction : lancer le simulateur (partie affichage)

    C'est le point d'entrée du package simuscreen pour le simulateur.
    Permet d'importer l'ensemble des modules du simulateur nécessaires pour l'affichage exclusivement.

    Note : le fonctionnement du package est expliqué dans le wiki UTCoupe.
"""

__author__ = "Thomas Fuhrmann"

from engine import *
from define import *

if __name__ == "__main__":
    eng = Engine()

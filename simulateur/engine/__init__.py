#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Simulateur UTCoupe 2014 : engine
    Fichier : __init__.py
    Fonction : lancer l'engine

    C'est le point d'entrée du package engine pour le simulateur.
    Permet de lancer l'engine (moteur physique + moteur graphique)

    Note : le fonctionnement du package est expliqué dans le wiki UTCoupe.
"""

__author__ = "Thomas Fuhrmann", "Thomas Recouvreux"


from .mainengine import *


if __name__ == "__main__":
    eng = Engine()


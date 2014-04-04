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

class general(Frame):
    """ Frame qui regroupe les widgets du frame général.
    Hérite de Frame."""

    def __init__(self, fenetre, **kwargs):
        """
        @param fenetre : frame de la fenêtre principale
        """
        Frame.__init__(self, fenetre, width=300, height=700, bg="yellow")
        self.grid()
        self.mode()
        self.boutons()
        self.temps()
        self.team()
        self.nbrPts()

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
            bout.grid(column = n, row = 0)
        Fmode.grid(column = 0, row = 0, sticky=N+S+W+E, columnspan=2)

    def boutons(self):
        """
        Création des boutons start/stop/pause.
        """
        #! ajouter les traitements !
        Fbouton = LabelFrame(self, text="Bouton de contrôle", bg="blue")
        liste_button = ["Start", "Stop", "Pause"]
        for n in range(3):
             bout = Button(Fbouton, text = liste_button[n])
             bout.grid(column = n, row = 0)
        Fbouton.grid(column = 2, row = 0, sticky=N+S+W+E)

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
        secE = Label(Ftemps, text="00")
        secE.grid(column=0, row=1)
        secR = Label(Ftemps, text="90")
        secR.grid(column = 1, row = 1)
        Ftemps.grid(column = 0, row = 2, sticky=N+S)

    def team(self):
        """
        Permet d'afficher la team actuelle.
        """
        #! ajouter l'accès aux données de l'IA !
        Fteam = LabelFrame(self, text="Team", bg="white")
        labelfont = ('times', 20, 'bold')
        equipe = Label(Fteam, text="Blue", bg="blue")
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
        points = Label(Fpoints, text="00")
        points.config(font=labelfont, anchor=CENTER)
        points.grid(column=0, padx=35)
        Fpoints.grid(column = 2, row = 2, sticky=N+S)

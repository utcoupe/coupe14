
import xml.dom.minidom

import sys
import os
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR_PATH, "..", "define"))
sys.path.append(os.path.join(DIR_PATH, "..", "objects"))

from objects import *
from define import *

def load_map(filename,engine):
	
	ofi = open(filename, 'r')
	document = ofi.read()
	ofi.close()
	
	dom = xml.dom.minidom.parseString(document)

	for wall in dom.getElementsByTagName("wall"):
		engine.add(Wall(engine,mm_to_px(int(wall.getAttribute("x1")),int(wall.getAttribute("y1"))),mm_to_px(int(wall.getAttribute("x2")),int(wall.getAttribute("y2")))))
	for feu in dom.getElementsByTagName("feu"):
		engine.add(Feu(engine,mm_to_px(int(feu.getAttribute("x")),int(feu.getAttribute("y"))),feu.getAttribute("orientation"),feu.getAttribute("sens")))
	for arbre in dom.getElementsByTagName("arbre"):
		engine.add(Arbre(engine,mm_to_px(int(arbre.getAttribute("x")),int(arbre.getAttribute("y"))),arbre.getAttribute("orientation")))
	for torche in dom.getElementsByTagName("torche"):
		engine.add(Torche(engine,mm_to_px(int(torche.getAttribute("x")),int(torche.getAttribute("y")))))
	for fresque in dom.getElementsByTagName("fresque"):
		engine.add(Fresque(engine,mm_to_px(int(fresque.getAttribute("x")),int(fresque.getAttribute("y")))))
	for mammouth in dom.getElementsByTagName("mammouth"):
		engine.add(Mammouth(engine,mm_to_px(int(mammouth.getAttribute("x")),int(mammouth.getAttribute("y")))))
	for foyerCentre in dom.getElementsByTagName("foyerCentre"):
		engine.add(FoyerCentre(engine,mm_to_px(int(foyerCentre.getAttribute("x")),int(foyerCentre.getAttribute("y")))))
	for foyerBord in dom.getElementsByTagName("foyerBord"):
		engine.add(FoyerBord(engine,mm_to_px(int(foyerBord.getAttribute("x")),int(foyerBord.getAttribute("y"))),foyerBord.getAttribute("position")))
	for bac in dom.getElementsByTagName("bac"):
		engine.add(Bac(engine,mm_to_px(int(bac.getAttribute("x")),int(bac.getAttribute("y"))),bac.getAttribute("color")))

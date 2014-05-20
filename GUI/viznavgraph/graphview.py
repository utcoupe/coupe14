# -*- coding: utf-8 -*-


from view import *
import time
import threading


class GraphView(View):
	def __init__(self, graph, bots, bots_simu):
		View.__init__(self)

		self.self_bot = bots[0]
		self.dynamic_obstacle = bots[1]
		self.__liste_robots = bots #self_bot, other_bot, ennemy1, ennemy2
		self.__liste_robots_simu = bots_simu #color, big_us, mini_us, big_ennemy, mini_ennemy
		self.graph = graph

		self.p_depart = (200,200)
		self.p_arrive = (1500,1500)

		self.draw_polygons(graph.getPolygons())

		self.id_raw_path = None
		self.id_path = None
		
		## bindings
		self.canvas.bind('<Button-1>',self.onLeft)
		self.canvas.bind('<B1-Motion>',self.onLeft)
		self.canvas.bind('<Button-3>',self.onRight)
		self.canvas.bind('<B3-Motion>',self.onRight)
		self.canvas.bind('<Button-2>',self.onWheel)
		self.canvas.bind('<B2-Motion>',self.onWheel)

		self.bind_all('m', self.switchPathType)

		self.sum_calc_times = 0
		self.nb_calc_times = 0
		self.sum_update = 0
		self.nb_update = 0

		self.path_type = True  # True = smooth

		#thread de récupération des données robot
		threading.Thread(target=self.__pullDataRobots).start()

	def __pullDataRobots(self):
		"""
		Thread pour pull les données du robot
		"""
		while 1:
			self.__updateNavGraph()
			time.sleep(1)

	def switchPathType(self, args):
		self.path_type = not self.path_type
		print('Smooth_path status : ' + str(self.path_type))
		self.calc_path()
	
	def onLeft(self, event):
		"""
		Traitement à faire quand clique gauche souris
		Déplace le point d'arrivée du chemin à calculer
		"""
		event = self.event_to_x_y(event)
		print(event)
		self.p_arrive = event
		self.calc_path()

	def onRight(self, event):
		"""
		Traitement à faire quand clique droit souris
		Déplace le point de départ du chemin à calculer
		"""
		event = self.event_to_x_y(event)
		print(event)
		self.p_depart = event
		self.calc_path()

	def onWheel(self, event):
		"""
		Traitement à faire quand clique central (molette) souris
		Déplace notre deuxième robot, et actulise le navgraph
		"""
		event = self.event_to_x_y(event)
		print(event)
		
		start = time.time()
		self.dynamic_obstacle["setPosition"] = event
		self.graph.update(self.self_bot)
		difference = (time.time() - start)
		self.sum_update += difference
		self.nb_update += 1
		print("update graph time : %s (%s)" % (difference,self.sum_update / self.nb_update))

		self.__updateView()

	def event_to_x_y(self, event):
		"""
		Convertit la positon du curseur de la souris pour la rendre utilisation
		"""
		return (round(event.x / self.w_to_px), round((HEIGHT - event.y) / self.h_to_px))

	def calc_path(self):
		"""
		Calcule un nouveau chemin à partir du point de départ et d'arrivée.
		"""
		start = time.time()
		path = self.graph.getPath(self.p_depart,self.p_arrive, self.path_type)
		difference = (time.time() - start)
		self.sum_calc_times += difference
		self.nb_calc_times += 1
		print("pathfinding computing time : %s (moy=%s)" % (difference,self.sum_calc_times/self.nb_calc_times))
		print("path : "+str(path))

		self.show_result_calc_path(path)
		print("Longueur : " + str(path.getDist()))
		
		return path

	def show_result_calc_path(self, path):
		"""
		Affiche un chemin
		"""
		self.remove(self.id_path)
		if self.path_type:  #smooth
			color = 'red'
		else:
			color = 'blue'
		if path:
			self.id_path = self.draw_line(path, color)

	def __updateView(self):
		"""
		Met à jour l'affichage du graph navigation (les polygones)
		"""
		self.remove()
		self.draw_polygons(self.graph.getPolygons())
		#self.calc_path()

	def __updateNavGraph(self):
		"""
		Met à jour le graph de navigation en récupérant la position des robots dans le simulateur
		"""
		#on actualise la position de tous les robots:
		#big_us
		self.__liste_robots[0]["getPosition"] = self.__liste_robots_simu[1].getPositionXY()
		#mini_us
		self.__liste_robots[1]["getPosition"] = self.__liste_robots_simu[2].getPositionXY()
		#big_ennemy
		self.__liste_robots[2]["getPosition"] = self.__liste_robots_simu[3].getPositionXY()
		#mini_ennemy
		self.__liste_robots[3]["getPosition"] = self.__liste_robots_simu[4].getPositionXY()
		#actualisation du graph
		self.graph.update(self.self_bot)
		#on dessine
		self.__updateView()
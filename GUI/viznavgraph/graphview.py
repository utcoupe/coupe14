# -*- coding: utf-8 -*-


from view import *
import time


class GraphView(View):
	def __init__(self, graph, dynamic_obstacle, self_bot):
		View.__init__(self)

		self.self_bot = self_bot
		self.dynamic_obstacle = dynamic_obstacle
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

	def switchPathType(self, args):
		self.path_type = not self.path_type
		print('Smooth_path status : ' + str(self.path_type))
		self.calc_path()
	
	def onLeft(self, event):
		event = self.event_to_x_y(event)
		print(event)
		self.p_arrive = event
		self.calc_path()

	def onRight(self, event):
		event = self.event_to_x_y(event)
		print(event)
		self.p_depart = event
		self.calc_path()

	def onWheel(self, event):
		event = self.event_to_x_y(event)
		print(event)
		
		start = time.time()
		self.dynamic_obstacle.setPosition(event)
		self.graph.update(self.self_bot)
		difference = (time.time() - start)
		self.sum_update += difference
		self.nb_update += 1
		print("update graph time : %s (%s)" % (difference,self.sum_update / self.nb_update))
		
		self.remove()
		self.draw_polygons(self.graph.getPolygons())
		self.calc_path()

	def event_to_x_y(self, event):
		return (round(event.x / self.w_to_px), round((HEIGHT - event.y) / self.h_to_px))

	def calc_path(self):
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
		self.remove(self.id_path)
		if self.path_type:  #smooth
			color = 'red'
		else:
			color = 'blue'
		if path:
			self.id_path = self.draw_line(path, color)

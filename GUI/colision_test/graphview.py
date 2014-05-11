# -*- coding: utf-8 -*-


from view import *
import time


class GraphView(View):
	def __init__(self, graph, col, dynamic_obstacle, self_bot):
		View.__init__(self)

		self.self_bot = self_bot
		self.dynamic_obstacle = dynamic_obstacle
		self.graph = graph
		self.graph.update(self.self_bot)
		self.col = col

		self.p_depart = (200,200)
		self.p_arrive = (1500,1500)

		self.draw_polygons(graph.getPolygons())

		self.id_smooth_path = None
		
		## bindings
		self.canvas.bind('<Button-1>',self.onLeft)
		self.canvas.bind('<B1-Motion>',self.onLeft)
		self.canvas.bind('<Button-3>',self.onRight)
		self.canvas.bind('<B3-Motion>',self.onRight)
		self.canvas.bind('<Button-2>',self.onWheel)
		self.canvas.bind('<B2-Motion>',self.onWheel)

		self.sum_calc_times = 0
		self.nb_calc_times = 0
		self.sum_update = 0
		self.nb_update = 0
	
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
		
		self.dynamic_obstacle["getPosition"] = event
		self.graph.update(self.self_bot)
		self.remove()

		self.draw_polygons(self.graph.getPolygons())
		self.show_result_calc_path(self.smooth_path)
		start = time.time()
		couple = self.col.getCollision(self.self_bot)
		print("Duree de calcul de collision : %s ms" % ((time.time() - start)*1000))
		if couple is not None:
			print("Collision id=%s, dist=%s" % (couple[0], couple[1]))

	def event_to_x_y(self, event):
		return (round(event.x / self.w_to_px), round((HEIGHT - event.y) / self.h_to_px))

	def calc_path(self):
		start = time.time()
		smooth_path = self.graph.getPath(self.p_depart,self.p_arrive)
		self.smooth_path = smooth_path
		difference = (time.time() - start)
		self.sum_calc_times += difference
		self.nb_calc_times += 1
		print("pathfinding computing time : %s (moy=%s)" % (difference,self.sum_calc_times/self.nb_calc_times))
		print("path : "+str(smooth_path))
		self.self_bot.traj = [[42, smooth_path]]

		self.show_result_calc_path(smooth_path)
		print("Longueur : " + str(smooth_path.getDist()))
		
		return smooth_path

	def show_result_calc_path(self, smooth_path):
		self.remove(self.id_smooth_path)
		if smooth_path:
			self.id_smooth_path = self.draw_line(smooth_path, 'blue')

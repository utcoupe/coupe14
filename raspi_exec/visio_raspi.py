# -*- coding: utf-8 -*-
import os
import sys
import time

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(FILE_DIR, "../ia/"))

import event.goals.visio as visio


class Tourelle:
	def __init__(self):
		self.isATourelle = True

	def getPosition(self):
		return (0, 0)

	def getPositionAndAngle(self):
		return (0, 0, 0)


def compute(v):
	triangles = v.update()
	return triangles


def send(triangles, pipe):
	for tri in triangles:
		print(tri)
	print()

if __name__ == '__main__':
	try:
		path_pipe = sys.argv[1]
		color = sys.argv[2]
	except:
		print('Not enough arguments : visio_raspi path_pipe color')
		exit()

	path_to_exec = "../supervisio/visio"
	config_path = "../config/visio/visio_tourelle" + color + "/"

	print("Executing the visio program at", path_to_exec)
	print("\tFirst with config at", config_path, "on port video0")
	try:
		tourelle = Tourelle()
		v = visio.Visio(path_to_exec, 0, config_path, tourelle, True)
	except BaseException as e:
		print("Failed to open visio programs : "+str(e))
		exit()

	print("Done, attempting to open fifo")
	try:
		pipe = open(path_pipe, "w+")
	except BaseException as e:
		print("Failed to open pipe : "+str(e))
		exit()
	print("Fifo opened")

	while(1):
		start = time.time()
		triangles = []
		try:
			triangles = compute(v)
			send(triangles, pipe)
		except BaseException as e:
			print("Failed to compute and send triangles :", str(e))
			triangles = []

		print("Detected", len(triangles), "in", (time.time() - start), "seconds")




# -*- coding: utf-8 -*-
import os
import sys
import time
import errno

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
		path = sys.argv[1]
		color = sys.argv[2]
	except:
		print('Not enough arguments : visio_raspi path_pipe color')
		sys.exit()
	try:
		index = int(sys.argv[3])
	except:
		index = 0

	path_to_exec = path+"/supervisio/visio"
	path_pipe = path+"/config/raspi/pipe_cameras"
	config_path = path+"/config/visio/visio_tourelle_" + color + "/"

	print("Executing visio with config at", config_path, "on port video"+str(index))
	try:
		tourelle = Tourelle()
		v = visio.Visio(path_to_exec, index, config_path, tourelle, True)
	except BaseException as e:
		print("Failed to open visio programs : "+str(e))
		sys.exit()

	print("Done")
	print("[CAM ]  Attempting to open fifo at",path_pipe)
	try:
		pipe = open(path_pipe, "w")
	except BaseException as e:
		print("Failed to open pipe : "+str(e))
		sys.exit()
	print("Fifo opened")

	conti = True
	while(conti):
		start = time.time()
		triangles = []
		try:
			triangles = compute(v)
			send(triangles, pipe)
			print("Detected", len(triangles), "in", (time.time() - start), "seconds")
		except BaseException as e:
			conti = False
			print("Failed to compute and send triangles :", str(e))

			triangles = []

	print('Closing')
	v.close()
	sys.exit()

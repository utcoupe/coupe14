from xml.etree import ElementTree as ET
import os
import sys

class Gpio:
	def __init__(self):
		self.__parsePorts()
		self.initJackPort(1)
		self.initColorSelectPort(2)

	def initJackPort(self, port):
		self.jackPort = self.ports[str(port)]
		os.system('echo in > ' + self.jackPort)

	def initColorSelectPort(self, port):
		self.colorSelectPort = self.ports[str(port)]
		os.system('echo in > ' + self.colorSelectPort)

	def getJack(self):
		"""Returns electrical level on jack port"""
		f = open(self.jackPort)
		status = f.readline()[0]
		return status

	def getColor(self):
		"""HIGH = YELLOW ; LOW = RED"""
		f = open(self.colorSelectPort)
		status = f.readline()[0]
		if status == '1':
			return 'YELLOW'
		if status == '0':
			return 'RED'

	def __parsePorts(self, path='ports.xml'):
		path = os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/" +path)
		self.ports = {}
		table = ET.parse(path).getroot()
		for port_el in table:
			self.ports[port_el[0].text] = port_el[2].text

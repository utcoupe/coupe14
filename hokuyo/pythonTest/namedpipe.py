import tempfile
import os

#handle, filename = tempfile.mkstemp()
filename = "/tmp/lidarPipe"

os.remove(filename)
os.mkfifo(filename)

print("Opening fifo, waiting for c program...")
reader = open(filename, 'r') 
print("Fifo connected !")

line = reader.readline()
while line != None :
	print(line, end="")
	line = reader.readline()

print("Fifo disconnected !")




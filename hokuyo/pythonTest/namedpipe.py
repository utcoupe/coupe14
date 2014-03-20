import tempfile
import os

#handle, filename = tempfile.mkstemp()
filename = "/tmp/lidarPipe"

try:
    os.remove(filename)
except OSError:
    pass
os.mkfifo(filename)

print("Opening fifo, waiting for c program...")
reader = open(filename, 'r') 
print("Fifo connected !")

line = reader.readline()
while line is not None:
	print(line, end="")
	line = reader.readline()

print("Fifo disconnected !")




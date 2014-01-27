import os

class Lidar:
    def __init__(self, debug=True):
        self._debug = debug
        filename = "/tmp/lidarPipe"

        try:
            os.remove(filename)
        except OSError:
            pass
        os.mkfifo(filename)

        print("Opening fifo, waiting for c program...")
        pipe = os.open(filename, os.O_RDONLY|os.O_NONBLOCK)
        self._reader = os.fdopen(pipe) 

        firstread = self._reader.readline()
        while firstread == "" :
            firstread = self._reader.readline()


        if firstread == "Hi!\n" :
            print("FIFO connected !")
        else :
            raise("FIFO error")

    def poll(self):
        r = self._reader.readline()
        if r == "":
            return None
        return list([list([int(f) for f in e.split(":")]) for e in r[:-1].split(";")[1:]])



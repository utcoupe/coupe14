import os
import sys
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(FILE_DIR,"../../../libs"))
sys.path.append(os.path.join(FILE_DIR,"../../"))

from .pathfinding import *

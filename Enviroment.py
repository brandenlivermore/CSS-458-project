import numpy as np

class Enviroment(object):
    width = 0
    height = 0
    grid = None

    def __init__(self, in_width, in_height):
        self.height = in_height
        self.width = in_width
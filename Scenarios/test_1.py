##################################################################
#                       TEST ONE
##################################################################
#Conditions: 10x10 grid, all teff max, teff does not grow,
#            deer eat teff, uniformly distributed 1000 deer
#
#Expectations: teff will be consumed until it is eliminated
#               deer will starve and die
#               two predictable extinction events

from environment import Environment
from tile import Tile
from Agents.teff import Teff
from Agents.animal import Deer
import numpy as np

def run_test_1():
    out = Environment(10,10)
    for x in range(10):
        for y in range(10):
            out.grid[x,y].add_agent(Teff())
            for w in range(10):
                out.grid[x,y].add_agent(Deer(out.grid[x,y]))


    Teff.updates = False


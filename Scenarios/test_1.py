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
from driver import Driver
from weathermodel import WeatherModel

def run_test_1():

    Teff.threshold_acre = 1000
    Teff.updates = False

    environment = Environment(10,10)
    for x in range(10):
        for y in range(10):
            environment.grid[x,y].add_agent(Teff(environment.grid[x,y]))
            for w in range(10):
                environment.grid[x,y].add_agent(Deer(environment.grid[x,y]))


    driver = Driver()
    weather = WeatherModel(numYears=1)
    driver.runSimulation([(weather, environment)])

    

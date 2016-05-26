from src.Agents.teff import Teff
from src.weathermodel import WeatherModel

from src.Agents.animal import Deer
from src.environment import Environment
import importlib

description = 'Uniformly distributed teff, 10 deer per tile, 10x10 grid. Pretty boring. '

def setup():
    Teff.threshold_acre = 10000
    Teff.updates = False

    environment = Environment(10,10)

    for x in range(10):
        for y in range(10):
            environment.grid[x,y].add_agent(Teff(environment.grid[x,y]))
            for w in range(10):
                environment.grid[x,y].add_agent(Deer(environment.grid[x,y]))


    weather = WeatherModel(numYears=1)

    return [(weather, environment)]

def display_results(results):
    Teff.updates = True
    Teff.threshold_acre = 177

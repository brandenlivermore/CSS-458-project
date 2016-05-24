
##################################################################
#                       TEST ONE
##################################################################
#Conditions: 10x10 grid, all teff max, teff does not grow,
#            deer eat teff, uniformly distributed 1000 deer
#
#Expectations: teff will be consumed until it is eliminated
#               deer will starve and die
#               two predictable extinction events

from src.Agents.teff import Teff
from src.weathermodel import WeatherModel

from src.Agents.animal import Deer
from src.environment import Environment


class Scenario(object):


    def __init__(self):
        self.weather = WeatherModel(numYears=1)
        self.environment = Environment(10,10)


    def run_test_1(self):

        Teff.threshold_acre = 10000
        Teff.updates = False

        self.environment = Environment(10,10)
        for x in range(10):
            for y in range(10):
                self.environment.grid[x,y].add_agent(Teff(self.environment.grid[x,y]))
                for w in range(10):
                    self.environment.grid[x,y].add_agent(Deer(self.environment.grid[x,y]))


        self.weather = WeatherModel(numYears=1)

    def run_test_2(self):
        pass

    def run_test_3(self):
        pass

    def run_test_4(self):
        pass

    def run_test_5(self):
        pass
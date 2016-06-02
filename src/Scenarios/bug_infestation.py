import src.utility

from src.Agents.teff import Teff
from src.weathermodel import WeatherModel

from src.Agents.animal import Deer
from src.environment import Environment
from src.Agents.drinking_water import DrinkingWater
import matplotlib.pyplot as plt
import src.Agents.bugs
import numpy as N

description = 'Uniform teff, bug infestation!'

def setup():

    size = 5
    runs = 5

    simulations = []
    for i in range(runs):
        environment = Environment(size,size)
        for x in range(size):
            for y in range(size):
                environment.grid[x,y].add_agent(Teff(environment.grid[x,y]))
                for w in range(y % 2 + 3):
                    environment.grid[x,y].add_agent(Deer(environment.grid[x,y]))

        randX = N.random.randint(0, size)
        randY = N.random.randint(0, size)

        environment.grid[randX, randY].add_agent(src.Agents.bugs.Bugs(environment.grid[randX, randY]))

        weather = WeatherModel(numYears=17)
        simulations.append((weather, environment))




    return simulations

def display_results(results):
    results = src.utility.remove_bad_simulations([Deer, Teff, DrinkingWater, src.Agents.bugs.Bugs], results)
    average_returns_deer = src.utility.average_returns(results, Deer)[0]
    average_returns_teff = src.utility.average_returns(results, Teff)[1]
    average_returns_bugs = src.utility.average_returns(results, src.Agents.bugs.Bugs)[1]
    average_returns_drinking_water = src.utility.average_returns(results, DrinkingWater)[1]

    days = N.arange(365 * 17)

    plt.subplot(4, 1, 1)
    plt.plot(days, average_returns_deer)
    plt.xlabel('Day')
    plt.ylabel('Deer count')
    plt.title('Deer count by day')

    plt.subplot(4, 1, 2)
    plt.plot(days, average_returns_teff)
    plt.xlabel('Day')
    plt.ylabel('Thousands of pounds of teff')
    plt.title('Teff weight by day')

    plt.subplot(4, 1, 3)
    plt.plot(days, average_returns_bugs)
    plt.xlabel('Day')
    plt.ylabel('Bug count')
    plt.title('Bug count by day')

    plt.subplot(4, 1, 4)
    plt.plot(days, average_returns_drinking_water)
    plt.xlabel('Day')
    plt.ylabel('1000s of gal of water')
    plt.title('Drinking water by day')


    plt.show()
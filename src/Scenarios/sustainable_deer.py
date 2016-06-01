from src.Agents.teff import Teff
from src.weathermodel import WeatherModel

from src.Agents.animal import Deer
from src.environment import Environment
from src.Agents.ground_water import GroundWater
import matplotlib.pyplot as plt
import numpy as N

weather = None

description = 'Randomly distributed teff, 2 deer per tile, 30x30 grid.'

def setup():

    size = 10
    environment = Environment(size,size)
    for x in range(size):
        for y in range(size):
            environment.grid[x,y].add_agent(Teff(environment.grid[x,y]))
            for w in range(3):
                environment.grid[x,y].add_agent(Deer(environment.grid[x,y]))

    global weather
    weather = WeatherModel(numYears=3)
    return [(weather, environment)]

def display_results(results):
    results = results[0]

    days = N.arange(365 * 3)
    deer_count = [day[Deer][0] for day in results]
    print(deer_count)
    teff_count = [day[Teff][1] for day in results]
    ground_water_mass = [day[GroundWater][1] for day in results]
    print(teff_count)

    plt.subplot(3, 1, 1)
    plt.plot(days, deer_count)
    plt.xlabel('Day')
    plt.ylabel('Deer count')
    plt.title('Deer count by day')

    plt.subplot(3, 1, 2)
    plt.plot(days, teff_count)
    plt.xlabel('Day')
    plt.ylabel('Thousands of pounds of teff')
    plt.title('Teff weight by day')

    plt.subplot(3, 1, 3)
    plt.plot(days, ground_water_mass)
    plt.xlabel('Day')
    plt.ylabel('Thousands of gallons of ground water')
    plt.title('Ground water mass by day')


    plt.tight_layout()

    plt.show()
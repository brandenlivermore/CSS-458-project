
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
from src.Agents.drinking_water import DrinkingWater
import matplotlib.pyplot as plt
import numpy as N

weather = None

description = 'Uniformly distributed teff, 10 deer per tile, 30x30 grid.'

def setup():

    # Teff.threshold_acre = 10000
    # Teff.updates = False
    size = 5
    environment = Environment(size,size)
    for x in range(size):
        for y in range(size):
            environment.grid[x,y].add_agent(Teff(environment.grid[x,y]))
            for w in range(y % 3 + 1):
                environment.grid[x,y].add_agent(Deer(environment.grid[x,y]))

    global weather
    weather = WeatherModel(numYears=14)
    return [(weather, environment)]

def display_results(results):
    results = results[0]
    Teff.threshold_acre = 177
    Teff.updates = True

    days = N.arange(365 * 14)
    deer_count = [day[Deer][0] for day in results]
    print(deer_count)
    teff_count = [day[Teff][1] for day in results]
    ground_water_mass = [day[DrinkingWater][1] for day in results]
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


    #plt.tight_layout()
    #

    plt.show()
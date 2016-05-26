import src.environment
import src.Agents.teff
from src.weathermodel import WeatherModel
import numpy as N
import matplotlib.pyplot as plt

weather = None

description = 'Teff starts in the center, shows how teff spreads over time. '

def setup():
    size = 20

    environment = src.environment.Environment(size, size)

    environment.grid[int(size / 2.), int(size / 2.)].add_agent \
        (src.Agents.teff.Teff(environment.grid[int(size / 2.), int(size / 2.)]))

    global weather

    weather = WeatherModel(numYears=1)
    return [(weather, environment)]

def display_results(results):
    results = results[0]

    days = N.arange(365)

    teff_count = [day[src.Agents.teff.Teff][1] for day in results]
    teff_agent_count = [day[src.Agents.teff.Teff][0] for day in results]



    plt.subplot(2, 1, 1)
    plt.plot(days, teff_count)
    plt.xlabel('Day of the year')
    plt.ylabel('Teff weight (thousands of pounds)')
    plt.title('Teff weight by day')

    plt.subplot(2, 1, 2)
    plt.plot(days, teff_agent_count)
    plt.xlabel('Day of the year')
    plt.ylabel('Teff agent count')
    plt.title('Teff count by day')


    plt.show()


    #plt.plot(days, )

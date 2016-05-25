import src.environment
import src.Agents.teff
from weathermodel import WeatherModel
import numpy as N
import matplotlib.pyplot as plt

weather = None

description = 'Teff starts in the center, shows how teff spreads over time. '

def setup():
    size = 20

    environment = src.environment.Environment(size, size)

    environment.grid[size / 2, size / 2].add_agent \
        (src.Agents.teff.Teff(environment.grid[size / 2, size / 2]))

    global weather

    weather = WeatherModel(numYears=1)
    return [(weather, environment)]

def display_results(results):
    results = results[0]

    days = N.arange(365)

    teff_count = [day[src.Agents.teff.Teff][1] for day in results]

    plt.plot(days, teff_count)
    plt.xlabel('Day of the year')
    plt.ylabel('Teff weight (thousands of pounds)')
    plt.title('Teff weight by day')
    plt.show()


    #plt.plot(days, )

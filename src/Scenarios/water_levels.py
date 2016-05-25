import matplotlib.pyplot as plt
import src.environment
from src.weathermodel import WeatherModel
import numpy as N
from src.Agents.drinking_water import DrinkingWater
from src.Agents.ground_water import GroundWater


description = 'Teff starts in the center, shows how water volume increases over time. '

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

    ground_water = [day[GroundWater][1] for day in results]
    drinking_water = [day[DrinkingWater][1] for day in results]

    plt.subplot(2, 1, 1)
    plt.plot(days, ground_water)
    plt.xlabel('Day of the year')
    plt.ylabel('Ground water volume (thousands of gallons)')
    plt.title('Ground water volume by day')

    plt.subplot(2, 1, 2)
    plt.plot(days, drinking_water)
    plt.xlabel('Day of the year')
    plt.ylabel('Drinking water volume (thousands of gallons)')
    plt.title('Drinking water volume by day')


    plt.show()


    #plt.plot(days, )

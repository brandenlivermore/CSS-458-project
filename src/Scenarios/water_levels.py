import src.environment
from src.weathermodel import WeatherModel
import numpy as N
from src.Agents.drinking_water import DrinkingWater
from src.Agents.ground_water import GroundWater
from src.Agents.soil import Soil
import src.grapher


description = 'Teff starts in the center, shows how water volume increases over time. '

def setup():
    size = 100

    environment = src.environment.Environment(size, size)

    environment.grid[int(size / 2.), int(size / 2.)].add_agent \
        (src.Agents.teff.Teff(environment.grid[int(size / 2.), int(size / 2.)]))

    global weather

    weather = WeatherModel(numYears=1)
    return [(weather, environment)]

def display_results(results):
    results = results[0]

    days = N.arange(365)

    graphs = []

    ground_water = [day[GroundWater][1] for day in results]
    drinking_water = [day[DrinkingWater][1] for day in results]
    soil = [day[Soil][1] for day in results]

    graphs.append((days, ground_water, 'Day of the year', \
                   'volume (1000s of gallons)', \
                   'Ground water volume by day'))

    graphs.append((days, drinking_water, 'Day of the year', \
                   'volume (1000s of gallons)', \
                   'Drinking water volume by day'))

    graphs.append((days, soil, 'Day of the year', \
                   'volume (1000s of gallons)', \
                   'Soil retained water volume by day'))


    src.grapher.display_graph(graphs)
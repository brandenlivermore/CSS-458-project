import src.environment
from src.weathermodel import WeatherModel
import numpy as N
from src.Agents.drinking_water import DrinkingWater
from src.Agents.ground_water import GroundWater
from src.Agents.soil import Soil
import src.grapher


description = 'Teff starts in the center, shows how water volume increases over time. '

def setup():
    size = 10

    environment = src.environment.Environment(size, size)

    environment.grid[int(size / 2.), int(size / 2.)].add_agent \
        (src.Agents.teff.Teff(environment.grid[int(size / 2.), int(size / 2.)]))

    #Test setting wells to 100% percent chance
    environment.chance_well = 1

    global weather

    weather = WeatherModel(numYears=5)
    return [(weather, environment)]

def display_results(results):
    results = results[0]

    days = N.arange(1825)

    graphs = []
    drinking_water = []

    ground_water = [day[GroundWater][1] for day in results]
    for day in results:
        if DrinkingWater in day:
            drinking_water.append(day[DrinkingWater][1])
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
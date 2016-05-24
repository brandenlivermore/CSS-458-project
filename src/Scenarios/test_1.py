
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
from driver import Driver
from weathermodel import WeatherModel

from src.Agents.animal import Deer
from src.environment import Environment


def run_test_1():

    Teff.threshold_acre = 1000
    Teff.updates = False

    environment = Environment(20,20)
    for x in range(10):
        for y in range(10):
            environment.grid[x,y].add_agent(Teff(environment.grid[x,y]))
            for w in range(10):
                environment.grid[x,y].add_agent(Deer(environment.grid[x,y]))

    driver = Driver()
    weather = WeatherModel(numYears=1)
    result = driver.runSimulation([(weather, environment)])[0]
    for i in range(len(result)):
        day_dict = result[i]
        print("new day!!!")

        day = weather.days[i]

        print("day: " + str(day.day) + " rain: " + str(day.rain) \
              + " sun: " + str(day.sun) + " temp: " + str(day.temp))
        for key in day_dict:
            print("Agent type: " + str(key) + ", count: " + str(day_dict[key][0]) + ", weight: " + str(day_dict[key][1]) + " thousand pounds")

        print("Day end!!! \n\n\n\n\n")
    
run_test_1()
import matplotlib.pyplot as plt
import numpy as N
from src.weathermodel import WeatherModel
from src.Agents.animal import Deer
from src.Agents.teff import Teff
from src.Agents.drinking_water import DrinkingWater
from src.Agents.ground_water import GroundWater
from src.Agents.soil import Soil
from src.Agents.animal import Wolf
import os
import importlib.util

class Driver(object):
    """
    Driver class for simulation
    """

    weatherModel = WeatherModel(3)

    def __init__(self):
        """
        Initialize the simulation driver
        """
        self.daily_totals = []

    def import_module(self, file_name):
        file_name = file_name[:-3]
        return importlib.import_module("src.Scenarios." + file_name)


    def get_scenario_names_and_descriptions_and_modules(self):
        names_and_descriptions_and_modules = []
        for file in os.listdir("./src/Scenarios"):
            if file.endswith(".py"):
                module = self.import_module(file)
                names_and_descriptions_and_modules.append((file, module.description, module))

        return names_and_descriptions_and_modules
    def get_descriptions_string(self, names_descriptions):


        descriptions_string = "Enter the number of the simulation you'd like to run, or type -1 to quit. \n"

        scenario_number = 1

        for name_description_pair in names_descriptions:
            descriptions_string += str(scenario_number) + ". " + name_description_pair[0] + ": " + name_description_pair[1] + "\n"
            scenario_number += 1

        return descriptions_string

    def run(self):
        scenario_number = None
        scenario_information = self.get_scenario_names_and_descriptions_and_modules()

        descriptions_string = self.get_descriptions_string(scenario_information)
        while (True):
            print(descriptions_string)
            scenario_number = input()

            try:
                scenario_number = int(scenario_number)
            except ValueError:
                print("That is not a number. ")
                scenario_number = -1

            if scenario_number == -1:
                print("Bye. ")
                return
            elif scenario_number < 1 or scenario_number > len(scenario_information):
                print("Invalid index. ")
                continue

            # Get the correct scenario module
            module = scenario_information[scenario_number - 1][2]

            # Tell the module to setup the environment and array of days
            info = module.setup()

            # Run the scenario
            scenario_results = self.run_scenario(info)

            # Pass the results to the scenario for display
            module.display_results(scenario_results)

            self.daily_totals = scenario_results[0]

            self.visualizeWeather()
            self.visualizeEnvironmentTotals()

    def run_scenario(self, tuple_list):
        '''

        :param tuple_list: A list of tuples, with corresponding weather model and environment objects
            Calls the update method on the environment for each day of the simulation.
            The weather object's day properties are passed into the environment update method
            tupleList[0] is weather objects
            tupleList[1] is environment objects
        :return: daily_totals
        '''


        for current_tuple in tuple_list:
            weather_model = current_tuple[0]
            environment = current_tuple[1]
            run_output = []
            for day in weather_model.days:
                print(day.day)
                run_output.append(environment.update(day))

            self.daily_totals.append(run_output)


        return self.daily_totals
        ##########################################################################################

    def visualizeEnvironmentTotals(self):
        days = N.arange(365)
        deer_count = [day[Deer][0] for day in self.daily_totals]
        teff_count = [day[Teff][1] for day in self.daily_totals]

        plt.subplot(2, 1, 1)
        plt.plot(days, deer_count)
        plt.xlabel('Day')
        plt.ylabel('Deer count')
        plt.title('Deer count by day')

        plt.subplot(2, 1, 2)
        plt.plot(days, teff_count)
        plt.xlabel('Day')
        plt.ylabel('Thousands of pounds of teff')
        plt.title('Teff weight by day')

        plt.tight_layout()

        plt.show()

    def visualizeWeather(self):
        """

        Returns
        -------
        No return

        """
        dayArray = N.arange(0, self.weatherModel.totalDays)
        temp = [x.temp for x in self.weatherModel.days]
        sun = [x.sun for x in self.weatherModel.days]
        rain = [x.rain for x in self.weatherModel.days]
        print(rain)
        plt.subplot(3, 1, 1)
        plt.plot(dayArray, temp)
        plt.axis([0, self.weatherModel.totalDays, 0, 90])
        plt.xlabel('Day')
        plt.ylabel('Temperature (F)')
        plt.title('Daily Temp')

        plt.subplot(3, 1, 2)
        plt.plot(dayArray, sun)
        plt.axis([0, self.weatherModel.totalDays, 0, 24])
        plt.xlabel('Day')
        plt.ylabel('Sunlight (hours)')
        plt.title('Daily Sun')

        plt.subplot(3, 1, 3)
        plt.plot(dayArray, rain)
        plt.axis([0, self.weatherModel.totalDays, 0, 1])
        plt.xlabel('Day')
        plt.ylabel('Precipitation (inches)')
        plt.title('Daily Precipitation')

        plt.tight_layout()
        plt.show()


d = Driver()
d.run()
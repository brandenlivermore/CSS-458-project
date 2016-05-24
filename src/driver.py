import matplotlib.pyplot as plt
import numpy as N
from src.weathermodel import WeatherModel
from src.Scenarios.scenario import Scenario
from src.Agents.animal import Deer
from src.Agents.teff import Teff
from src.Agents.drinking_water import DrinkingWater
from src.Agents.ground_water import GroundWater
from src.Agents.soil import Soil
from src.Agents.animal import Wolf

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

    def run(self):
        scenarioNumber = 0
        numScenarios = 5
        while (scenarioNumber != -1):
            scenarioNumber = input("Enter a number for the simulation you would like to run: \n" \
                               "1. Only Deer and Teff. Teff does not grow \n" \
                               "2. .... \n" \
                               "3. .... \n" \
                               "4. .... \n" \
                               "5. .... \n" \
                               "-1 to quit \n")
            try:
                scenarioNumber = int(scenarioNumber)
            except ValueError:
                scenarioNumber = 0

            if (scenarioNumber > 0 and scenarioNumber <= numScenarios):
                print("Running scenario " + str(scenarioNumber) + "\n")
                s = Scenario()
                if (scenarioNumber == 1):
                    s.run_test_1()
                elif (scenarioNumber == 2):
                    s.run_test_2()
                elif(scenarioNumber == 3):
                    s.run_test_3()
                elif(scenarioNumber == 4):
                    s.run_test_4()
                elif(scenarioNumber == 5):
                    s.run_test_5()
                self.daily_totals = self.runScenario([(s.weather, s.environment)])[0]
            elif (scenarioNumber == -1):
                print("Thank you for running our simulation")
                return
            else:
                print("Please enter a number between 1 and " + str(numScenarios) + "\n")

            self.visualizeWeather()
            self.visualizeEnvironmentTotals()

    def runScenario(self, tuple_list):
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
        print(deer_count)
        teff_count = [day[Teff][1] for day in self.daily_totals]
        print(teff_count)

        plt.subplot(2, 1, 1)
        plt.plot(days, deer_count)
        plt.xlabel('Day')
        plt.ylabel('Deer count')
        plt.axis([0, len(days), -10, 1200])
        plt.title('Deer count by day')

        plt.subplot(2, 1, 2)
        plt.plot(days, teff_count)
        plt.xlabel('Day')
        plt.ylabel('Thousands of pounds of teff')
        plt.axis([0, len(days), -10, 1200])
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
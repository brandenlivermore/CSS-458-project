from weathermodel import WeatherModel
from environment import Environment
import matplotlib.pyplot as plt
import numpy as N

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



    def runSimulation(self, tuple_list):
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
                run_output.append(environment.update(day))

            self.daily_totals.append(run_output)


        return self.daily_totals
        ##########################################################################################

    def visualizeEnvironmentTotals(self):
        pass

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
d.visualizeWeather()
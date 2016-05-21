from weathermodel import WeatherModel
# from environment import Environment
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
        pass


    def runSimulation(self, tupleList):
        """
        Parameters
        ----------
        tupleList
            A list of tuples, with corresponding weather model and environment objects
            Calls the update method on the environment for each day of the simulation.
            The weather object's day properties are passed into the environment update method
        """
        for i in range(0, len(tupleList)):
            weather, environ = tupleList[i]
            for day in range(0, len(weather.days)):
                # TODO: use the return value from environment update method to store the data
                environ.update(weather[day])

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
        plt.plot(dayArray, temp)
        plt.axis([0, self.weatherModel.totalDays, 0, 90])
        plt.xlabel('Day')
        plt.ylabel('Temperature (F)')
        plt.title('Daily Temp')
        plt.show()

        plt.plot(dayArray, sun)
        plt.axis([0, self.weatherModel.totalDays, 0, 24])
        plt.xlabel('Day')
        plt.ylabel('Sunlight (hours)')
        plt.title('Daily Sun')
        plt.show()

        plt.plot(dayArray, rain)
        plt.axis([0, self.weatherModel.totalDays, 0, 1])
        plt.xlabel('Day')
        plt.ylabel('Precipitation (inches)')
        plt.title('Daily Precipitation')
        plt.show()


d = Driver()
d.visualizeWeather()
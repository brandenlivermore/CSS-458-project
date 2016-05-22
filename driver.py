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
        self.agent_totals = {}
        for agent in len(self.agent_types):
            self.agent_totals[agent] = [0,0]
        pass


    def runSimulation(self, tupleList):
        """
        Parameters
        ----------
        tupleList
            A list of tuples, with corresponding weather model and environment objects
            Calls the update method on the environment for each day of the simulation.
            The weather object's day properties are passed into the environment update method

            tupleList[0] is weather objects
            tupleList[1] is environment objects
        """

        ##########################################################################################
        #The code between these two blocks may not work correctly
        # Trying to create 2D array with number of columns equal to tupleList length where
        # the length of each row is the number of days in each simulation

        a = [x[0] for x in tupleList]  # a is list of weather objects from tupleList
        daysPerSimulation = [x.totalDays for x in a] # daysPerSimulation is a list of the length of each simulation
        numSimulations = len(tupleList) # the number of different simulations to be run
        data = [] #List to hold all data from all simulations
        for i in range(numSimulations):
            length = daysPerSimulation[i]
            data.append([0] * length)

        for i in range(0, len(tupleList)):
            weather, environ = tupleList[i]
            for day in range(0, len(weather.days)):
                data[i, day] = environ.update(weather[day])
        ##########################################################################################


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
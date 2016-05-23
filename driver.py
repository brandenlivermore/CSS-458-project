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
        self.daily_totals = []



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
        #The code between these two blocks does not work yet
        # Trying to create 2D array with number of columns equal to tupleList length where
        # the length of each row is the number of days in each simulation

        #######
        # Using the logic from this code:

        # listOfData = []
        # numSimulations = 6
        # daysPerSimulation = range(numSimulations)
        # daysPerSimulation = [x + 1 for x in daysPerSimulation]
        # for i in range(numSimulations):
        #     length = daysPerSimulation[i]
        #     data = [([0] * length)]
        #     listOfData.append(data)
        #
        # for row in listOfData:
        #     print(row)

        #######
        a = [x[0] for x in tupleList]  # a is list of weather objects from tupleList
        daysPerSimulation = [x.totalDays for x in a] # daysPerSimulation is a list of the length of each simulation
        numSimulations = len(tupleList) # the number of different simulations to be run
        listOfData = []
        data = [] #List to hold all data from all simulations
        for i in range(numSimulations):
            length = daysPerSimulation[i]
            data = [([0] * length)]
            listOfData.append(data)

        for i in range(0, len(tupleList)):
            weather, environ = tupleList[i]
            for day in range(0, len(weather.days)):
                data[i, day] = environ.update(weather[day])
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
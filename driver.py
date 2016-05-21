from weathermodel import WeatherModel
from environment import Environment

class Driver(object):
    """
    Driver class for simulation
    """

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

        """
        pass


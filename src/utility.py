#################################################################
#                    Utility Functions
#################################################################
#
#class to hold utility functions for use throughout the
#model
#
#functions: average_returns - takes in a list of returns
#               and a Type and returns a tuple of the
#               average on a daily bases of the count
#               and weight
#
#
#
#
#
#
#
#
#
############################################################

from src.Agents.ground_water import GroundWater
from src.Agents.drinking_water import DrinkingWater
from src.Agents.teff import Teff
from src.Agents.animal import Deer
from src.Agents.soil import Soil
import numpy as N

def average_returns(list_returns, type):
    '''Averages an Agents daily values for multiple runs

    :param list_returns: a list of list of dictionaries
            a collection of the results from the multiple
            runs
    :param type: the class name of the agent in question
            ie. Teff, Deer
    :return: A tuble with two list (count_average, weight_average)
    '''
    #The two list to be returned the averages of
    #the various runs
    output_counts = []
    output_weight = []

    #Averaging the days and appending to the list
    for x in range(len(list_returns[0])):
        output_counts.append(N.average([agent[x][type][0] for \
            agent in list_returns]))

        output_weight.append(N.average([agent[x][type][1] for \
            agent in list_returns]))

    #returns
    return (output_counts, output_weight)
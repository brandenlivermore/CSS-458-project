import numpy as N
import matplotlib.pyplot as plt
import math
import random

#Global Constants
NUM_YEARS = 1
MONTHS_PER_YEAR = 12
DAYS_PER_YEAR = 365
TOTAL_DAYS = NUM_YEARS * DAYS_PER_YEAR

"""
Weather data taken from:
    http://www.usclimatedata.com/climate/seattle/washington/united-states/uswa0395
    http://www.seattle.climatemps.com
"""
AVG_TEMP =          N.array([41.4, 44.2, 46.6, 50.4, 56.1, 61.3, 65.3, 65.7, 60.8, 53.4, 46.2, 41.5]) #Fahrenheit
AVG_PRECIP =        N.array([5.20, 3.90, 3.31, 1.97, 1.57, 1.42, 0.63, 0.75, 1.65, 3.27, 5.00, 5.43]) #Inches per month
DAYS_WITH_PRECIP =  N.array([19,   15,   16,   13,   11,   9,    5,    6,    8,    14,   17,   19]) #Days per month
HOURS_OF_SUN =      N.array([74,   99,   154,  201,  247,  234,  304,  248,  197,  122,  77,   62]) #Hours per month
DAYS_IN_MONTH =     N.array([31,   28,   31,   30,   31,   30,   31,   31,   30,   31,   30,   31]) #Days in each month

DAILY_TEMP_VARIATION = 14 #Fahrenheit
DAILY_TEMP_STD_DEV = math.sqrt(DAILY_TEMP_VARIATION) #Fahrenheit

DAILY_SUN_VARIATION = 2 #Hours
DAILY_SUN_STD_DEV = math.sqrt(DAILY_SUN_VARIATION) #Hours

SUN_PER_DAY = HOURS_OF_SUN / DAYS_IN_MONTH #Average hours of sunlight per day for each month
PRECIP_CHANCE = DAYS_WITH_PRECIP / DAYS_IN_MONTH #Chance of precipitation each day for each month
PRECIP_PER_DAY = AVG_PRECIP / DAYS_WITH_PRECIP #Average precipitation on days that have precipitation, per month



class Model(object):
    """
    Model class
    The main driver for the simulation
    """
    def __init__(self):
        """
        Initialization of model object
        Calls the initWeather method
        """
        self.dailyTemp = N.zeros([TOTAL_DAYS])
        self.dailySun = N.zeros([TOTAL_DAYS])
        self.dailyPrecip = N.zeros([TOTAL_DAYS])
        self.initWeather()

    def initWeather(self):
        """
        Initializes the weather data for the entire simulation
        The data initialized includes:

            dailyTemp: Temperature on each day of the year (Fahrenheit)
            dailyPrecip: Precipitation on each day of the year (inches)
            dailySun: Amount of sunlight on each day of the year (hours)
        """
        for month in range(0, MONTHS_PER_YEAR):
            for day in range(0, DAYS_IN_MONTH[month]):
                cumulativeDay = N.sum(DAYS_IN_MONTH[:month]) + day
                precip = random.uniform(0,1)
                if (precip <= PRECIP_CHANCE[month]):
                    self.dailyPrecip[cumulativeDay] = PRECIP_PER_DAY[month] #Add random variance
                else:
                    self.dailyPrecip[cumulativeDay] = 0
                nextMonth = month + 1
                if (nextMonth >= 11):
                    nextMonth = 0
                thisMonthsInfluence = (DAYS_IN_MONTH[month] - day) / DAYS_IN_MONTH[month]
                nextMonthsInfluence = 1 - thisMonthsInfluence
                avgTemp = (AVG_TEMP[month] * thisMonthsInfluence) + (AVG_TEMP[nextMonth] * nextMonthsInfluence)
                self.dailyTemp[cumulativeDay] = N.random.normal(avgTemp, DAILY_TEMP_STD_DEV)

                avgSun = (SUN_PER_DAY[month] * thisMonthsInfluence) + (SUN_PER_DAY[nextMonth] * nextMonthsInfluence)
                self.dailySun[cumulativeDay] = N.random.normal(avgSun, DAILY_SUN_STD_DEV)

    def displayData(self):
        """
        Displays plots for temperature, sunlight, and precipitation
        """
        dayArray = N.arange(0, TOTAL_DAYS)
        plt.plot(dayArray, m.dailyTemp)
        plt.axis([0, TOTAL_DAYS, 0, 90])
        plt.xlabel('Day')
        plt.ylabel('Temperature (F)')
        plt.title('Daily Temp')
        plt.show()

        plt.plot(dayArray, m.dailySun)
        plt.axis([0, TOTAL_DAYS, 0, 24])
        plt.xlabel('Day')
        plt.ylabel('Sunlight (hours)')
        plt.title('Daily Sun')
        plt.show()

        plt.plot(dayArray, m.dailyPrecip)
        plt.axis([0, TOTAL_DAYS, 0, 1])
        plt.xlabel('Day')
        plt.ylabel('Precipitation (inches)')
        plt.title('Daily Precipitation')
        plt.show()



m = Model()
m.displayData()

import numpy as N
import matplotlib.pyplot as plt
import math

#Global Constants
NUM_YEARS = 1
MONTHS_PER_YEAR = 12
DAYS_PER_YEAR = 265

AVG_TEMP =          N.array([41.4, 44.2, 46.6, 50,4, 56.1, 61.3, 65.3, 65.7, 60.8, 53.4, 46.2, 41.5])
AVG_PRECIP =        N.array([5.20, 3.90, 3.31, 1.97, 1.57, 1.42, 0.63, 0.75, 1.65, 3.27, 5.00, 5.43])
DAYS_WITH_PRECIP =  N.array([19,   15,   16,   13,   11,   9,    5,    6,    8,    14,   17,   19])
HOURS_OF_SUN =      N.array([74,   99,   154,  201,  247,  234,  304,  248,  197,  122,  77,   62])
DAYS_IN_MONTH =     N.array([31,   28,   31,   30,   31,   30,   31,   31,   30,   31,   30,   31])

DAILY_TEMP_VARIATION = 14
DAILY_TEMP_STD_DEV = math.sqrt(DAILY_TEMP_VARIATION)

DAILY_SUN_VARIATION = 2 #Made up for now
DAILY_SUN_STD_DEV = math.sqrt(DAILY_SUN_VARIATION)

SUN_PER_DAY = HOURS_OF_SUN / DAYS_IN_MONTH
PRECIP_CHANCE = DAYS_WITH_PRECIP / DAYS_IN_MONTH
PRECIP_PER_DAY = AVG_PRECIP / DAYS_WITH_PRECIP

class Model(object):
    def __init__(self):
        pass


    pass
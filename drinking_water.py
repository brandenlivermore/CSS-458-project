from enum import Enum

from Agents.agent import Agent


class WaterType(Enum):
    well = 0
    reservoir = 1

    class DrinkingWater(Agent):

        # conversions
        square_inches_acres = 6272640
        cubic_inches_to_gallons = 0.004329

        # Resevoir / Well Constants
        rez_max_volume = 10000  # in gallons
        well_max_volume = 10000  # in gallons

        def __init__(self, water_type):

            self.water_type = water_type


        def update(self):
            pass
from Agents.agent import Agent
from enum import Enum

class SoilType(Enum):
    sandy = 1
    rocky = 2
    dirt = 3
    mud = 4

class Soil(Agent):
    # constants for soil
    soil_retention = {SoilType.sandy: 0.75, SoilType.rocky: 0.45, \
                  SoilType.dirt: .85, SoilType.mud: .95}

    #TODO: Alex needs to research
    soil_max_retention = {SoilType.sandy: 1000000, SoilType.rocky: 1000000, \
                          SoilType.dirt: 1000000, SoilType.mud: 1000000}

    def __init__(self, soil_type):
        self.soil_type = soil_type

        self.retained_water = 0

    def update(self):
        pass

    def get_amount(self):
        return self.retained_water
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
    soil_max_retention = {SoilType.sandy: 9999, SoilType.rocky: 9999, \
                          SoilType.dirt: 9999, SoilType.mud: 9999}

    def update(self):
        pass
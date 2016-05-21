from Agents.agent import Agent
from enum import Enum
from environment import Environment
from tile import Tile
from day import Day

class SoilType(Enum):
    sandy = 1
    rocky = 2
    dirt = 3
    mud = 4

class Soil(Agent):
    # constants for soil
    soil_retention = {SoilType.sandy: 0.75, SoilType.rocky: 0.45, \
                  SoilType.dirt: .85, SoilType.mud: .95}

    # conversions
    square_inches_acres = 6272640
    cubic_inches_to_gallons = 0.004329

    #TODO: Alex needs to research
    soil_max_retention = {SoilType.sandy: 1000000, SoilType.rocky: 1000000, \
                          SoilType.dirt: 1000000, SoilType.mud: 1000000}

    def __init__(self, soil_type, tile_in):
        self.soil_type = soil_type
        self.my_tile = tile_in
        self.retained_water = 0

    def update(self):
        rainfall = self.my_tile.environment.current_day.rain_in


    def get_amount(self):
        return self.retained_water
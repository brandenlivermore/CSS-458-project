from enum import Enum
from tile import Tile
from Agents.agent import Agent
from Agents.soil import Soil
from Agents.ground_water import GroundWater
from environment import Environment

class WaterType(Enum):
    well = 0
    reservoir = 1
    none = 2

class DrinkingWater(Agent):

    # conversions
    square_inches_acres = 6272640
    cubic_inches_to_gallons = 0.004329

    # Resevoir / Well Constants
    rez_max_volume = 10000  # in gallons
    well_max_volume = 10000  # in gallons
    precent_groundwater_pulled = .001 #precent of groundwater a well pulls from the groundwater

    def __init__(self, water_type, tile_in):
        self.water_type = water_type
        self.current_volume = 0
        self.my_tile = tile_in

    def update(self):
        """
            Method:
                This method updates the volume of the DrinkingWater Agent.
                In the case that the Agent is a well type is draws from the ground
                water in the case that it is a resevoir type it collects the runoff
                from the soil and send the overflow to the tile's environment's groundwater
        :return:
        """
        if self.water_type == WaterType.well:
            volume_gw = self.my_tile.environment.my_groundwater.get_amount()
            water_pumped = volume_gw * self.precent_groundwater_pulled
            new_volume = max[self.current_volume + water_pumped, self.well_max_volume]
            water_used = new_volume - self.current_volume
            if water_used > 0:
                self.my_tile.environment.my_groundwater.set_weight(volume_gw - water_used)
                self.my_tile.weight_changed(type(self), water_used)
                self.current_volume = new_volume


        elif self.water_type == WaterType.reservoir:
            runoff = self.my_tile.get_agent(Soil).get_runoff()
            overflow = (self.current_volume + runoff) % self.rez_max_volume
            old_gw = self.my_tile.environment.my_groundwater.get_amount()
            self.my_tile.environment.my_groundwater.set_weight(old_gw + overflow)
            new_volume = max[self.rez_max_volume, self.current_volume + runoff]
            difference = new_volume - self.current_volume
            self.my_tile.weight_changed(type(self), difference)
            self.current_volume = new_volume

    def get_amount(self):
        return self.current_volume

    def set_weight(self, new_volume):
        if new_volume < 0:
            raise Exception("You cannot do that!")

        difference = new_volume - self.current_volume
        self.my_tile.weight_changed(type(self), difference)
        self.current_volume = new_volume
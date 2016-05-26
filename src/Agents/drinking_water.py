from enum import Enum

import src.Agents.soil

from src.Agents.agent import Agent


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
            runoff = self.my_tile.get_agent(src.Agents.soil.Soil).get_runoff()

            volume_gw = self.my_tile.environment.my_groundwater.get_amount() + runoff
            self.my_tile.environment.my_groundwater.set_weight(volume_gw)

            water_pumped = volume_gw * self.precent_groundwater_pulled
            new_volume = min(self.current_volume + water_pumped, self.well_max_volume)
            water_used = new_volume - self.current_volume
            if water_used > 0:
                self.my_tile.environment.my_groundwater.set_weight(volume_gw - water_used)
                self.set_weight(new_volume)


        elif self.water_type == WaterType.reservoir:
            runoff = self.my_tile.get_agent(src.Agents.soil.Soil).get_runoff()
            overflow = (self.current_volume + runoff) % self.rez_max_volume
            old_gw = self.my_tile.environment.my_groundwater.get_amount()
            self.my_tile.environment.my_groundwater.set_weight(old_gw + overflow)
            new_volume = min(self.rez_max_volume, self.current_volume + runoff)
            self.set_weight(new_volume)

        #evaporation
        temp = self.my_tile.environment.current_day.temp
        energy = (temp - 32) / 10   #the ten division is to slow the rate of evaporation
                                    #do to the nature of having less exposed water
        if energy > 0:
            self.set_weight(self.current_volume * ((temp / 180)))

    def get_amount(self):
        return self.current_volume

    def set_weight(self, new_volume):
        if new_volume < 0:
            raise Exception("You cannot do that!")

        difference = new_volume - self.current_volume
        self.my_tile.weight_changed(type(self), difference)
        self.current_volume = new_volume
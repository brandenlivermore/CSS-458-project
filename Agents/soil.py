from Agents.agent import Agent
from enum import Enum
from environment import Environment
from tile import Tile
from day import Day
import math as m
from Agents.drinking_water import DrinkingWater
from Agents.ground_water import GroundWater

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
        self.runoff = 0

    def update(self):
        """This function updates the soils current retained water

            Method:
                Soil.update() looks at the daily rainfall and updates
                the amount of water that is being held in the soil updates
                the amount in the ground water when no water feature is present
                on the tile otherwise that is left for the water feature to handle
                Updates the weight in the tile method


        :return:
            None
        """
        #the type of soil
        my_type = self.soil_type
        #the amount of gallons of precipitation
        rainfall_gallons = (self.my_tile.environment.current_day.rain_in \
            * self.square_inches_acres * self.cubic_inches_to_gallons)
        #the amount of water theoretically retained by the soil_agent
        retention = self.soil_retention[my_type] * rainfall_gallons
        #the amount of runoff in the soil
        self.runoff = (1 - self.soil_max_retention[my_type] * rainfall_gallons) \
            + ((self.retained_water + retention) % self.soil_max_retention[my_type])
        #changing the amount of water in the soil and updating tile
        new_volume = max[self.soil_max_retention[my_type], \
            self.retained_water + retention]
        difference = new_volume - self.retained_water
        self.my_tile.weight_changed(type(self), difference)
        self.retained_water = new_volume
        #updating ground water or passing the job up for the water feature to handle
        if self.my_tile.get_agent(DrinkingWater) == None:
            old_gw = self.my_tile.environment.my_groundwater.get_amount()
            self.my_tile.environment.my_groundwater.set_weight(self.runoff + old_gw)
        else:
            pass


    def get_runoff(self):
        """Gives the amount of runoff produced by the soil for that day

        :return:
            returns an integer of gallons of water that was produced in runoff
            for the soil
        """
        return self.runoff

    def get_amount(self):
        return self.retained_water

    def set_weight(self, new_retained):
        if new_retained < 0:
            raise Exception("You cannot do that!")

        difference = new_retained - self.retained_water
        self.my_tile.weight_changed(type(self), difference)
        self.retained_water = new_retained
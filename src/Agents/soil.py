from enum import Enum
import src.Agents.drinking_water

from src.Agents.agent import Agent


class SoilType(Enum):
    sandy = 1
    rocky = 2
    dirt = 3
    clay = 4

class Soil(Agent):
    # constants for soil
    soil_retention = {SoilType.sandy: 0.60, SoilType.rocky: 0.45, \
                      SoilType.dirt: .85, SoilType.clay: .95}

    # conversions
    square_inches_acres = 6272640
    cubic_inches_to_gallons = 0.004329
    #http://hydrolab.arsusda.gov/SPAW/SPAW%20Reference%20Manual/SoilWaterEvaporation.htm
    teff_coverage = 1.666666 #the linear correlation between the coverage of teff and the reduction in
                        #energy to the soil to evaporate water
    complete_cover = 60


    #http: // psep.cce.cornell.edu / facts - slides - self / facts / wat - so - grw85.aspx
    soil_max_retention = {SoilType.sandy: 1000000, SoilType.rocky: 500000, \
                          SoilType.dirt: 2000000, SoilType.clay: 1500000}

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
                Updates the weight in the tile method also calculates the loss of water
                to evaporation


        :return:
            None
        """
        #the type of soil
        my_type = self.soil_type
        #the amount of gallons of precipitation
        rainfall_gallons = (self.my_tile.environment.current_day.rain \
            * self.square_inches_acres * self.cubic_inches_to_gallons)

        #the amount of water theoretically retained by the soil_agent
        retention = self.soil_retention[my_type] * rainfall_gallons

        #the amount of runoff in the soil
        self.runoff = (1 - self.soil_retention[my_type]) * rainfall_gallons
        if retention + self.retained_water > self.soil_max_retention[my_type]:
            self.runoff += (retention + self.retained_water - self.soil_max_retention[my_type])

        #changing the amount of water in the soil and updating tile
        new_volume = min(self.soil_max_retention[my_type], \
            self.retained_water + retention)


        self.set_weight(new_volume)

        #updating ground water or passing the job up for the water feature to handle
        if self.my_tile.get_agent(src.Agents.drinking_water.DrinkingWater) == None:
            old_gw = self.my_tile.environment.my_groundwater.get_amount()
            self.my_tile.environment.my_groundwater.set_weight(self.runoff + old_gw)

        #doing evaporation for the tile's absorbed water in the case that there is a layer
        #of teff the evaporation will be lower
        #in the case that there is teff

        from src.Agents.teff import Teff

        teff = self.my_tile.get_agent(Teff)
        temp = self.my_tile.environment.current_day.temp
        if teff is not None:
            coverage = (teff.get_amount() *0.1) / Teff.threshold_acre
            energy = (1-(coverage * self.complete_cover * self.teff_coverage)) * (temp -32)
            if energy > 0:
                self.set_weight(self.retained_water * ((temp/180)* (1 - \
                    self.soil_retention[self.soil_type])))

        #in the case that there is no teff
        else:
            energy = (temp - 32)
            if energy > 0:
                self.set_weight(self.retained_water * ((temp / 180)))

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
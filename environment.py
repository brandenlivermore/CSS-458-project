import numpy as np
import tile
import animal
from animal import Deer, Wolf, Animal

class environment(object):

#################################################################
#                    Environment Static Variables
#################################################################
    #conversions
    square_inches_acres = 6272640
    cubic_inches_to_gallons = 0.004329

    #constants for soil
    soil_types = {"sandy": 0.75, "rocky": 0.45, \
                  "dirt": .85, "mud": .95}


    #Constants for Teff Grass
    #sourced from http://teffgrass.com/harvesting-teff/
    teff_growing_sun = 8.2 #hours a day
    teff_water_consume_acres = 1785 #gallons
    teff_ideal_temp = 63.275 #in degrees celsius
    teff_min_temp = 32.1 #in degrees celsius
    teff_min_sun = 4.32 #hours per day
    teff_max_heat = 100 #degrees celsius
    teff_seed_date = 225 #day of year teff tests to seed
    max_teff_acre = 16000 #pounds
    threshold_teff_acre = 177 #pounds
    teff_death_chance = .01 #chance teff is wiped out if below threshold

    #Resevoir / Well Constants
    rez_max_volume = 10000 #in gallons
    well_max_volume = 10000 #in gallons


    #percent chances
    teff_seed = 0.5 #base chance of seeding adjacent tiles
    chance_reservoir = .02 #chance of tile having resevoir
    chance_well = .001 #chance of tile having a well
    tree_seed = .05 #base chance of seeding adjacent tiles

#################################################################
#                    Constructor
#################################################################
    def __init__(self, in_width, in_height):
        #variables for environment
        teff_total_mass = 0  # in pounds
        tree_total_mass = 0  # in pounds
        total_volume_groundwater = 0  # in gallons

        # values for storing the grid of tiles
        width = 0
        height = 0
        grid = None

        #values for controlling animals
        total_mass_animal = 0 #in lbs
        animals_alive = {Deer: 0, Wolf: 0}

        #setting size of grid and creating grid
        self.height = in_height
        self.width = in_width
        grid = np.empty([self.height,self.width], dtype=object)


        well = False
        res = False
        #random array for determining placement of wells and reservoirs
        test_array = np.random.rand(self.height,self.width)
        #filling grid with tiles
        for x in range(self.height):
            for i in range (self.width):
                if(test_array[x,i] < self.chance_well):
                    well = True
                elif(test_array[x, i] < self.chance_reservoir):
                    res = True
                grid[x,i] = tile(res, self.soil_types[1], well, \
                                 self)
                grid[x,i].tile_x = x
                grid[x,i].tile_y = i
                well = False
                res = False

        def update(day_in):
            grid[:,:].update
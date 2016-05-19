import numpy as np
from animal import Deer, Wolf, Animal
from tile import Tile
import math as m

class Environment(object):

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
    teff_seed_date = [225,175] #day of year teff tests to seed
    max_teff_acre = 16000 #pounds
    teff_threshold_acre = 177 #pounds
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
        self.teff_total_mass = 0  # in pounds
        self.tree_total_mass = 0  # in pounds
        self.total_volume_groundwater = 0  # in gallons

        # values for storing the grid of tiles
        self.width = 0
        self.height = 0
        self.grid = None

        #values for controlling animals
        self.total_mass_animal = 0 #in lbs
        self.animals_alive = {Deer: 0, Wolf: 0}

        #setting size of grid and creating grid
        self.height = in_height
        self.width = in_width
        self.grid = np.empty([self.height,self.width], dtype=Tile)


        #for managing day
        self.current_day = None

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
                self.grid[x,i] = Tile(res, self.soil_types[1], well, \
                                 self)
                self.grid[x,i].tile_x = x
                self.grid[x,i].tile_y = i
                well = False
                res = False

    def update(self, day_in):
        self.current_day = day_in
        self.grid[:,:].update



    def is_location_valid(self, location):
        '''
        Returns whether or not the given location is valid (inside
        of the grid).

        :param location: List of length 2 where index 0 is the
            x-coordinate and index 1 is the y-coordinate of the
            location that is to be checked
        :return: True if the location is inside the grid, False
            otherwise.
        '''
        return location[0] >= 0 and location[0] < Environment.width \
               and location[1] >= 0 and location[1] < Environment.height


    def get_tile(self, loc):
        if(self.is_location_valid(loc)):
            return self.grid[loc[0], loc[1]]
        else:
            return None

    def get_adjacent(self, local_in, radius=1):
        if(isinstance(local_in, Tile)):
            x = local_in.tile_x
            y = local_in.tile_y
        else:
            x = local_in[0]
            y = local_in[1]

        possible_cords = []

        for x_i in range(x-radius, x-radius+1):
            for y_i in range(y-radius, y+radius +1):
                possible_cords.append([x_i,y_i])

        possible_cords.remove([x,y])
        tiles_out = []

        for x_i in range(len(possible_cords)):
            if(self.is_location_valid(possible_cords[x_i])):
                tiles_out.append(self.grid[possible_cords[0], possible_cords[1]])

        return tiles_out


    def get_distance(self, cord_1, cord_2):
        if(isinstance(cord_1, Tile)):
            x_1 = cord_1.tile_x
            y_1 = cord_1.tile_y
        else:
            x_1 = cord_1[0]
            y_1 = cord_1[1]
        if(isinstance(cord_2, Tile)):
            x_2 = cord_2.tile_x
            y_2 = cord_2.tile_y
        else:
            x_2 = cord_2[0]
            y_2 = cord_2[1]

        return m.sqrt((x_2-x_1)**2+(y_2-y_1)**2)

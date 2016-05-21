import numpy as np

from Agents.animal import Deer, Wolf
from Agents.soil import SoilType
from Agents.drinking_water import WaterType
from tile import Tile
import math as m


class Environment(object):

#################################################################
#                    Environment Static Variables
#################################################################

    #percent chances
    chance_reservoir = .02 #chance of tile having resevoir
    chance_well = .001  # chance of tile having a well

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

        water_type = WaterType.none

        #random array for determining placement of wells and reservoirs
        test_array = np.random.rand(self.height,self.width)
        #filling grid with tiles
        for x in range(self.height):
            for i in range (self.width):

                if(test_array[x,i] < self.chance_well):
                    water_type = WaterType.well
                elif(test_array[x, i] < self.chance_reservoir):
                    water_type = WaterType.reservoir
                self.grid[x,i] = Tile(res, SoilType.sandy, well, \
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

    def agent_moved_to_tile(self, agent, new_tile):
        '''

        To be called whenever an agent moves. Updates the appropriate
        tiles.

        :param agent: The agent that is moving
        :param new_tile: Tile object that the agent is moving to
        :return: None
        '''
        old_tile = agent.tile
        old_tile.remove_agent(agent)
        new_tile.add_agent(agent)

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

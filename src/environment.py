import math as m
from copy import deepcopy

import numpy as N
from src.Agents.drinking_water import WaterType
from src.Agents.ground_water import GroundWater
from src.Agents.soil import SoilType

from src.tile import Tile


def nearly_equal(x,y, sig_fig=5):
    '''Takes in two integers or floating point numbers and checks
        if they are equal to within the significant digit

        Source:
          http://stackoverflow.com/questions/558216/function-to-determine-
          if-two-numbers-are-nearly-equal-when-rounded-to-n-signific

    :param x: first value to compare
    :param y: second value to compare
    :param sig_fig:  significant digits
    :return: returns a boolean true if the values are the same
                within the significant digits or false otherwise
    '''
    return (x == y or int(x*10**sig_fig) == int(y*10**sig_fig))


class Environment(object):

#################################################################
#                    Environment Static Variables
#################################################################

    #percent chances
    chance_reservoir = 0.05 #chance of tile having resevoir
    chance_well = 0.03 # chance of tile having a well

    #list of possible agent types
#################################################################
#                    Constructor
#################################################################
    def __init__(self, in_width, in_height):
        #building the total count and weight dictionary
        self.agent_totals = {}

        #setting size of grid and creating grid
        self.height = in_height
        self.width = in_width
        self.grid = N.empty([self.height,self.width], dtype=Tile)

        #adding groundwater agent
        self.my_groundwater = GroundWater(enviro_in=self)
        self.agent_totals[type(self.my_groundwater)] = [1, 0]

        #variables for environment
        self.teff_total_mass = 0  # in pounds
        self.tree_total_mass = 0  # in pounds


        #for managing day
        self.current_day = None

        water_type = WaterType.none

        #random array for determining placement of wells and reservoirs
        test_array = N.random.rand(self.height,self.width)
        #filling grid with tiles
        for x in range(self.height):
            for i in range (self.width):
                water_type = WaterType.none
                if(test_array[x,i] < self.chance_well):
                    water_type = WaterType.well
                elif(test_array[x, i] < self.chance_reservoir):
                    water_type = WaterType.reservoir
                self.grid[x,i] = Tile(SoilType.sandy, water_type, \
                                 self)
                self.grid[x,i].tile_x = x
                self.grid[x,i].tile_y = i

    def update(self, day_in):
        self.current_day = day_in

        for tile in N.ndenumerate(self.grid):
            tile[1].update()

        return deepcopy(self.agent_totals)



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
        return location[0] >= 0 and location[0] < self.width \
               and location[1] >= 0 and location[1] < self.height


    def get_tile(self, loc):
        if(self.is_location_valid(loc)):
            return self.grid[loc[0], loc[1]]
        else:
            return None

    def get_adjacent(self, local_in, radius=1):

        x = None
        y = None

        if(isinstance(local_in, Tile)):
            x = local_in.tile_x
            y = local_in.tile_y
        else:
            x = local_in[0]
            y = local_in[1]

        possible_cords = []

        for x_i in range(x-radius, x+radius+1):
            for y_i in range(y-radius, y+radius +1):
                possible_cords.append([x_i, y_i])

        #possible_cords.remove([x,y])
        tiles_out = []

        for current_coord in possible_cords:
            if(self.is_location_valid(current_coord)):
                tiles_out.append(self.grid[current_coord[0], current_coord[1]])

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
        agent.tile = new_tile

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

    def update_total_mass_and_count(self, type, mass_difference, count_difference=0):
        if type in self.agent_totals:
            self.agent_totals[type] = [self.agent_totals[type][0] + count_difference,\
                self.agent_totals[type][1] + mass_difference]
        else:
            self.agent_totals[type] = [count_difference, mass_difference]
import environment, tile_actions, Agents.animal, day
from Agents.animal import Animal, Wolf, Deer
import tile_actions


class Tile(object):

    def __init__(self, add_reservoir, soil_in, well_in, eviro_in):
        self.reservoir = add_reservoir # does a reservoir exist on tile
        self.soil_type = soil_in
        self.environment = eviro_in
        self.well = well_in

        # tile location
        self.tile_x = 0
        self.tile_y = 0

        self.teff_coverage = 0  # percent of the land covered in teff
        self.teff_mass = 0  # mass of teff on land in lbs

        self.tree_coverage = 0  # coverage of trees on tile
        self.tree_mass = 0  # mass of trees in lbs
        self.reservoir_volume = 0  # volume of reservoir in gallons
        self.well_volume = 0  # gallons

        self.list_animals = [] #animals responsible for tracking themselves
        self.list_objects = {} #list of objects present on tile

    def update(self):
        #checking if the date is a day of the year seeding occurs and that
        #there is a minium amount of teff to seed adjacent tiles
        #if yes then seeding adjacent tiles
        if(self.environment.current_day.day in self.environment.teff_seed_date \
            and self.teff_mass > self.environment.teff_threshold_acre):
            tile_actions.seed_tiles(self)

        #checking to make sure that there is teff to grow then calling grow function
        if(self.teff_mass > 0):
            tile_actions.water_manage(self)

        #managing the water of the tile
        tile_actions.teff_grow(self)


    def add_agent(self, agent_in):
        self.list_animals.append(agent_in)
        if(type(agent_in) in self.list_objects):
            self.list_objects[type(agent_in)] = self.list_objects[type(agent_in)] \
                + 1
        else:
            self.list_objects[type(agent_in)] = 1

    def remove_agent(self, agent_in):
        self.list_animals.remove(agent_in)
        self.list_objects[type(agent_in)] = self.list_objects[type(agent_in)] \
            - 1
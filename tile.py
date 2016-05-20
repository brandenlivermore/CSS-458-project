import numpy as N
import environment, Agents.animal, day
from Agents.animal import Animal, Wolf, Deer
from Agents.soil import Soil, SoilType
from Agents.teff import Teff
from Agents.drinking_water import DrinkingWater, WaterType


class Tile(object):

    def __init__(self, soil_in, water_type, eviro_in):

        self.environment = eviro_in

        # tile location
        self.tile_x = 0
        self.tile_y = 0

        self.agent_mapping = {}  # list of objects present on tile
        self.agent_weights = {}

        self.priority_agent_types = [Teff, Soil, DrinkingWater]

        soil = Soil(soil_in)
        self.add_agent(soil)

        if water_type is not WaterType.none:
            self.add_agent(DrinkingWater(water_type))

        self.teff_coverage = 0  # percent of the land covered in teff
        self.teff_mass = 0  # mass of teff on land in lbs

        self.tree_coverage = 0  # coverage of trees on tile
        self.tree_mass = 0  # mass of trees in lbs
        self.reservoir_volume = 0  # volume of reservoir in gallons
        self.well_volume = 0  # gallons


    def update(self):
        for priority_agent_type in self.priority_agent_types:
            if priority_agent_type in self.agent_mapping:
                self.agent_mapping[priority_agent_type][:].update()

        for agent_type in self.agent_mapping:
            if agent_type in self.priority_agent_types:
                continue

            agent_list = self.agent_mapping[agent_type]
            N.random.shuffle(agent_list)
            agent_list[:].update()

    def add_agent(self, agent_in):
        type = type(agent_in)

        if type in self.agent_mapping:
            self.agent_mapping[type].append(agent_in)
        else:
            self.agent_mapping[type] = N.array(agent_in)

        if type in self.agent_weights:
            self.agent_weights[type] = \
                self.agent_weights[type] + agent_in.get_amount()
        else:
            self.agent_weights[type] = agent_in.get_amount()


    def remove_agent(self, agent_in):
        type = type(agent_in)

        self.agent_mapping[type].remove(agent_in)
        self.agent_weights[type] = self.agent_weights[type] - agent_in.get_amount()

    def weight_changed(self, type, difference):
        self.agent_weights[type] = \
            self.tile.agent_weights[type] + difference

    def get_agent(self, type):
        if type in self.agent_mapping and len(self.agent_mapping[type]) > 0:
            return self.agent_mapping[type][0]
        else:
            return None

    def get_mass_and_totals(self):
        for agent_type in self.agent_mapping
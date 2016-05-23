from copy import deepcopy

import numpy as N
from src.Agents.drinking_water import DrinkingWater, WaterType
from src.Agents.teff import Teff

from src.Agents.soil import Soil


class Tile(object):

    def __init__(self, soil_in, water_type, eviro_in):

        self.environment = eviro_in

        # tile location
        self.tile_x = 0
        self.tile_y = 0

        self.agent_mapping = {}  # list of objects present on tile
        self.agent_weights = {}

        self.priority_agent_types = [Teff, Soil, DrinkingWater]

        soil = Soil(soil_in, self)
        self.add_agent(soil)

        if water_type is not WaterType.none:
            self.add_agent(DrinkingWater(water_type, self))

    def update(self):
        for priority_agent_type in self.priority_agent_types:
            if priority_agent_type in self.agent_mapping:
                for agent in self.agent_mapping[priority_agent_type]:
                    agent.update()

        for agent_type in self.agent_mapping:
            if agent_type in self.priority_agent_types:
                continue

            agent_list = self.agent_mapping[agent_type]
            N.random.shuffle(agent_list)

            for agent in agent_list:
                agent.update()

    def add_agent(self, agent_in):
        agent_type = type(agent_in)

        if agent_type in self.agent_mapping:
            N.append(self.agent_mapping[agent_type], agent_in)
        else:
            self.agent_mapping[agent_type] = N.array([agent_in])
        if agent_type in self.agent_weights:
            self.agent_weights[agent_type] = \
                self.agent_weights[agent_type] + agent_in.get_amount()
        else:
            self.agent_weights[agent_type] = agent_in.get_amount()

        self.environment.agent_totals[agent_type] = [self.environment.agent_totals[agent_type][0] + 1, \
            self.environment.agent_totals[agent_type][1] + (agent_in.get_amount() / 1000.0)]

    def remove_agent(self, agent_in):
        type = type(agent_in)

        self.agent_mapping[type].remove(agent_in)
        self.agent_weights[type] = self.agent_weights[type] - agent_in.get_amount()
        self.environment.agent_totals[type] = [self.environment.agent_totals[type][0] -1, \
            self.environment.agent_totals[type][1] - (agent_in.get_amount() / 1000.0)]

    def weight_changed(self, type, difference):
        self.agent_weights[type] = \
            self.agent_weights[type] + difference
        self.environment.agent_totals[type][1] = self.environment.agent_totals[type]\
            [1] + (difference / 1000.0)

    def get_agent(self, type):
        if type in self.agent_mapping and self.agent_mapping[type].size > 0:
                return self.agent_mapping[type][0]
        else:
            return None

    def get_mass_and_totals(self):
        out_values = deepcopy(self.agent_weights)
        for agent_type in self.out_values:
                out_values[agent_type] = [len(self.agent_mapping[agent_type]),\
                                          self.agent_weights[agent_type]]
        return out_values
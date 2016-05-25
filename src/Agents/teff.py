import random as random
import src.environment as enviro
import numpy as np
from src.Agents.soil import Soil

from src.Agents.agent import Agent


class Teff(Agent):

    #Constants for Teff Grass
    #sourced from http://teffgrass.com/harvesting-teff/
    percent_water = .12 #amount of teff that is water
    growing_sun = 8.2 #hours a day
    water_consume_acres = 1785 #gallons
    ideal_temp = 63.275 #in degrees celsius
    min_temp = 32.1 #in degrees celsius
    max_temp = 101 #degrees celsius
    seed_date = [225,175] #day of year teff tests to seed
    max_per_acre = 16000 #pounds
    threshold_acre = 177 #pounds
    high_growth = 12000 #pounds per 55 day period
    low_growth = 2500 #pounds per 55 day period
    growth_period = 55 #days
    max_loss = .1 #maxium amount of teff loss to extreme temperatures
    death_chance = .05  #chance teff is wiped out if below threshold
    seed = 0.5 #base chance of seeding adjacent tiles
    updates = True
    
    def __init__(self, tile_in):
        # for initial test 
        self.current_weight = self.threshold_acre
        self.coverage = 1  # percent of the land covered in teff
        self.my_tile = tile_in

    def update(self):
        #####If the update variable is false update will not run
        if not self.updates:
            return None
        #checking to see if there is no more Teff left to eat
        #if so removing the object from the tile and deletes self
        if enviro.nearly_equal(self.current_weight, 0):
            self.my_tile.remove_agent(self)
            del self
            return
        ##checking if teff is in danger of desicating then
        elif self.current_weight <= self.threshold_acre:
            if random.random() <= self.death_chance:
                self.my_tile.remove_agent(self)
                del self
                return
        #preforming the growth update in the case that the teff survives

        #checking to make sure that the paremeters are inside
        #safe values
        sun = self.my_tile.environment.current_day.sun
        temp = self.my_tile.environment.current_day.temp
        #if true growing the teff
        if temp >= self.min_temp and temp <= self.max_temp:
            growth_factor = ((sun / self.growing_sun) + (temp / self.ideal_temp)) / 2
            desired_growth = ((self.high_growth + self.low_growth) * growth_factor) \
                / self.growth_period
            soil = self.my_tile.get_agent(Soil)
            available_water = soil.get_amount()
            #checking to makes sure the teff has enough water to grow
            if available_water >= (self.water_consume_acres):
                self.set_weight(min(self.current_weight+desired_growth, self.max_per_acre))
                soil.set_weight(available_water-(self.water_consume_acres))
            #else desired growth is hampered by the available water
            else:
                desired_growth = desired_growth * (available_water/self.water_consume_acres)
                self.set_weight(min(self.current_weight + desired_growth, self.max_per_acre))
                soil.set_weight(0)
        # if not inside desired values the teff looses some amount of it's mass
        # to the extreme temperatures
        else:
            amount_lost = random.uniform(0, self.max_loss)
            self.set_weight(self.current_weight * (1 - amount_lost))

        #doing seeding if the day of the year is the seed day
        if self.my_tile.environment.current_day.day in self.seed_date and \
                self.current_weight > self.threshold_acre:
            to_seed = self.my_tile.environment.get_adjacent(self.my_tile)
            will_seed = np.random.random(len(to_seed))
            for x in range(len(to_seed)):
                if will_seed[x] <= self.seed and (to_seed[x].get_agent(Teff) == None):
                    to_seed[x].add_agent(Teff(to_seed[x]))

    def get_amount(self):
        return self.current_weight

    def set_weight(self, new_weight):
        if new_weight < 0:
            raise Exception("You cannot do that!")

        difference = new_weight - self.current_weight
        self.my_tile.weight_changed(type(self), difference)
        self.current_weight = new_weight
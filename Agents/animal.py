import numpy as N
import random
from enum import Enum

from Agents.agent import Agent
from Agents.teff import Teff
# from tile import Tile #err. Just pass in reference to tile obj to inst var

class AnimalType(Enum):
    predator = 1
    prey = 2

class State(Enum):
    dead = 0
    alive = 1

class Animal(Agent):
    """Animal object
        Base class for all animals.

        Attributes
        ----------
        tile : reference to animal's tile in environment

    """
    def __init__(self, tile):
        self.speed = 0
        self.type = None # See AnimalType enum above, can be predator or prey
        self.state = State.alive
        self.age = 0
        self.max_age = 0
        self.weight = 0.0
        self.max_weight = 0.0
        self.gestationPeriod = 0
        self.matingSeasons = []
        self.tile = tile

        self.rememberedResources = [] #coords of water, food, etc.
        self.consumptionRate = 0.0
        self.birthRate = 0.0 #offspring per year

        self.days_to_decompose = 0.0 # based on 3 months for a human
        self.days_deceased = 0.0
        self.objectives = []

    def update(self):
        '''
        Updates the animal by moving it to a random adjacent
        tile.

        Intended to be overridden by subclasses.

        :return: None
        '''

        self.move()

    def move(self):
        '''
        Moves the animal randomly.

        A random location is chosen and the animal
        attempts to move to it. If it is not a valid
        location, a new location is chosen. This repeats
        until the animal successfully moves.

        :return: None
        '''
        x = self.tile.tile_x
        y = self.tile.tile_y

        adjacent_tiles = self.tile.environment.get_adjacent(self.tile,
                                                            radius=self.speed)

        index = random.randint(len(adjacent_tiles))

        self.tile.environment.agent_moved_to_tile(self, adjacent_tiles[index])

    def set_weight(self, val):
        '''Set Deer Weight
        Updates deer weight and adjusts weight of its tile accordingly
        :param difference: the amount of weight to be changed
        '''
        difference = val - self.weight
        self.weight = val
        self.tile.weight_changed(type(self), difference)

    def remove(self):
        self.tile.remove_agent(self)
        del self
        
    def eat(self):
        pass

class Deer(Animal):
    '''Deer object

        Resources
        ---------
        http://animals.nationalgeographic.com/animals/mammals/white-tailed-deer/
        http://wiredtohunt.com/2010/05/18/how-much-food-does-a-deer-eat-a-year/
        https://www.michigan.gov/dnr/0,4570,7-153-10370_12150_12220-26946--,00.html
        http://www.desertusa.com/animals/white-tail-tdeer.html
    '''
    TOTAL_DEER = 0

    def __init__(self, tile):
        super(Deer, self).__init__(tile)

        Deer.TOTAL_DEER += 1

        self.speed = 30.0 #mph (top speed, escaping. can also jump 30 feet)
        self.type = AnimalType.prey
        self.age = 0.0
        self.maxAge = random.uniform(6,14)

        '''
        1 1/2 quarts for every 100 pounds of body weight per day during the
        winter.
        This requirement doubles during the summer, with deer needing about 3
        quarts for every 100 pounds of body weight.
        '''
        self.thirst = self.max_thirst = 100 #TODO determine thirst level? Keep?
        # deer can lose 25-30% of body weight without dying
        self.weight = self.max_weight = random.uniform(110, 300) #lbs
        self.gestationPeriod = 7 #months pregnant
        self.matingSeasons = ["May","June"]
        self.female_ratio = 0.66

        self.consumptionRate = 8.22 # lbs/day from 3000 lbs/yr
        self.birthRate = 0.0  # offspring per year

        self.rememberedResources = []  # coords of water, food, etc.

        self.days_to_decompose = 90.0 # based on 3 months for a human
        self.days_deceased = 0.0

        # self.objectives = [] #inherited from animal

    def update(self):
        '''Update Deer
        '''
        if (self.state == 'alive'): # deer alive
            print("Update deer alive")
            self.move()
            self.eat()
            #TODO: once a year, spawn new deer all at once
            # self.reproduce()
        elif (self.state == 'dead'):
            print("Update deer dead") # deer dead
            self.days_deceased += 1
            if self.days_deceased >= self.days_to_decompose:
                self.remove()

    def move(self):
        '''Move Deer
        TODO: safely remove eat. move() simply relocates deer to place with
        most abundant grass.
        :return:
        '''
        tiles = self.tile.environment.get_adjacent(self.tile, self.speed)

        max_tile = self.tile

        # Get tile with the most Teff within sight distance
        for tile in tiles:
            teff_amount = tile.get_agent(Teff).get_amount()

            if teff_amount is not None and teff_amount > max_tile.get_amount():
                max_tile = tile

        #move deer to tile w/ most teff and set vars
        self.tile.environment.agent_moved_to_tile(self, max_tile)

    def remove(self):
        self.tile.remove_agent(self)
        del self
        Deer.TOTAL_DEER -= 1

    def eat(self):
        '''Eat Grass
        Eats the grass, modifies itself accordingly, and checks for hunger.

        With the current 1-lb-per-day implementation,
            biggest deer can last ~2 months straight, while
            smallest deer can last ~1 month straight without food

        PreCond: Deer previously moved to tile with most abundant grass
        :return:
        '''

        #get teff
        teff_agent = self.tile.get_agent(Teff)

        if (teff_agent is None or teff_agent.current_weight <= 0):
            # teff empty/ starve case
            self.set_weight(self.weight-1) #starve a bit
            self.thirst -= 1 #thirst a bit

            self._check_starve() # check for starvation here
        else:
            #teff exists/ eat case
            #get teff weight
            teff_weight = teff_agent.get_amount()

            #decrease teff weight
            teff_eaten = min(self.consumptionRate, teff_weight)
            teff_agent.set_weight(teff_weight - teff_eaten)

            #increase deer weight by fraction of teff eaten
            weight_gained = random.uniform(0, teff_eaten)
            new_weight = min(self.weight + weight_gained, self.max_weight)
            self.set_weight(new_weight)

            #increase deer thirst meter
            self.thirst += self.consumptionRate * teff_agent.percent_water

    def _check_starve(self):
        '''Check for starvation
        A check performed on a day where a deer is on a tile with no grass.
        Losing Between 25 and 30% of its body weight puts it at risk
        Any amount lost more than 30% results in death.
        :return:
        '''
        if self.weight <= self.max_weight * 0.70:
            #insta-death
            self.state = State.dead
            pass
        elif self.weight <= self.max_weight * 0.75:
            #chance-death : 50/50
            coin = [True,False]
            N.random.shuffle(coin)
            if (coin[0]):
                self.state = State.dead

    def reproduce(self):
        '''Increase Deer Population

        reference: Just 2 deer without predation can produce a herd of up to 35
                deer in just 7 years. (up to 5 offspring per year)

                4-5 lbs at birth

        http://www.deerdamage.org/page/deer-facts
        http://bioweb.uwlax.edu/bio203/s2007/parr_jaco/taxonomy.htm


        :return: None
        '''
        # get single birthing day (rand mating season time + gestation period)

        # take female population (whole * female_ratio)
        # give each a chance to birth 1-4 babies
        # place children on empty squares (or just same tile?)


class Wolf(Animal):

    def __init__(self, tile):
        super(Wolf, self).__init__(tile)


import random
from enum import Enum

from Agents.agent import Agent
from Agents.teff import Teff

class AnimalType(Enum):
    predator = 1
    prey = 2

class Animal(Agent):
    """Animal object
        Base class for all animals.

        Attributes
        ----------
        tile : reference to animal's tile in environment

    """
    def __init__(self, tile):
        self.speed = 0
        self.energy = 0.0
        self.type = None # See AnimalType enum above, can be predator or prey
        self.age = 0
        self.maxAge = 0
        self.weight = 0.0
        self.gestationPeriod = 0
        self.matingSeasons = []
        self.tile = tile

        self.rememberedResources = [] #coords of water, food, etc.
        self.consumptionRate = 0.0
        self.birthRate = 0.0 #offspring per year

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

    def eat(self):

        pass

class Deer(Animal):
    '''Deer object

        Resources
        ---------
        http://animals.nationalgeographic.com/animals/mammals/white-tailed-deer/
        http://wiredtohunt.com/2010/05/18/how-much-food-does-a-deer-eat-a-year/
    '''
    def __init__(self, tile):
        super(Deer, self).__init__(tile)
        self.hunger = 0.0

        self.speed = 30.0 #mph (top speed, escaping. can also jump 30 feet)
        # self.health = 0.0
        self.type = AnimalType.prey
        self.age = 0.0
        self.maxAge = random.uniform(6,14)
        self.weight = random.uniform(110, 300) #lbs
        self.gestationPeriod = 7 #months pregnant
        self.matingSeasons = ["May","June"]

        self.rememberedResources = []  # coords of water, food, etc.
        self.consumptionRate = 8.22 # lbs/day from 3000 lbs/yr
        self.birthRate = 0.0  # offspring per year

        # self.objectives = []
    def move(self):

        tiles = self.tile.environment.get_adjacent(self.tile, self.speed)

        max_tile = self.tile

        # Get tile with the most Teff within sight distance
        for tile in tiles:
            teff_amount = tile.get_agent(Teff).get_amount()

            if teff_amount is not None and teff_amount > max_tile.get_amount():
                max_tile = tile

        if max_tile.get_agent(Teff) is not None:
            self.tile.environment.agent_moved_to_tile(self, max_tile)
            self.eat()
        else:
            self.tile.weight_changed(type(self), -1)
            self.weight -= 1

    def eat(self):
        '''Eat Grass
        Consumes 'consumptionRate' amt of grass in current tile and records
        changes in tile's Teff agent.

        * if teff_mass is less than 'consumptionRate',
            [move? Increase hunger?]

        Pre: Deer previously moved to tile with most abundant grass

        :return: None
        '''

        remainingTeff = self.tile.get_agent(Teff).get_amount() - self.consumptionRate
        self.tile.set_weight = max(remainingTeff, 0)

        #TODO: gain weight? or something.


class Wolf(Animal):

    def __init__(self, tile):
        super(Wolf, self).__init__(tile)


import random
from enum import Enum

from Agents.agent import Agent
# from tile import Tile #err. Just pass in reference to tile obj to inst var

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

        self.animal_attempt_move(adjacent_tiles[index])

    def animal_attempt_move(self, new_tile):
        '''
        Attempts to move the self (an animal) to the given location.

        If the location is valid, the animal is moved to the
        new location and the animal is removed from its previous
        tile and added to the new tile.

        :param location: List of length 2 where index 0 is the
            x-coordinate and index 1 is the y-coordinate of the
            desired move location
        :param animal: The animal that is attempting to move
        :return: None
        '''

        environment = self.tile.environment

        new_tile.list_animals.append(self)

        original_tile = self.tile
        original_tile.list_animals.remove(self)

        self.tile = new_tile
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
    def eat(self):
        '''Eat Grass
        Consumes 'consumptionRate' amt of grass in current tile and records
        changes in tile's teff_mass variable.

        * if teff_mass is less than 'consumptionRate',
            [move? Increase hunger?]

        Pre: Deer previously moved to tile with most abundant grass

        :return:
        '''
        remainingTeff = self.tile.teff_mass - self.consumptionRate
        self.tile.teff_mass = min(remainingTeff, 0)

        if (remainingTeff <= 0):
            #handle starvation
            pass

        # print ('remainingTeff' + remainingTeff)

### Testing
# aTile = Tile()
# aDeer = Deer(aTile)
# aDeer.eat()
###

class Wolf(Animal):

    def __init__(self, tile):
        super(Wolf, self).__init__(tile)


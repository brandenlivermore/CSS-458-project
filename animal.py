import numpy as N
import random
from enum import Enum

class AnimalType(Enum):
    predator = 1
    prey = 2

class Animal(object):
    '''Animal object
        Base class for all animals

    '''
    def __init__(self, tile):
        self.speed = 0.0
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
        #age
        #perform next step in objective

        pass

    def move(self, environment):
        '''
        Moves the animal randomly.

        A random location is chosen and the animal
        attempts to move to it. If it is not a valid
        location, a new location is chosen. This repeats
        until the animal successfully moves.

        :param environment: the animal's environment
        :return: None
        '''
        x = self.tile.tile_x
        y = self.tile.tile_y

        x_locations = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
        y_locations = [-1, 0, 1, -1, 0, 1, -1, 0, 1]

        success = False

        while success is False:
            random_index = random.randint(len(x_locations) - 1)
            success = self.environment.animal_attempt_move([x_locations[random_index], y_locations[random_index]], self)

    def animal_attempt_move(self, location):
        '''
        Attempts to move the given animal to the given location.

        If the location is valid, the animal is moved to the
        new location and the animal is removed from its previous
        tile and added to the new tile.

        :param location: List of length 2 where index 0 is the
            x-coordinate and index 1 is the y-coordinate of the
            desired move location
        :param animal: The animal that is attempting to move
        :return: A boolean, True if the move was successful or
            False otherwise
        '''

        environment = self.tile.environment

        if not environment.is_location_valid(location):
            return False

        new_tile = environment.grid[location[0], location[1]]
        new_tile.list_animals.append(self)

        original_tile = self.tile
        original_tile.list_animals.remove(self)

        self.tile = new_tile
        return True

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

    def update(self):
        pass

class Wolf(Animal):

    def __init__(self, tile):
        super(Wolf, self).__init__(tile)

#testing
aDeer = Deer()
print(aDeer.maxAge)
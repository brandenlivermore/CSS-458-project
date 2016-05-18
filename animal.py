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
        x = self.tile.tile_x
        y = self.tile.tile_y

        x_locations = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
        y_locations = [-1, 0, 1, -1, 0, 1, -1, 0, 1]

        random_index = random.randint(7)

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
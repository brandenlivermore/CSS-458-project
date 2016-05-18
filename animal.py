import numpy as N
import random

class Animal(object):
    '''Animal object
        Base class for all animals

    '''
    def __init__(self):
        self.hunger = 0.0
        self.speed = 0.0
        self.health = 0.0
        self.type = None #"Predator" or "prey"
        self.age = 0
        self.maxAge = 0
        self.weight = 0.0
        self.gestationPeriod = 0
        self.matingSeasons = []

        self.rememberedResources = [] #coords of water, food, etc.
        self.consumptionRate = 0.0
        self.birthRate = 0.0 #offspring per year

        self.objectives = []

    def update(self):
        #age
        #perform next step in objective

        pass

class Deer(Animal):
    '''Deer object

        Resources
        ---------
        http://animals.nationalgeographic.com/animals/mammals/white-tailed-deer/
        http://wiredtohunt.com/2010/05/18/how-much-food-does-a-deer-eat-a-year/
    '''
    def __init__(self):
        self.hunger = 0.0

        self.speed = 30.0 #mph (top speed, escaping. can also jump 30 feet)
        # self.health = 0.0
        self.type = "prey"  # "Predator" or "prey"
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

#testing
aDeer = Deer()
print(aDeer.maxAge)
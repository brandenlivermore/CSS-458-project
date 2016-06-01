import random
from enum import Enum

import numpy as N
from src.Agents.teff import Teff
from src.Agents.drinking_water import DrinkingWater

from src.Agents.agent import Agent


# from tile import Tile #err. Just pass in reference to tile obj to inst var

class AnimalType(Enum):
    predator = 1
    prey = 2
    ominvore = 3

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
    # taken from weathermodel as workaround to help with reproduction
    DAYS_IN_MONTH = N.array(
        [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])  # Days in each month
    CUMSUM_MONTHS = N.cumsum(DAYS_IN_MONTH)

    def __init__(self, tile):
        self.speed = 0
        self.type = None # See AnimalType enum above, can be predator or prey
        self.state = State.alive
        self.age = 0
        self.day_born = self.get_current_day()
        self.max_age = 0
        self.weight = 0.0
        self.max_weight = 0.0
        self.gestation_period = 0
        self.matingSeasons = []
        self.tile = tile
        self.is_female = None

        self.rememberedResources = [] #coords of water, food, etc.
        self.consumptionRate = 0.0
        self.birthRate = 0.0 #offspring per year

        self.days_to_decompose = 0.0 # based on 3 months for a human
        self.days_deceased = 0.0
        self.objectives = []

        self.thirst = None

    def get_current_day(self):
        return int(self.tile.environment.current_day)
    def get_day(self):
        return int(self.tile.environment.current_day % 365)
    def get_year(self):
        return int(self.tile.environment.current_day / 365)

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

    def get_amount(self):
        return self.weight

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
    def __init__(self, tile):
        super(Deer, self).__init__(tile)

        self.speed = 10.0 #mph (top speed, escaping. can also jump 30 feet)
        self.type = AnimalType.prey
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
        self.gestation_period = 7 #months pregnant
        self.matingSeasons = [4,5] #may, june
        self.female_ratio = 0.75 # 3 female : 1 adult buck

        #For reproduction
        self.is_female = \
            True if (random.random() < self.female_ratio) else False
        self.next_spawning_year = -1
        self.next_spawning_day = None
        self.new_spawndate()

        # For eating
        self.consumptionRate = 8.22 # lbs/day from 3000 lbs/yr
        # self.birthRate = 0.0  # offspring per year, impl in reproduce()

        # For drinking
        self.avg_summer_temp = 70 #deg F
        self.avg_winter_temp = 35 #deg F
        self.winter_thirst_ratio = 0.00375 #gal water per 1 lb
        self.summer_thirst_ratio = 0.0075 #gal water per 1 lb
        self.min_thirst = self.weight * self.winter_thirst_ratio * 0.25
        self.days_without_water = 0


        # self.rememberedResources = []  # coords of water, food, etc.

        self.days_to_decompose = 90.0 # based on 3 months for a human
        self.days_deceased = 0.0

        # self.objectives = [] #inherited from animal


    def new_spawndate(self):
        '''Generate New Birthday
        A new birthday is calculated after a birthing/upon initialization.
        By choosing a random day within their mating season , and adding
        'gestation_period' days to that.
        '''
        start_mating = (self.matingSeasons[0] - 1) % 12 # non-inclusive
        end_mating = self.matingSeasons[-1]
        #
        mating_day = random.randint(
            Deer.CUMSUM_MONTHS[start_mating],
            Deer.CUMSUM_MONTHS[end_mating])
        #
        gestation = self.gestation_period * 30 # convert months to days

        # change birthday and deer
        self.next_spawning_day += 1
        self.next_spawning_day = (mating_day + gestation) % 365

    def update(self):
        '''Update Deer
        '''
        self.thirst = self.get_thirst_today()

        if (self.state == State.alive and
            self.old_age() == False): # deer alive
            #print("Update deer alive")
            # calculate thirst for the day
            self.move()
            self.eat()
            self.drink()
            # self.reproduce()
        elif (self.state == State.dead):
            # print("Update deer dead") # deer dead
            self.days_deceased += 1
            if self.days_deceased >= self.days_to_decompose:
                self.remove()

    def old_age(self):
        curDay = self.get_current_day()
        age = curDay - self.day_born
        if (age >= self.max_age):
            self.die()
            return True
        return False

    def die(self):
        self.state  = State.dead
    def move(self):
        '''Move Deer
        TODO: safely remove eat. move() simply relocates deer to place with
        most abundant grass.
        :return:
        '''
        tiles = self.tile.environment.get_adjacent(self.tile, int(self.speed))

        max_tile = self.tile
        # Get tile with the most Teff within sight distance

        for current_tile in tiles:
            teff = current_tile.get_agent(Teff)

            teff_amount = None

            if teff is not None:
                teff_amount = teff.get_amount()

            current_teff = max_tile.get_agent(Teff)

            current_teff_amount = 0.0

            if current_teff is not None:
                current_teff_amount = current_teff.get_amount()


            if teff_amount is not None and teff_amount > current_teff_amount:
                max_tile = current_tile

        #move deer to tile w/ most teff and set vars

        if max_tile != self.tile:
            self.tile.environment.agent_moved_to_tile(self, max_tile)

    def remove(self):
        self.tile.remove_agent(self)
        del self

    def eat(self):
        '''Eat Grass
        Eats the grass, modifies itself accordingly, and checks for hunger.

        With the current 1-lb-per-day implementation,
            biggest deer can last ~2 months straight, while
            smallest deer can last ~1 month straight without food

        deer survive a month with little or no food

        PreCond: Deer previously moved to tile with most abundant grass
        :return:
        '''

        #get teff
        teff_agent = self.tile.get_agent(Teff)

        if (teff_agent is None or teff_agent.current_weight <= 0):
            # teff empty/ starve case
            self.set_weight(self.weight-1) #starve a bit
            # self.thirst -= 1 #thirst a bit

            self.check_starve() # check for starvation here
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

            #decrease deer thirst for the day
            self.thirst -= self.consumptionRate * Teff.percent_water

    def get_thirst_today(self):
        ''' Calculate Thirst
        Determine gallons of water to drink on the current day via a
        linear function
        '''
        #get temperature
        x = self.tile.environment.current_day.temp #temperature, degF

        m = (self.summer_thirst_ratio - self.winter_thirst_ratio) \
            / (self.avg_summer_temp - self.avg_winter_temp) #slope

        b = self.summer_thirst_ratio - (m*self.avg_summer_temp) #y-intercept

        #linear function for thirst per lb with resp to temperature
        galPerLb = m * x + b# ratio of gal water needed for 1 lb

        #apply thirst ratio to deer's weight
        thirst = galPerLb * self.max_weight

        #account for small/negative thirst
        return max(thirst, self.min_thirst)

    def drink(self):
        '''Drink Water
        1 1/2 quarts (0.375 gal) for every 100 pounds of body weight per day during the
        winter. (0.00375 gal/lb)
        This requirement doubles during the summer, with deer needing
        about 3 quarts for every 100 pounds of body weight (0.0075 gal/lb)
        http://www.buckmanager.com/2012/07/31/whitetail-deer-water-requirements
         -and-deer-hunting/

        3 to 6 quarts of water a day, depending on the outside temperature
        (consistent with former data if looking at 200lb deer)
        http://www.huntingpa.com/deer_nutrition.html

        known to die 3 days without water
        http://www.huntingpa.com/deer_nutrition.html
        '''
        # thirst for the day is calculated by temperature
        # Deer should have already gotten some water from food

        # Drink remaining water from drinking_water source
        dwater_agent = self.tile.get_agent(DrinkingWater)

        if (dwater_agent is None
            or dwater_agent.get_amount() <= 0):
            # water absent/ thirst case
            #increment days without water
            self.days_without_water += 1
            if self.days_without_water >= 3:
                self.die()
        elif (dwater_agent.get_amount() <= self.min_thirst):
            #water insufficient, only a little closer to death
            #drink all & decrease thirst. does not alter weight.
            self.thirst -= dwater_agent.get_amount()
            dwater_agent.set_weight(0)

            #increment days without water by a little
            self.days_without_water += self.thirst/ self.get_thirst_today()
            if self.days_without_water >= 3:
                self.die()
        else:
            #water sufficient. Thirst satisfied. Death delayed
            new_volume = dwater_agent.get_amount() - self.thirst
            dwater_agent.set_weight(new_volume)
            self.thirst = 0
            if (self.days_without_water > 0):
                self.days_without_water -= 1

    def check_starve(self):
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
        '''
        if (self.is_female \
            and self.get_year() == self.next_spawning_year\
            and self.get_day() == self.next_spawning_day):
                #reproduce
                # give each a chance to birth 0-3 babies
                babies = random.randint(0,3)
                # place children on same tile as parent
                for i in range(babies):
                    baby = Deer(self.tile)
                    self.tile.add_agent(baby)
                self.new_spawndate()



class Wolf(Animal):

    def __init__(self, tile):
        super(Wolf, self).__init__(tile)


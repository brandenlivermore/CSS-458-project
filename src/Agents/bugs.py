import src.Agents.animal
from src.Agents.teff import Teff
from src.environment import Environment

################################################################################
#                       Bugs
################################################################################
#loosly based on desert locust this agent serves to purposes
#one- to show how easily a new agent can be added to the mode
#two- to simulate how a swarm could impact the teff and eventually
#       the deer populations of a model
#
#

class Bugs(src.Agents.animal.Animal):

    #source: http://www.fao.org/ag/locusts/en/info/info/faq/
    CONSUME_RATE = 0.1 #the rate a witch a swarm consumes itself
    BREED_INTERVAL = 17 #days between creating new broods
    BREED_INITIAL = 60 #days of life before first brood
    HATCH_TIME = 20 #time between broods
    MAX_BROODS = 3 #maxium amount of times a brood can have childern
    BROOD_SIZE = 3 #the amount of individuals let to hatch
    ADULT_SIZE = 0.01 #lbs
    NEWBORN_SIZE = 0.002 #lbs

    def __init__(self, tile ,weight=100):
        '''
            Method:
                Constructor for the Bugs Agent, uses the animal
        '''
        super().__init__(tile)
        self.weight = weight
        self.speed = 1
        self.type = type(self)
        self.individuals = self.weight / self.NEWBORN_SIZE
        self.day_alive = 0
        self.current_size = self.NEWBORN_SIZE
        self.hatch = -self.HATCH_TIME
        self.time_to_next_brood = 0
        self.broods = self.MAX_BROODS

    def consume(self):
        '''Dictates the behavior of the swarm as it eats

        :return: updates the values of the swarm and the teff agent they have consumed
        '''
        teff = self.tile.get_agent(Teff)
        if teff is not None:
            amount_eat = min(self.weight, teff.get_amount())
            teff.set_weight(teff.get_amount() - amount_eat)
            if self.current_size < self.ADULT_SIZE:
                self.current_size = self.current_size + ((amount_eat / self.weight) \
                    * self.current_size * ((self.ADULT_SIZE - self.NEWBORN_SIZE) / self.BREED_INITIAL))
            self.set_weight(self.current_size * self.individuals)
        else:
            self.individuals = self.individuals * (1 - self.CONSUME_RATE)
            self.set_weight(self.current_size * self.individuals)

    def breed(self):
        '''Behavior for breeding for the swarm

        :return: in cases where the brood is mature
        '''
        if self.day_alive >= self.BREED_INITIAL and self.time_to_next_brood <= 0:
            new_brood = Bugs(self.tile, self.NEWBORN_SIZE * self.individuals * self.BROOD_SIZE)
            self.tile.add_agent(new_brood)
            self.time_to_next_brood = self.BREED_INTERVAL
            self.broods -= 1
            if self.broods == 0:
                self.tile.remove_agent(self)
                del self
                return
        else:
            self.time_to_next_brood -= 1

    def update(self):
        if self.hatch >= 0:
            self.day_alive += 1
            self.consume()
            self.move()
            self.breed()

        else:
            self.hatch += 1

from Agents.agent import Agent

class Teff(Agent):

    #Constants for Teff Grass
    #sourced from http://teffgrass.com/harvesting-teff/
    growing_sun = 8.2 #hours a day
    water_consume_acres = 1785 #gallons
    ideal_temp = 63.275 #in degrees celsius
    min_temp = 32.1 #in degrees celsius
    min_sun = 4.32 #hours per day
    max_heat = 100 #degrees celsius
    seed_date = [225,175] #day of year teff tests to seed
    max_per_acre = 16000 #pounds
    threshold_acre = 177 #pounds
    death_chance = .01 #chance teff is wiped out if below threshold
    seed = 0.5 #base chance of seeding adjacent tiles
    updates = True
    
    def __init__(self):
        # for initial test 
        self.amount = Teff.max_per_acre

    def update(self):
        pass

    def get_amount(self):
        return self.amount
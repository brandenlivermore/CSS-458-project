from Agents.agent import Agent

class Teff(Agent):

    #Constants for Teff Grass
    #sourced from http://teffgrass.com/harvesting-teff/
    teff_growing_sun = 8.2 #hours a day
    teff_water_consume_acres = 1785 #gallons
    teff_ideal_temp = 63.275 #in degrees celsius
    teff_min_temp = 32.1 #in degrees celsius
    teff_min_sun = 4.32 #hours per day
    teff_max_heat = 100 #degrees celsius
    teff_seed_date = [225,175] #day of year teff tests to seed
    max_teff_acre = 16000 #pounds
    teff_threshold_acre = 177 #pounds
    teff_death_chance = .01 #chance teff is wiped out if below threshold

    def update(self):
        pass
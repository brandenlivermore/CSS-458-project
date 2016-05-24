from src.Agents.agent import Agent


class GroundWater(Agent):

    def __init__(self, enviro_in):
        self.my_environment = enviro_in
        self.water_volume = 0 #in gallons
        self.my_environment.agent_totals[type(self)][1] = 1

    def set_weight(self, new_volume):
        if new_volume < 0:
            raise Exception("You cannot do that!")

        difference = new_volume - self.water_volume

        self.my_environment.agent_totals[type(self)][1] = new_volume / 1000.0
        self.water_volume = new_volume

    def get_amount(self):
        return self.water_volume
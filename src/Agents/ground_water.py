from src.Agents.agent import Agent


class GroundWater(Agent):

    #groundwater constants
    max_volume_acre = 500000 #gallons per acer

    def __init__(self, enviro_in):
        self.my_environment = enviro_in
        self.water_volume = 0 #in gallons
        self.max_volume = self.max_volume_acre * enviro_in.width * enviro_in.height

    def set_weight(self, new_volume):
        if new_volume < 0:
            raise Exception("You cannot do that!")

        difference = min(new_volume, self.max_volume)- self.water_volume

        self.my_environment.update_total_mass_and_count(type(self), difference / 1000.0, count_difference=0)
        self.water_volume = min(new_volume, self.max_volume)

    def get_amount(self):
        return self.water_volume
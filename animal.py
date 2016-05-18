class animal(object):
    def __init__(self):
        self.hunger = 0.0
        self.speed = 0.0
        self.health = 0.0
        self.type = None #"Predator" or "prey"
        self.age = 0

        self.rememberedResources = [] #coords of water, food, etc.
        self.consumptionRate = 0.0

    def update(self):
        pass

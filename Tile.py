class Tile(object):

    #contants for the state of the land
    teff_coverage = 0 #percent of land covered in teff
    teff_mass = 0     #mass of teff on land in lbs
    reservoir = False  #does reservoir exist on tile
    well = False        #does a well exist
    tree_coverage =0 #coverage of trees on tile
    tree_mass = 0   #mass of trees in lbs
    reservoir_volume = 0 #volume of reservoir in gallons
    well_volume = 0 #gallons
    soil_type = None #soil type
    environment = None #the environment

    #tile location
    tile_x = 0
    tile_y = 0

    #animals info
    list_animals = []

    def __init__(self, add_reservoir, soil_in, well_in, eviro_in):
        self.reservoir = add_reservoir
        self.soil_type = soil_in
        self.environment = eviro_in
        self.well = well_in

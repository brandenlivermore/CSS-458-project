import unittest
import math

from src.weathermodel import WeatherModel
from src.Agents.animal import Deer
from src.tile import Tile
from src.environment import Environment
from src.Agents.teff import Teff
from src.Agents.animal import State
from src.Agents.soil import Soil

class TestUM(unittest.TestCase):

    def setUp(self):
        self.w1 = WeatherModel(1)
        self.w2 = WeatherModel(2)
        self.e1 = Environment(10,15)
        self.e2 = Environment(20,25)

        loc = [2, 1]
        self.tile = self.e1.get_tile(loc)
        self.teff1 = Teff(self.tile)

        # self.d1 = Deer(self.tile)

    def tearDown(self):
        pass

    # Weather Model Tests
    def test_weatherModel_days_in_year(self):
        self.assertEqual(self.w1.totalDays, 365, "Total days is incorrect")
        self.assertEqual(self.w2.totalDays, 730, "Total days is incorrect")

    def test_weatherModel_years(self):
        self.assertEqual(self.w1.numYears, 1, "Number of years is incorrect")
        self.assertEqual(self.w2.numYears, 2, "Number of years is incorrect")

    def test_weatherModel_days_property(self):
        self.assertEqual(self.w1.totalDays, len(self.w1.days), "Total days must equal length of day property")

    def test_weatherModel_sunlight(self):
        for i in range(0, self.w1.days.size):
            self.assertLess(self.w1.days[i].sun, 24, "A day cannot have more than 24 hours of sunlight")
            self.assertGreater(self.w1.days[0].sun, 0, "A day cannot have less than 0 hours of sunlight")

        for i in range(0, self.w2.days.size):
            self.assertLess(self.w2.days[i].sun, 24, "A day cannot have more than 24 hours of sunlight")
            self.assertGreater(self.w2.days[0].sun, 0, "A day cannot have less than 0 hours of sunlight")

    def test_weatherModel_precipitation(self):
        for i in range(0, self.w1.days.size):
            self.assertGreaterEqual(self.w1.days[0].rain, 0, "A day cannot have less than 0 inches of precipitation")

        for i in range(0, self.w2.days.size):
            self.assertGreaterEqual(self.w2.days[0].rain, 0, "A day cannot have less than 0 inches of precipitation")

    # Environment Tests
    def test_environment_width(self):
        self.assertEqual(self.e1.width, 10, "Initial width for e1 is 10")
        self.assertEqual(self.e2.width, 20, "Initial width for e2 is 20")

    def test_environment_height(self):
        self.assertEqual(self.e1.height, 15, "Initial height for e1 is 15")
        self.assertEqual(self.e2.height, 25, "Initial height for e2 is 25")

    def test_environment_teff_mass(self):
        self.assertEqual(self.e1.teff_total_mass, 0, "Initial mass for e1 is 0")
        self.assertEqual(self.e2.teff_total_mass, 0, "Initial mass for e2 is 0")

    def test_environment_valid_location(self):
        loc1 = [2,2]
        self.assertEqual(self.e1.is_location_valid(loc1), True, "Location [2, 2] is valid")
        self.assertEqual(self.e2.is_location_valid(loc1), True, "Location [2, 2] is valid")

        loc2 = [-1, -1]
        self.assertEqual(self.e1.is_location_valid(loc2), False, "Location [-1, -1] is invalid")
        self.assertEqual(self.e2.is_location_valid(loc2), False, "Location [-1, -1] is invalid")

        loc3 = [-1, 1]
        self.assertEqual(self.e1.is_location_valid(loc3), False, "Location [-1, 1] is invalid")
        self.assertEqual(self.e2.is_location_valid(loc3), False, "Location [-1, 1] is invalid")

        loc4 = [1, -1]
        self.assertEqual(self.e1.is_location_valid(loc4), False, "Location [1, -1] is invalid")
        self.assertEqual(self.e2.is_location_valid(loc4), False, "Location [1, -1] is invalid")

        loc5 = [40, 40]
        self.assertEqual(self.e1.is_location_valid(loc5), False, "Location [40, 40] is invalid")
        self.assertEqual(self.e2.is_location_valid(loc5), False, "Location [40, 40] is invalid")

    def test_environment_distance(self):
        loc1 = [0, 1]
        loc2 = [0, 2]
        loc3 = [0, 3]
        loc4 = [-1, 1]
        loc5 = [1, 2]

        self.assertEqual(self.e1.get_distance(loc1, loc2), 1, "Distance is one")
        self.assertEqual(self.e2.get_distance(loc1, loc2), 1, "Distance is one")

        self.assertEqual(self.e1.get_distance(loc1, loc3), 2, "Distance is two")
        self.assertEqual(self.e2.get_distance(loc1, loc3), 2, "Distance is two")

        self.assertEqual(self.e1.get_distance(loc1, loc4), 1, "Distance is one")
        self.assertEqual(self.e2.get_distance(loc1, loc4), 1, "Distance is one")

        self.assertEqual(self.e1.get_distance(loc1, loc5), math.sqrt(2), "Distance is square root of two")
        self.assertEqual(self.e2.get_distance(loc1, loc5), math.sqrt(2), "Distance is square root of two")


        self.assertEqual(self.e1.get_distance(loc2, loc1), 1, "Distance is one")
        self.assertEqual(self.e2.get_distance(loc2, loc1), 1, "Distance is one")

        self.assertEqual(self.e1.get_distance(loc3, loc1), 2, "Distance is two")
        self.assertEqual(self.e2.get_distance(loc3, loc1), 2, "Distance is two")

        self.assertEqual(self.e1.get_distance(loc4, loc1), 1, "Distance is one")
        self.assertEqual(self.e2.get_distance(loc4, loc1), 1, "Distance is one")

        self.assertEqual(self.e1.get_distance(loc5, loc1), math.sqrt(2), "Distance is square root of two")
        self.assertEqual(self.e2.get_distance(loc5, loc1), math.sqrt(2), "Distance is square root of two")

    def test_environment_tile_location(self):
        loc1 = [2, 1]
        t1 = self.e1.get_tile(loc1)
        t2 = self.e2.get_tile(loc1)

        self.assertEqual(t1.tile_x, 2, "X coordinate is 2")
        self.assertEqual(t1.tile_y, 1, "Y coordinate is 1")

        self.assertEqual(t2.tile_x, 2, "X coordinate is 2")
        self.assertEqual(t2.tile_y, 1, "Y coordinate is 1")


        loc2 = [-1 ,1]
        t3 = self.e1.get_tile(loc2)
        t4 = self.e2.get_tile(loc2)

        self.assertEqual(t3, None, "-1 is and invalid x coordinate")
        self.assertEqual(t4, None, "-1 is and invalid x coordinate")


    # Teff tests
    def test_teff_initial_weight(self):
        self.assertEqual(self.teff1.current_weight, 167, "Initial weight is 167 pounds")
        self.assertEqual(self.teff1.get_amount(), 167, "Initial weight is 167 pounds")

    # def test_teff_weight_change(self):
    #     newWeight = 10
    #     self.teff1.set_weight(newWeight)
    #
    #     self.assertEqual(self.teff1.current_weight, newWeight, "Weight must be updated by set_weight method")
    #
    #     self.teff1.set_weight(-1)
    #
    #     self.assertEqual(self.teff1.current_weight, newWeight, "Weight cannot be updated to be negative")
    #     self.assertNotEqual(self.teff1.current_weight, -1, "Weight cannot be negative")

    def test_teff_update(self):
        self.teff1.updates = False

        self.assertEqual(self.teff1.update(), None, "Updates is set to false")

    # Deer Tests
    def test_deer_initial_weight(self):
        self.assertLess(self.d1.weight, 300, "Starting weight must be less than 300 pounds")
        self.assertGreaterEqual(self.d1.weight, 110,
                                "Starting weight must be greater or equal to 110 pounds")

    def test_deer_starve(self):

        self.assertEqual(self.d1.state, State.alive, "Deer should be alive")

        self.d1.weight = self.d1.max_weight * 0.6
        self.d1.check_starve()

        self.assertEqual(self.d1.state, State.dead, "Deer should die once it's weight is below 70% of it's max weight")

        self.d1.weight = self.d1.max_weight
        self.d1.check_starve()

        self.assertEqual(self.d1.state, State.dead, "Animal state should not change from dead to alive")

    # Tile Tests
    def test_tile_location(self):
        self.assertEqual(self.tile.tile_x, 2, "Tile's x location is set to 2 in set up method")
        self.assertEqual(self.tile.tile_y, 1, "Tile's y location is set to 1 in set up method")

    def test_tile_add_agent(self):
        preAgents = len(self.tile.agent_mapping)
        self.tile.add_agent(self.d1)
        postAgents = len(self.tile.agent_mapping)
        self.assertGreater(postAgents, preAgents,
                           "Adding an agent to a tile should increase agent_mapping")

    def test_tile_weight_changed(self):
        s = Soil(1, self.tile)
        preWeight = self.tile.get_mass_and_totals()
        self.tile.weight_changed(type(s), 10)
        postWeight = self.tile.get_mass_and_totals()
        self.assertNotEqual(preWeight,postWeight, "Adding weight should change total mass")

if __name__ == '__main__':
    unittest.main()

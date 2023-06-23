import unittest
from tempest.simulation import TempestSimulator
from tempest.errors import SimulationException


class TestR1(unittest.TestCase):

    def setUp(self):
        self._ts = TempestSimulator()

    def test_add_name(self):
        self._ts.add_city("City1", 25, 7)
        self._ts.add_village("Village1", 9, 4)
        self.assertEqual("City1", self._ts.get_location("City1").name)
        self.assertEqual("Village1", self._ts.get_location("Village1").name)

    def test_add_properties(self):
        self._ts.add_city("City1", 25, 7)
        self._ts.add_village("Village1", 9, 4)

        city = self._ts.get_location("City1")
        village = self._ts.get_location("Village1")

        self.assertEqual([25, 7], [city.value, city.resilience])
        self.assertEqual([9, 4], [village.value, village.resilience])

    def test_str(self):
        self._ts.add_city("City1", 25, 7)
        self._ts.add_village("Village1", 9, 4)
        self.assertEqual("City City1", str(self._ts.get_location("City1")))
        self.assertEqual("Village Village1", str(self._ts.get_location("Village1")))

    def test_add_multiple(self):
        self._ts.add_city("City1", 25, 7)
        self._ts.add_city("City2", 15, 3)
        self._ts.add_village("Village1", 9, 4)
        self._ts.add_village("Village2", 22, 1)

        self.assertEqual("City1", self._ts.get_location("City1").name)
        self.assertEqual("City2", self._ts.get_location("City2").name)
        self.assertEqual("Village1", self._ts.get_location("Village1").name)
        self.assertEqual("Village2", self._ts.get_location("Village2").name)

    def test_add_multiple_properties(self):
        self._ts.add_city("City1", 25, 7)
        self._ts.add_city("City2", 15, 3)
        self._ts.add_village("Village1", 9, 4)
        self._ts.add_village("Village2", 22, 1)

        city1 = self._ts.get_location("City1")
        city2 = self._ts.get_location("City2")
        village1 = self._ts.get_location("Village1")
        village2 = self._ts.get_location("Village2")

        self.assertEqual([25, 7], [city1.value, city1.resilience])
        self.assertEqual([15, 3], [city2.value, city2.resilience])
        self.assertEqual([9, 4], [village1.value, village1.resilience])
        self.assertEqual([22, 1], [village2.value, village2.resilience])


class TestR2(unittest.TestCase):

    def setUp(self):
        self._ts = TempestSimulator()
        self._ts.add_city("City1", 25, 6)
        self._ts.add_village("Village1", 9, 4)
        self._city = self._ts.get_location("City1")
        self._village = self._ts.get_location("Village1")

    def test_damage_village(self):
        self.assertAlmostEqual((5-4)/10 * 9, self._village.simulate_damage(5))

    def test_damage_city(self):
        self._city.set_damage_function(lambda x: (x/10)**2)
        self.assertAlmostEqual((8/10) ** 2 * 25, self._city.simulate_damage(8))

    def test_damage_city_exception(self):
        self.assertRaises(SimulationException, self._city.simulate_damage, 2)
        self._city.set_damage_function(lambda x: x/10)
        self._city.simulate_damage(8)

    def test_damage_village_exception(self):
        self._village.simulate_damage(3)
        self.assertRaises(SimulationException, self._village.set_damage_function, lambda x: x/10)

    def test_damage_thresholds_city(self):
        self._city.set_damage_function(lambda x: (x / 10) ** 2)
        self.assertAlmostEqual(0, self._city.simulate_damage(5))
        self.assertGreater(self._city.simulate_damage(8), 0)
        self.assertAlmostEqual(0, self._village.simulate_damage(0))


class TestR3(unittest.TestCase):

    def setUp(self):
        self._ts = TempestSimulator()
        self._ts.add_city("City1", 25, 6)
        self._ts.add_city("City2", 15, 3)
        self._ts.add_village("Village1", 9, 4)
        self._ts.add_village("Village2", 22, 1)

    def test_set_next(self):
        self._ts.set_next("City1", "Village1", 0.9)
        self._ts.set_next("City2", "City1", 0.8)
        self._ts.set_next("Village1", "Village2", 0.7)

        self.assertEqual("City1", self._ts.get_next("City2")[0].name)
        self.assertEqual("Village1", self._ts.get_next("City1")[0].name)
        self.assertEqual("Village2", self._ts.get_next("Village1")[0].name)

    def test_next_attenuation(self):
        self._ts.set_next("City1", "Village1", 0.9)
        self._ts.set_next("City2", "City1", 0.8)
        self._ts.set_next("Village1", "Village2", 0.7)

        self.assertAlmostEqual(0.8, self._ts.get_next("City2")[1])
        self.assertAlmostEqual(0.9, self._ts.get_next("City1")[1])
        self.assertAlmostEqual(0.7, self._ts.get_next("Village1")[1])

    def test_next_missing(self):
        self._ts.set_next("City1", "Village1", 0.9)
        self.assertIsNone(self._ts.get_next("Village1"))
        self.assertIsNotNone(self._ts.get_next("City1"))


class TestR4(unittest.TestCase):

    def setUp(self) -> None:
        self._ts = TempestSimulator()
        self._ts.add_city("City1", 25, 6)
        self._ts.add_city("City2", 15, 3)
        self._ts.add_village("Village1", 9, 4)
        self._ts.add_village("Village2", 22, 1)

        self._ts.set_next("City2", "City1", 0.7)
        self._ts.set_next("City1", "Village1", 0.9)
        self._ts.set_next("Village1", "Village2", 0.5)

        self._ts.get_location("City1").set_damage_function(lambda x: (x / 10))
        self._ts.get_location("City2").set_damage_function(lambda x: (x / 10))

    def test_get_affected(self):
        locations = [loc.name for loc in self._ts.get_affected("City2")]
        self.assertEqual(["City2", "City1", "Village1", "Village2"], locations)

    def test_get_total_damage(self):
        damage = self._ts.get_total_damage("City2", 10.0)
        answer = 15 * (10 / 10) + 25 * (0.7 * 10 / 10) + 9 * ((0.9 * 0.7 * 10 - 4) / 10) + 22 * (
                    (0.9 * 0.7 * 0.5 * 10 - 1) / 10)
        self.assertAlmostEqual(answer, damage)

    def test_get_affected_complex(self):
        locations = [loc.name for loc in self._ts.get_affected("City1")]
        self.assertEqual(["City1", "Village1", "Village2"], locations)

    def test_get_total_damage_complex(self):
        damage = self._ts.get_total_damage("City2", 6)
        answer = 15 * (6 / 10) + 25 * 0 + 9 * 0 + 22 * ((0.7 * 0.9 * 0.5 * 6 - 1) / 10)
        self.assertAlmostEqual(answer, damage)


class TestR5(unittest.TestCase):

    def setUp(self) -> None:
        self._ts = TempestSimulator()
        self._ts.add_city("City1", 25, 7)
        self._ts.add_city("City2", 15, 3)
        self._ts.add_village("Village1", 9, 4)
        self._ts.add_village("Village2", 22, 1)

        self._ts.set_next("Village1", "Village2", 0.5)
        self._ts.set_next("City1", "Village1", 0.9)
        self._ts.set_next("City2", "City1", 0.7)

    def test_add_location_middle_after(self):
        self._ts.add_city("New_City", 1, 1)
        self._ts.add_location(to_insert="New_City", location_before="City2", attenuation=0.5)
        loc, dmp = self._ts.get_next("New_City")
        self.assertEqual("City1", loc.name)
        self.assertAlmostEqual(0.5, dmp)

    def test_add_location_middle_before(self):
        self._ts.add_city("New_City", 1, 1)
        self._ts.add_location(to_insert="New_City", location_before="City2", attenuation=0.5)
        loc, dmp = self._ts.get_next("City2")
        self.assertEqual("New_City", loc.name)
        self.assertAlmostEqual(0.7, dmp)

    def test_add_location_end_after(self):
        self._ts.add_city("New_City", 1, 1)
        self._ts.add_location(to_insert="New_City", location_before="Village2", attenuation=0.5)
        next_loc = self._ts.get_next("New_City")
        self.assertIsNone(next_loc)

    def test_add_location_end_before(self):
        self._ts.add_city("New_City", 1, 1)
        self._ts.add_location(to_insert="New_City", location_before="Village2", attenuation=0.5)
        loc, dmp = self._ts.get_next("Village2")
        self.assertEqual("New_City", loc.name)
        self.assertAlmostEqual(0.5, dmp)


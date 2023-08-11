#!/usr/bin/python3
"""Defines unittests for models/city.py."""
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """Test cases for class city instantiation."""

    # Tests that a new city instance can be created.
    def test_city_instantiates(self):
        self.assertEqual(City, type(City()))

    # Tests that new city instance is stored in objects.
    def test_new_city_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    # Tests that city instance id is a public attribute.
    def test_city_id_is_public_attr(self):
        self.assertEqual(str, type(City().id))

    # Tests that city creation time is public.
    def test_city_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    # Tests that city updated time is public attribute.
    def test_city_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    # Tests that city state_id is public attribute.
    def test_city_state_id_is_public_attr(self):
        self.assertEqual(str, type(City.state_id))

    # Tests that city name is public attribute.
    def test_city_name_is_public_attr(self):
        self.assertEqual(str, type(City.name))

    # Tests that cities instantiate with different unique ids.
    def test_cities_instantiated_unique_ids(self):
        city1 = City()
        city2 = City()
        self.assertNotEqual(city1.id, city2.id)

    # Tests that two or more cities are created at different times.
    def test_cities_different_created_at(self):
        City1 = City()
        sleep(0.05)
        City2 = City()
        self.assertLess(City1.created_at, City2.created_at)

    # Tests that two or more cities are updated at different times.
    def test_cities_different_updated_at(self):
        City1 = City()
        sleep(0.05)
        city2 = City()
        self.assertLess(City1.updated_at, city2.updated_at)

    # Tests that city string representation can be output.
    def test_city_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        city = City()
        city.id = "14151624"
        city.created_at = city.updated_at = dt
        city_str = city.__str__()
        self.assertIn("[City] (14151624)", city_str)
        self.assertIn("'id': '14151624'", city_str)
        self.assertIn("'created_at': " + dt_repr, city_str)
        self.assertIn("'updated_at': " + dt_repr, city_str)

    # Tests that city doesn't save a None argument
    #  as value in the dictionary.
    def test_city_None_arg(self):
        city = City(None)
        self.assertNotIn(None, city.__dict__.values())

    # Tests that city instantiates with kwargs.
    def test_city_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        city = City(id="1017", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(city.id, "1017")
        self.assertEqual(city.created_at, dt)
        self.assertEqual(city.updated_at, dt)

    # Tests that city raises an exception when None as a value in kwargs.
    def test_city_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Test cases for save method."""

    # Tests that updated city is saved at the current time.
    def test_city_updated_at_saved(self):
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        self.assertLess(first_updated_at, city.updated_at)

    # Tests that two or more cities updates are saved at different times.
    def test_two_cities_updates_saved(self):
        city = City()
        sleep(0.05)
        first_updated_at = city.updated_at
        city.save()
        second_updated_at = city.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        city.save()
        self.assertLess(second_updated_at, city.updated_at)

    # Tests that save city with a None argument raises an exception.
    def test_city_save_with_None_argument(self):
        city = City()
        with self.assertRaises(TypeError):
            city.save(None)

    # Tests that save city updates the __file_path(JSON file)
    #  in the file_storage.
    def test_city_save_updates_file(self):
        city = City()
        city.save()
        city_id = "City." + city.id
        with open("file.json", "r") as f:
            self.assertIn(city_id, f.read())


class TestCity_to_dict(unittest.TestCase):
    """Test cases for to_dict method."""

    # Tests that city instance is returned as a dictionary.
    def test_city_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    # Tests that to_dict contains correct city keys.
    def test_city_to_dict_keys(self):
        city = City()
        self.assertIn("id", city.to_dict())
        self.assertIn("created_at", city.to_dict())
        self.assertIn("updated_at", city.to_dict())
        self.assertIn("__class__", city.to_dict())

    # Tests that to_dict contains added city attributes
    def test_city_to_dict_added_attributes(self):
        city = City()
        city.region = "Southside"
        city.year_established = 1788
        self.assertEqual("Southside", city.region)
        self.assertIn("year_established", city.to_dict())

    # Tests that to_dict has city datetime attributes as strings.
    def test_city_to_dict_datetime_attributes_type(self):
        city = City()
        city_dict = city.to_dict()
        self.assertEqual(str, type(city_dict["id"]))
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    # Tests that to_dict returns a dictionary with
    #  city attributes(keys and values)
    def test_city_to_dict_valid_attr(self):
        dt = datetime.today()
        city = City()
        city.id = "14151624"
        city.created_at = city.updated_at = dt
        citydict = {
            'id': '14151624',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(city.to_dict(), citydict)

    # Tests that to_dict returns a different city dictionary compared
    #  to the class __dict__ representation.
    def test_city_to_dict_with_class__dict__(self):
        city = City()
        self.assertNotEqual(city.to_dict(), city.__dict__)

    # Tests that to_dict raises an exception when a None argument
    #  is passed in the city class.
    def test_city_to_dict_with_None_argument(self):
        city = City()
        with self.assertRaises(TypeError):
            city.to_dict(None)


if __name__ == "__main__":
    unittest.main()

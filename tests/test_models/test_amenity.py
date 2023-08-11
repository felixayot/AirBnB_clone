#!/usr/bin/python3
"""Defines unittests for models/amenity.py."""
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Test cases for class amenity instantiation."""

    # Tests that a new amenity instance can be created.
    def test_amenity_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    # Tests that new amenity instance is stored in objects.
    def test_new_amenity_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    # Tests that amenity instance id is a public attribute.
    def test_amenity_id_is_public_attr(self):
        self.assertEqual(str, type(Amenity().id))

    # Tests that amenity creation time is public.
    def test_amenity_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    # Tests that amenity updated time is public attribute.
    def test_amenity_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    # Tests that amenity name is public attribute.
    def test_amenity_name_is_public_attr(self):
        self.assertEqual(str, type(Amenity.name))

    # Tests that amenities instantiate with different unique ids.
    def test_amenities_instantiated_unique_ids(self):
        amenity1 = Amenity()
        amenity2 = Amenity()
        self.assertNotEqual(amenity1.id, amenity2.id)

    # Tests that two or more amenities are created at different times.
    def test_amenities_different_created_at(self):
        amenity1 = Amenity()
        sleep(0.05)
        amenity2 = Amenity()
        self.assertLess(amenity1.created_at, amenity2.created_at)

    # Tests that two or more amenities are updated at different times.
    def test_amenities_different_updated_at(self):
        amenity1 = Amenity()
        sleep(0.05)
        amenity2 = Amenity()
        self.assertLess(amenity1.updated_at, amenity2.updated_at)

    # Tests that amenity string representation can be output.
    def test_amenity_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        amenity = Amenity()
        amenity.id = "14151624"
        amenity.created_at = amenity.updated_at = dt
        amenity_str = amenity.__str__()
        self.assertIn("[Amenity] (14151624)", amenity_str)
        self.assertIn("'id': '14151624'", amenity_str)
        self.assertIn("'created_at': " + dt_repr, amenity_str)
        self.assertIn("'updated_at': " + dt_repr, amenity_str)

    # Tests that amenity doesn't save a None argument
    #  as value in the dictionary.
    def test_amenity_None_arg(self):
        amenity = Amenity(None)
        self.assertNotIn(None, amenity.__dict__.values())

    # Tests that amenity instantiates with kwargs.
    def test_amenity_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        amenity = Amenity(id="1017", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(amenity.id, "1017")
        self.assertEqual(amenity.created_at, dt)
        self.assertEqual(amenity.updated_at, dt)

    # Tests that amenity raises an exception when None as a value in kwargs.
    def test_amenity_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Test cases for save method."""

    # Tests that updated amenity is saved at the current time.
    def test_amenity_updated_at_saved(self):
        amenity = Amenity()
        sleep(0.05)
        first_updated_at = amenity.updated_at
        amenity.save()
        self.assertLess(first_updated_at, amenity.updated_at)

    # Tests that two or more amenities updates are saved at different times.
    def test_two_amenities_updates_saved(self):
        amenity = Amenity()
        sleep(0.05)
        first_updated_at = amenity.updated_at
        amenity.save()
        second_updated_at = amenity.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amenity.save()
        self.assertLess(second_updated_at, amenity.updated_at)

    # Tests that save amenity with a None argument raises an exception.
    def test_amenity_save_with_None_argument(self):
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.save(None)

    # Tests that save amenity updates the __file_path(JSON file)
    #  in the file_storage.
    def test_amenity_save_updates_file(self):
        amenity = Amenity()
        amenity.save()
        amenity_id = "Amenity." + amenity.id
        with open("file.json", "r") as f:
            self.assertIn(amenity_id, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Test cases for to_dict method."""

    # Tests that amenity instance is returned as a dictionary.
    def test_amenity_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    # Tests that to_dict contains correct amenity keys.
    def test_amenity_to_dict_keys(self):
        amenity = Amenity()
        self.assertIn("id", amenity.to_dict())
        self.assertIn("created_at", amenity.to_dict())
        self.assertIn("updated_at", amenity.to_dict())
        self.assertIn("__class__", amenity.to_dict())

    # Tests that to_dict contains added amenity attributes
    def test_amenity_to_dict_added_attributes(self):
        amenity = Amenity()
        amenity.nature = "Falls"
        amenity.year_discovered = 1788
        self.assertEqual("Falls", amenity.nature)
        self.assertIn("year_discovered", amenity.to_dict())

    # Tests that to_dict has amenity datetime attributes as strings.
    def test_amenity_to_dict_datetime_attributes_type(self):
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertEqual(str, type(amenity_dict["id"]))
        self.assertEqual(str, type(amenity_dict["created_at"]))
        self.assertEqual(str, type(amenity_dict["updated_at"]))

    # Tests that to_dict returns a dictionary with
    #  amenity attributes(keys and values)
    def test_amenity_to_dict_valid_attr(self):
        dt = datetime.today()
        amenity = Amenity()
        amenity.id = "14151624"
        amenity.created_at = amenity.updated_at = dt
        amenitydict = {
            'id': '14151624',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(amenity.to_dict(), amenitydict)

    # Tests that to_dict returns a different amenity dictionary compared
    #  to the class __dict__ representation.
    def test_amenity_to_dict_with_class__dict__(self):
        amenity = Amenity()
        self.assertNotEqual(amenity.to_dict(), amenity.__dict__)

    # Tests that to_dict raises an exception when a None argument
    #  is passed in the amenity class.
    def test_amenity_to_dict_with_None_argument(self):
        amenity = Amenity()
        with self.assertRaises(TypeError):
            amenity.to_dict(None)


if __name__ == "__main__":
    unittest.main()

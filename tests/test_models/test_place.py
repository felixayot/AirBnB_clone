#!/usr/bin/python3
"""Defines unittests for models/place.py."""
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_instantiation(unittest.TestCase):
    """Test cases for class place instantiation."""

    # Tests that a new place instance can be created.
    def test_place_instantiates(self):
        self.assertEqual(Place, type(Place()))

    # Tests that new place instance is stored in objects.
    def test_new_place_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    # Tests that place instance id is a public attribute.
    def test_place_id_is_public_attr(self):
        self.assertEqual(str, type(Place().id))

    # Tests that place creation time is public.
    def test_place_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    # Tests that place updated time is public attribute.
    def test_place_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    # Tests that place city_id is public attribute.
    def test_place_city_id_is_public_attr(self):
        self.assertEqual(str, type(Place.city_id))

    # Tests that place user id is public attribute.
    def test_place_user_id_is_public_attr(self):
        self.assertEqual(str, type(Place.user_id))

    # Tests that place name is public attribute.
    def test_place_name_is_public_attr(self):
        self.assertEqual(str, type(Place.name))

    # Tests that place description is public attribute.
    def test_place_description_is_public_attr(self):
        self.assertEqual(str, type(Place.description))

    # Tests that place number_rooms is public attribute.
    def test_place_number_rooms_is_public_attr(self):
        self.assertEqual(int, type(Place.number_rooms))

    # Tests that place number_bathrooms is public attribute.
    def test_place_number_bathrooms_is_public_attr(self):
        self.assertEqual(int, type(Place.number_bathrooms))

    # Tests that place number_rooms is public attribute.
    def test_place_max_guests_is_public_attr(self):
        self.assertEqual(int, type(Place.max_guests))

    # Tests that place price_by_night is public attribute.
    def test_place_price_by_night_is_public_attr(self):
        self.assertEqual(int, type(Place.price_by_night))

    # Tests that place latitude is public attribute.
    def test_place_latitude_is_public_attr(self):
        self.assertEqual(float, type(Place.latitude))

    # Tests that place longitude is public attribute.
    def test_place_longitude_is_public_attr(self):
        self.assertEqual(float, type(Place.longitude))

    # Tests that place amenity_ids is public attribute.
    def test_place_amenity_ids_is_public_attr(self):
        self.assertEqual(list, type(Place.amenity_ids))

    # Tests that places instantiate with different unique ids.
    def test_places_instantiated_unique_ids(self):
        place1 = Place()
        place2 = Place()
        self.assertNotEqual(place1.id, place2.id)

    # Tests that two or more places are created at different times.
    def test_places_different_created_at(self):
        place1 = Place()
        sleep(0.05)
        place2 = Place()
        self.assertLess(place1.created_at, place2.created_at)

    # Tests that two or more places are updated at different times.
    def test_places_different_updated_at(self):
        place1 = Place()
        sleep(0.05)
        place2 = Place()
        self.assertLess(place1.updated_at, place2.updated_at)

    # Tests that place string representation can be output.
    def test_place_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        place = Place()
        place.id = "14151624"
        place.created_at = place.updated_at = dt
        place_str = place.__str__()
        self.assertIn("[Place] (14151624)", place_str)
        self.assertIn("'id': '14151624'", place_str)
        self.assertIn("'created_at': " + dt_repr, place_str)
        self.assertIn("'updated_at': " + dt_repr, place_str)

    # Tests that place doesn't save a None argument
    #  as value in the dictionary.
    def test_place_None_arg(self):
        place = Place(None)
        self.assertNotIn(None, place.__dict__.values())

    # Tests that place instantiates with kwargs.
    def test_place_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        place = Place(id="1017", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(place.id, "1017")
        self.assertEqual(place.created_at, dt)
        self.assertEqual(place.updated_at, dt)

    # Tests that place raises an exception when None as a value in kwargs.
    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    """Test cases for save method."""

    # Tests that updated place is saved at the current time.
    def test_place_updated_at_saved(self):
        place = Place()
        sleep(0.05)
        first_updated_at = place.updated_at
        place.save()
        self.assertLess(first_updated_at, place.updated_at)

    # Tests that two or more place updates are saved at different times.
    def test_two_place_updates_saved(self):
        place = Place()
        sleep(0.05)
        first_updated_at = place.updated_at
        place.save()
        second_updated_at = place.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        place.save()
        self.assertLess(second_updated_at, place.updated_at)

    # Tests that save place with a None argument raises an exception.
    def test_place_save_with_None_argument(self):
        place = Place()
        with self.assertRaises(TypeError):
            place.save(None)

    # Tests that save place updates the __file_path(JSON file)
    #  in the file_storage.
    def test_place_save_updates_file(self):
        place = Place()
        place.save()
        place_id = "Place." + place.id
        with open("file.json", "r") as f:
            self.assertIn(place_id, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """Test cases for to_dict method of the place class."""

    # Tests that place instance is returned as a dictionary.
    def test_place_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    # Tests that to_dict contains correct place keys.
    def test_place_to_dict_keys(self):
        place = Place()
        self.assertIn("id", place.to_dict())
        self.assertIn("created_at", place.to_dict())
        self.assertIn("updated_at", place.to_dict())
        self.assertIn("__class__", place.to_dict())

    # Tests that to_dict contains added place attributes
    def test_place_to_dict_added_attributes(self):
        place = Place()
        place.rooms = "Bedroom"
        place.number_of_beds = 6
        self.assertEqual("Bedroom", place.rooms)
        self.assertIn("number_of_beds", place.to_dict())

    # Tests that to_dict has place datetime attributes as strings.
    def test_place_to_dict_datetime_attributes_type(self):
        place = Place()
        place_dict = place.to_dict()
        self.assertEqual(str, type(place_dict["id"]))
        self.assertEqual(str, type(place_dict["created_at"]))
        self.assertEqual(str, type(place_dict["updated_at"]))

    # Tests that to_dict returns a dictionary with
    #  place attributes(keys and values)
    def test_place_to_dict_valid_attr(self):
        dt = datetime.today()
        place = Place()
        place.id = "14151624"
        place.created_at = place.updated_at = dt
        placedict = {
            'id': '14151624',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(place.to_dict(), placedict)

    # Tests that to_dict returns a different place dictionary compared
    #  to the class __dict__ representation.
    def test_place_to_dict_with_class__dict__(self):
        place = Place()
        self.assertNotEqual(place.to_dict(), place.__dict__)

    # Tests that to_dict raises an exception when a None argument
    #  is passed in the place class.
    def test_place_to_dict_with_None_argument(self):
        place = Place()
        with self.assertRaises(TypeError):
            place.to_dict(None)


if __name__ == "__main__":
    unittest.main()

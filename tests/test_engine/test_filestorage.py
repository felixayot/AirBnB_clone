#!/usr/bin/python3
"""Unittests for models/engine/file_storage.py."""
import unittest
import json
import models
import os
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestFileStorage_Instantiantion_and_Methods(unittest.TestCase):
    """Defines unittests for FileStorage instantiation and methods."""

    def test_filestorage_instantiation(self):
        # Test instantiation with no arguments
        storage = FileStorage()
        self.assertIsInstance(storage, FileStorage)
        # Test instantiation with None argument
        storage = FileStorage(None)
        self.assertIsInstance(storage, FileStorage)
        # Test that __file_path is private
        with self.assertRaises(AttributeError):
            print(storage.__file_path)
        # Test that __objects is private
        with self.assertRaises(AttributeError):
            print(storage.__objects)
        # Test that a new instance of FileStorage can be created
        storage2 = FileStorage()
        self.assertIsInstance(storage2, FileStorage)

    # Tests that all method returns the dictionary __objects
    #  when it is not empty.
    def test_all_returns_dict_when_not_empty(self):
        storage = FileStorage()
        user = User()
        storage.new(user)
        self.assertEqual(storage.all(), {'User.' + user.id: user})

    # Tests that all method returns an empty dictionary
    #  when __objects is empty.
    def test_all_returns_empty_dict_when_empty(self):
        storage = FileStorage()
        self.assertEqual(storage.all(), {})

    # Tests that all method returns None when __objects is None.
    def test_all_returns_none_when_objects_is_none(self):
        storage = FileStorage()
        storage._FileStorage__objects = None
        self.assertIsNone(storage.all())

    # Tests that all method returns a dictionary of type dict.
    def test_all_returns_dict_of_expected_type(self):
        storage = FileStorage()
        self.assertIsInstance(storage.all(), dict)

    # Tests that all method returns a dictionary containing
    #  only instances of the expected classes.
    def test_all_returns_dict_of_expected_classes(self):
        storage = FileStorage()
        user = User()
        state = State()
        city = City()
        amenity = Amenity()
        place = Place()
        review = Review()
        storage.new(user)
        storage.new(state)
        storage.new(city)
        storage.new(amenity)
        storage.new(place)
        storage.new(review)
        objects = storage.all()
        for obj in objects.values():
            self.assertIn(obj.__class__.__name__,
                          ['User', 'State', 'City', 'Amenity',
                           'Place', 'Review'])

    # Tests that new adds a new object to __objects with correct key
    def test_new_adds_object_to_objects_with_correct_key(self):
        obj = User()
        self.storage.new(obj)
        key = 'User.' + obj.id
        self.assertIn(key, self.storage.all())
        self.assertEqual(self.storage.all()[key], obj)

    # Tests that new adds multiple objects of different classes to __objects
    def test_new_adds_multiple_objects_of_different_classes_to_objects(self):
        obj1 = User()
        obj2 = State()
        obj3 = City()
        self.storage.new(obj1)
        self.storage.new(obj2)
        self.storage.new(obj3)
        key1 = 'User.' + obj1.id
        key2 = 'State.' + obj2.id
        key3 = 'City.' + obj3.id
        self.assertIn(key1, self.storage.all())
        self.assertIn(key2, self.storage.all())
        self.assertIn(key3, self.storage.all())
        self.assertEqual(self.storage.all()[key1], obj1)
        self.assertEqual(self.storage.all()[key2], obj2)
        self.assertEqual(self.storage.all()[key3], obj3)

    # Tests that new does not add an object with no id attribute
    def test_new_does_not_add_object_with_no_id_attribute(self):
        obj = User()
        del obj.id
        self.storage.new(obj)
        key = 'User.' + obj.id
        self.assertNotIn(key, self.storage.all())

    # Tests that new does not add an object with id attribute of None
    def test_new_does_not_add_object_with_id_attribute_of_None(self):
        obj = User()
        obj.id = None
        self.storage.new(obj)
        key = 'User.' + str(obj.id)
        self.assertNotIn(key, self.storage.all())

    # Tests that an empty dictionary is saved to the
    #  JSON file when __objects is empty
    def test_save_empty_dict(self):
        storage = FileStorage()
        storage.save()
        with open(storage._FileStorage__file_path, 'r') as f:
            self.assertEqual(f.read(), '{}')

    # Tests that nothing is saved when __file_path does not exist
    def test_save_nonexistent_file(self):
        storage = FileStorage()
        storage._FileStorage__file_path = 'nonexistent.json'
        storage.save()
        self.assertFalse(os.path.exists(storage._FileStorage__file_path))

    # Tests that the JSON file is overwritten when it already exists
    def test_save_overwrite(self):
        storage = FileStorage()
        storage.save()
        with open(storage._FileStorage__file_path, 'r') as f:
            original_data = f.read()
        storage.save()
        with open(storage._FileStorage__file_path, 'r') as f:
            self.assertNotEqual(f.read(), original_data)

    # Tests that a non-empty dictionary is saved to the JSON file
    def test_save_nonempty_dict(self):
        storage = FileStorage()
        user = User()
        storage.new(user)
        storage.save()
        with open(storage._FileStorage__file_path, 'r') as f:
            self.assertNotEqual(f.read(), '{}')

    # Tests that save method raises a TypeError when called with None argument
    def test_save_with_none_argument(self):
        storage = FileStorage()
        with self.assertRaises(TypeError):
            storage.save(None)

    # Tests that reload method successfully deserializes
    #  objects when file exists
    def test_reload_file_exists(self):
        # create objects
        user = User()
        state = State()
        city = City()
        amenity = Amenity()
        place = Place()
        review = Review()
        # add objects to __objects
        self.storage.new(user)
        self.storage.new(state)
        self.storage.new(city)
        self.storage.new(amenity)
        self.storage.new(place)
        self.storage.new(review)
        # save objects to file
        self.storage.save()
        # clear __objects
        self.storage._FileStorage__objects = {}
        # reload objects from file
        self.storage.reload()
        # check if objects were reloaded
        self.assertEqual(len(self.storage.all()), 6)

    # Tests that reload method does not raise an exception
    #  when file does not exist
    def test_reload_file_does_not_exist(self):
        # clear __objects
        self.storage._FileStorage__objects = {}
        # reload objects from file
        self.storage.reload()
        # check if __objects is still empty
        self.assertEqual(len(self.storage.all()), 0)

    # Tests that reload method does not raise an exception when file is empty
    def test_reload_file_is_empty(self):
        # create an empty file
        with open(self.storage._FileStorage__file_path, 'w') as f:
            f.write('')
        # clear __objects
        self.storage._FileStorage__objects = {}
        # reload objects from file
        self.storage.reload()
        # check if __objects is still empty
        self.assertEqual(len(self.storage.all()), 0)

    # Tests that reload method does nothing when None is passed as argument
    def test_reload_none_argument(self):
        self.storage.reload(None)
        self.assertEqual(len(self.storage.all()), 0)


if __name__ == '__main__':
    unittest.main()

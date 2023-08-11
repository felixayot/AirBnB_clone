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

    # Test that __file_path is private
    def test_filestorage_file_path_is_private_attr(self):
        storage = FileStorage()
        with self.assertRaises(AttributeError):
            print(storage.__file_path)

    # Test that __objects is private
    def test_filestorage_objects_is_private_attr(self):
        storage = FileStorage()
        with self.assertRaises(AttributeError):
            print(storage.__objects)

    # Test that a new instance of FileStorage can be created
    def test_filestorage_subsequent_instantiation(self):
        storage2 = FileStorage()
        self.assertIsInstance(storage2, FileStorage)

    # Test instantiation with None argument
    def test_fileStorage_instantiation_with_None_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

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
                          ['BaseModel', 'User', 'State', 'City', 'Amenity',
                           'Place', 'Review'])

    # Tests that all raises an exception when a None argument is passed
    def test_all_with_None(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    # Tests that new adds a new object to __objects with correct key
    def test_new_adds_object_to_objects_with_correct_key(self):
        storage = FileStorage()
        obj = User()
        storage.new(obj)
        key = 'User.' + obj.id
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key], obj)

    # Tests that new adds multiple objects of different classes to __objects
    def test_new_adds_multiple_objects_of_different_classes_to_objects(self):
        obj1 = User()
        obj2 = State()
        obj3 = City()
        storage = FileStorage()
        storage.new(obj1)
        storage.new(obj2)
        storage.new(obj3)
        key1 = 'User.' + obj1.id
        key2 = 'State.' + obj2.id
        key3 = 'City.' + obj3.id
        self.assertIn(key1, storage.all())
        self.assertIn(key2, storage.all())
        self.assertIn(key3, storage.all())
        self.assertEqual(storage.all()[key1], obj1)
        self.assertEqual(storage.all()[key2], obj2)
        self.assertEqual(storage.all()[key3], obj3)

    # Tests that nothing is saved when __file_path does not exist
    def test_save_nonexistent_file(self):
        storage = FileStorage()
        storage._FileStorage__file_path = 'nonexistent.json'
        storage.save()
        self.assertFalse(os.path.exists(storage._FileStorage__file_path))

    # Tests that new raises an exception when a None argument is passed
    def test_new_with_None(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    # Tests that new raises an exception when any other argument is passed
    def test_new_with_arguments(self):
        with self.assertRaises(TypeError):
            models.storage.new(User(), any)

    # Tests that a non-empty dictionary is saved to the JSON file
    def test_save_nonempty_dict(self):
        storage = FileStorage()
        user = User()
        storage.new(user)
        storage.save()
        with open(storage._FileStorage__file_path, 'r') as f:
            self.assertNotEqual(f.read(), '{}')

    # Tests that save method raises a TypeError when called
    #  with None argument
    def test_save_with_none_argument(self):
        storage = FileStorage()
        with self.assertRaises(TypeError):
            storage.save(None)

    # Tests that reload expects no exception when there
    #  is no file to be deserialized.
    def test_reload_no_file(self):
        self.assertRaises(TypeError, models.storage.reload())

    # Tests that reload method raises an exception when None is passed
    #  as argument
    def test_reload_none_argument(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == '__main__':
    unittest.main()

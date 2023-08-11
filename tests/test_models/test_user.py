#!/usr/bin/python3
"""Defines unittests for models/user.py."""
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser_instantiation(unittest.TestCase):
    """Test cases for class user instantiation."""

    # Tests that a new User instance can be created.
    def test_user_instantiates(self):
        self.assertEqual(User, type(User()))

    # Tests that new user instance is stored in objects.
    def test_new_user_instance_stored_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    # Tests that user instance id is a public attribute.
    def test_user_id_is_public_str(self):
        self.assertEqual(str, type(User().id))

    # Tests that user creation time is public.
    def test_user_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    # Tests that user updated time is public attribute.
    def test_user_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    # Tests that user email is public attribute.
    def test_user_email_is_public_attr(self):
        self.assertEqual(str, type(User.email))

    # Tests that user password is public attribute.
    def test_user_password_is_public_attr(self):
        self.assertEqual(str, type(User.password))

    # Tests that user first name is public attribute.
    def test_user_first_name_is_public_attr(self):
        self.assertEqual(str, type(User.first_name))

    # Tests that user last name is public attribute.
    def test_user_last_name_is_public_attr(self):
        self.assertEqual(str, type(User.last_name))

    # Tests that users instantiate with different unique ids.
    def test_users_instantiated_unique_ids(self):
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    # Tests that two or more users are created at different times.
    def test_users_different_created_at(self):
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    # Tests that two or more users are updated at different times.
    def test_users_different_updated_at(self):
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    # Tests that user string representation can be output.
    def test_user_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = dt
        us_str = user.__str__()
        self.assertIn("[User] (123456)", us_str)
        self.assertIn("'id': '123456'", us_str)
        self.assertIn("'created_at': " + dt_repr, us_str)
        self.assertIn("'updated_at': " + dt_repr, us_str)

    # Tests that user doesn't save a None argument
    #  as value in the dictionary.
    def test_user_None_arg(self):
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    # Tests that user instantiates with kwargs.
    def test_user_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        user = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(user.id, "345")
        self.assertEqual(user.created_at, dt)
        self.assertEqual(user.updated_at, dt)

    # Tests that user raises an exception when None as a value in kwargs.
    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
    """Test cases for save method."""

    # Tests that updated user is saved at the current time.
    def test_user_updated_at_saved(self):
        user = User()
        sleep(0.05)
        first_updated_at = user.updated_at
        user.save()
        self.assertLess(first_updated_at, user.updated_at)

    # Tests that two or more user updates are saved at different times.
    def test_two_user_updates_saved(self):
        user = User()
        sleep(0.05)
        first_updated_at = user.updated_at
        user.save()
        second_updated_at = user.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        user.save()
        self.assertLess(second_updated_at, user.updated_at)

    # Tests that save user with a None argument raises an exception.
    def test_user_save_with_None_argument(self):
        user = User()
        with self.assertRaises(TypeError):
            user.save(None)

    # Tests that save user updates the __file_path(JSON file)
    #  in the file_storage.
    def test_user_save_updates_file(self):
        user = User()
        user.save()
        usid = "User." + user.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())


class TestUser_to_dict(unittest.TestCase):
    """Test cases for to_dict method of the User class."""

    # Tests that user instance is returned as a dictionary.
    def test_user_to_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    # Tests that to_dict contains correct user keys.
    def test_user_to_dict_keys(self):
        user = User()
        self.assertIn("id", user.to_dict())
        self.assertIn("created_at", user.to_dict())
        self.assertIn("updated_at", user.to_dict())
        self.assertIn("__class__", user.to_dict())

    # Tests that to_dict contains added user attributes
    def test_user_to_dict_added_attributes(self):
        user = User()
        user.middle_name = "Labille"
        user.my_number = 6
        self.assertEqual("Labille", user.middle_name)
        self.assertIn("my_number", user.to_dict())

    # Tests that to_dict has user datetime attributes as strings.
    def test_user_to_dict_datetime_attributes_type(self):
        user = User()
        us_dict = user.to_dict()
        self.assertEqual(str, type(us_dict["id"]))
        self.assertEqual(str, type(us_dict["created_at"]))
        self.assertEqual(str, type(us_dict["updated_at"]))

    # Tests that to_dict returns a dictionary with
    #  user attributes(keys and values)
    def test_user_to_dict_valid_attr(self):
        dt = datetime.today()
        user = User()
        user.id = "14151624"
        user.created_at = user.updated_at = dt
        userdict = {
            'id': '14151624',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(user.to_dict(), userdict)

    # Tests that to_dict returns a different user dictionary compared
    #  to the class __dict__ representation.
    def test_user_to_dict_with_class__dict__(self):
        user = User()
        self.assertNotEqual(user.to_dict(), user.__dict__)

    # Tests that to_dict raises an exception when a None argument
    #  is passed in the user class.
    def test_user_to_dict_with_None_argument(self):
        user = User()
        with self.assertRaises(TypeError):
            user.to_dict(None)


if __name__ == "__main__":
    unittest.main()

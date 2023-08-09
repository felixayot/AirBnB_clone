#!/usr/bin/python3
"""Defines unittests for all features of console.py."""
import os
import sys
import unittest
from models import storage
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from io import StringIO
from unittest.mock import patch


class TestHBNB_prompt_and_help(unittest.TestCase):
    """Test cases for console prompt and help."""

    # Tests that emptyline outputs nothing.
    def test_emptyline_no_args(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().emptyline()
        self.assertEqual(f.getvalue(), '')

    # Tests that calling emptyline method with a string containing both
    # whitespace and non-whitespace characters does not raise any exceptions.
    def test_emptyline_whitespace_and_non_whitespace_chars(self):
        with patch('sys.stdout', new=StringIO()) as f:
            try:
                HBNBCommand().emptyline()
            except IOError:
                self.fail("emptyline raised an exception unexpectedly!")

    # Tests that all methods in HBNBCommand have help documentation.
    def test_help_documentation(self):
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = HBNBCommand()
            for method_name in dir(cmd):
                if method_name.startswith('do_'):
                    with self.subTest(method_name=method_name):
                        method = getattr(cmd, method_name)
                        self.assertIsNotNone(method.__doc__,
                                             f'{method_name} \
                                                has no help documentation.')


class TestHBNB_create_command(unittest.TestCase):
    """Test cases for the create method of the console."""

    # Tests that do_create creates an instance of BaseModel
    def test_create_base_model_instance(self):
        self.maxDiff = None
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create BaseModel')
            output = f.getvalue().strip()
            obj_dict = storage.all()
            obj_id = output
            obj_key = 'BaseModel.' + obj_id
            self.assertTrue(obj_key in obj_dict.keys())
            self.assertTrue(isinstance(obj_dict[obj_key], BaseModel))

    # Tests that do_create creates an instance of a derived class
    def test_create_derived_class_instance(self):
        self.maxDiff = None
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create User')
            output = f.getvalue().strip()
            obj_dict = storage.all()
            obj_id = output
            obj_key = 'User.' + obj_id
            self.assertTrue(obj_key in obj_dict.keys())
            self.assertTrue(isinstance(obj_dict[obj_key], User))

    # Tests that do_create saves the instance to the JSON file
    def test_create_save_instance(self):
        self.maxDiff = None
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create State')
            output = f.getvalue().strip()
            obj_dict = storage.all()
            obj_id = output
            obj_key = 'State.' + obj_id
            with open('file.json', 'r') as f:
                file_content = f.read()
                self.assertTrue(obj_key in obj_dict.keys())
                self.assertTrue(obj_id in file_content)

    # Tests that do_create prints the id of the created instance
    def test_create_print_id(self):
        self.maxDiff = None
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create City')
            output = f.getvalue().strip()
            obj_dict = storage.all()
            obj_id = output
            obj_key = 'City.' + obj_id
            self.assertTrue(obj_key in obj_dict.keys())
            self.assertTrue(obj_id in output)

    # Tests that do_create handles no class name provided
    def test_create_no_class_name(self):
        self.maxDiff = None
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create')
            output = f.getvalue().strip()
            self.assertEqual(output, '** class name missing **')

    # Tests that an error message is printed when an invalid class name
    #  is provided as input to do_create method.
    def test_invalid_class_name(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create InvalidClassName')
            output = f.getvalue().strip()
            self.assertEqual(output, '** class doesn\'t exist **')

    # Tests that a syntax error message is printed when an invalid command
    #  is entered.
    def test_invalid_command(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('crete Ayot')
            output = f.getvalue().strip()
            self.assertEqual(output, '*** Unknown syntax: crete Ayot')


class TestHBNB_show_command(unittest.TestCase):
    """Test cases for the show method in the console."""

    # Tests that do_destroy deletes an instance of an existing class and id
    def test_destroy_existing_instance(self):
        obj = User()
        obj.save()
        obj_id = obj.id
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy User ' + obj_id)
            self.assertNotIn(obj, storage.all().values())

    # Tests that do_destroy fails to delete an instance of
    #  a non-existing class
    def test_destroy_non_existing_class(self):
        obj = User()
        obj.save()
        obj_id = obj.id
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy NonExistingClass ' + obj_id)
            self.assertIn(obj, storage.all().values())

    # Tests that do_destroy fails to delete an instance of
    #  an existing class with a non-existing id
    def test_destroy_non_existing_id(self):
        obj = User()
        obj.save()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy User NonExistingId')
            self.assertIn(obj, storage.all().values())

    # Tests that do_destroy fails to delete an instance of
    #  a class with missing class name
    def test_destroy_missing_class_name(self):
        expected = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(expected, f.getvalue().strip())

    # Tests that do_destroy fails to delete an instance
    #  of a class with missing id
    def test_destroy_missing_id(self):
        obj = User()
        obj.save()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('destroy User')
            self.assertIn(obj, storage.all().values())


class TestHBNB_all_command(unittest.TestCase):
    """Test cases for all method of the console."""

    # Tests that all instances are printed when
    #  no class is specified
    def test_all_no_class_specified(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create BaseModel')
            HBNBCommand().onecmd('create User')
            HBNBCommand().onecmd('create State')
            HBNBCommand().onecmd('create City')
            HBNBCommand().onecmd('create Amenity')
            HBNBCommand().onecmd('create Place')
            HBNBCommand().onecmd('create Review')
            HBNBCommand().onecmd('all')
            output = f.getvalue().strip()
            self.assertIn('[BaseModel]', output)
            self.assertIn('[User]', output)
            self.assertIn('[State]', output)
            self.assertIn('[City]', output)
            self.assertIn('[Amenity]', output)
            self.assertIn('[Place]', output)
            self.assertIn('[Review]', output)

    # Tests that only instances of specified class are
    #  printed when class is specified
    def test_all_class_specified(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('create BaseModel')
            HBNBCommand().onecmd('create BaseModel')
            HBNBCommand().onecmd('create BaseModel')
            HBNBCommand().onecmd('create User')
            HBNBCommand().onecmd('create User')
            HBNBCommand().onecmd('create State')
            HBNBCommand().onecmd('create City')
            HBNBCommand().onecmd('create Amenity')
            HBNBCommand().onecmd('create Place')
            HBNBCommand().onecmd('create Review')
            HBNBCommand().onecmd('BaseModel.all()')
            output = f.getvalue().strip()
            self.assertIn('[BaseModel]', output)
            self.assertNotIn('[User]', output)
            self.assertNotIn('[State]', output)
            self.assertNotIn('[City]', output)
            self.assertNotIn('[Amenity]', output)
            self.assertNotIn('[Place]', output)
            self.assertNotIn('[Review]', output)


class TestHBNB_update_command(unittest.TestCase):
    """Test cases for the update method of the console."""

    # Tests that an error message is printed when update is
    #  used without class.
    def test_update_missing_class(self):
        expected = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual(expected, f.getvalue().strip())

    # Tests that an error message is printed when update
    #  is used with a non-existant class.
    def test_update_invalid_class(self):
        expected = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("HighClass.update()"))
            self.assertEqual(expected, f.getvalue().strip())

    # Tests that an error message is printed when update
    #  is used without class id.
    def test_update_missing_id(self):
        expected = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update User"))
            self.assertEqual(expected, f.getvalue().strip())

    # Tests that an error message is printed when update is used
    #  with an invalid class id.
    def test_update_invalid_id(self):
        expected = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("update User existing-id "))
            self.assertEqual(expected, f.getvalue().strip())

    # Tests that an error message is printed when update is used
    # without the attribute name.
    def test_update_missing_attribute(self):
        expected = "** attribute name missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testId = f.getvalue().strip()
            testCmd = "update User {}".format(testId)
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(expected, f.getvalue().strip())

    # Tests that an error message is printed when update is used
    # without the value of attribute name.
    def test_update_missing_attr_value(self):
        expected = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            testId = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            testCmd = "update BaseModel {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(expected, f.getvalue().strip())

    # Tests that a valid dictionary is updated.
    def test_update_valid_dictionary(self):
        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            testId = f.getvalue().strip()
        testCmd = "BaseModel.update({}".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        testKeys = storage.all()["BaseModel.{}"
                                 .format(testId)].__dict__.keys()
        self.assertIn("attr_name", testKeys)


class TestHBNB_count_command(unittest.TestCase):
    """Test cases for count method for the console."""

    # Tests that the count of instances is retrieved
    #  for a valid class name
    def test_valid_class_name(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel')
            self.assertEqual(f.getvalue().strip(),
                             '*** Unknown syntax: BaseModel')

    # Tests that the count of instances is retrieved for
    #  a valid class name with spaces
    def test_valid_class_name_with_spaces(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('   BaseModel  ')
            self.assertEqual(f.getvalue().strip(),
                             '*** Unknown syntax: BaseModel')

    # Tests that 0 is returned for an invalid class name
    def test_invalid_class_name(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('InvalidClass')
            self.assertEqual(f.getvalue().strip(),
                             '*** Unknown syntax: InvalidClass')

    # Tests that 0 is returned for a class name with spaces
    def test_class_name_with_spaces(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('   Invalid Class  ')
            self.assertEqual(f.getvalue().strip(),
                             '*** Unknown syntax: Invalid Class')

    # Tests that 0 is returned for an empty string
    def test_empty_string(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('')
            self.assertEqual(f.getvalue().strip(), '')

    # Tests that 0 is returned for a class with no instances
    def test_class_with_no_instances(self):
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('Amenity')
            self.assertEqual(f.getvalue().strip(),
                             '*** Unknown syntax: Amenity')


class TestHBNB_quit_and_EOF(unittest.TestCase):
    """Test cases for quit and EOF methods."""

    # Tests that do_EOF returns True when EOF character is entered
    def test_EOF_returns_true_on_EOF_input(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().do_EOF(None))

    # Tests that do_quit method returns True
    def test_quit_method(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd('quit'))

    # Tests that do_EOF returns True when called with arguments
    def test_EOF_returns_true_with_arguments(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().do_EOF('some arguments'))

    # Tests that do_EOF returns True when Ctrl-D is invoked
    def test_EOF_returns_true_when_ctrl_d_invoked(self):
        with patch('sys.stdout', new=StringIO()) as f:
            h = HBNBCommand()
            self.assertTrue(h.do_EOF(None))


if __name__ == "__main__":
    unittest.main()

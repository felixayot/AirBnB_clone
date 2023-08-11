#!/usr/bin/python3
"""Defines unittests for models/state.py."""
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_instantiation(unittest.TestCase):
    """Test cases for class state instantiation."""

    # Tests that a new state instance can be created.
    def test_state_instantiates(self):
        self.assertEqual(State, type(State()))

    # Tests that new state instance is stored in objects.
    def test_new_state_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    # Tests that state instance id is a public attribute.
    def test_state_id_is_public_attr(self):
        self.assertEqual(str, type(State().id))

    # Tests that state creation time is public.
    def test_state_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    # Tests that state updated time is public attribute.
    def test_state_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    # Tests that state name is public attribute.
    def test_state_name_is_public_attr(self):
        self.assertEqual(str, type(State.name))

    # Tests that states instantiate with different unique ids.
    def test_states_instantiated_unique_ids(self):
        state1 = State()
        state2 = State()
        self.assertNotEqual(state1.id, state2.id)

    # Tests that two or more states are created at different times.
    def test_states_different_created_at(self):
        state1 = State()
        sleep(0.05)
        state2 = State()
        self.assertLess(state1.created_at, state2.created_at)

    # Tests that two or more states are updated at different times.
    def test_states_different_updated_at(self):
        state1 = State()
        sleep(0.05)
        state2 = State()
        self.assertLess(state1.updated_at, state2.updated_at)

    # Tests that state string representation can be output.
    def test_state_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        state = State()
        state.id = "14151624"
        state.created_at = state.updated_at = dt
        state_str = state.__str__()
        self.assertIn("[State] (14151624)", state_str)
        self.assertIn("'id': '14151624'", state_str)
        self.assertIn("'created_at': " + dt_repr, state_str)
        self.assertIn("'updated_at': " + dt_repr, state_str)

    # Tests that state doesn't save a None argument
    #  as value in the dictionary.
    def test_state_None_arg(self):
        state = State(None)
        self.assertNotIn(None, state.__dict__.values())

    # Tests that state instantiates with kwargs.
    def test_state_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        state = State(id="1017", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(state.id, "1017")
        self.assertEqual(state.created_at, dt)
        self.assertEqual(state.updated_at, dt)

    # Tests that state raises an exception when None as a value in kwargs.
    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Test cases for save method."""

    # Tests that updated state is saved at the current time.
    def test_state_updated_at_saved(self):
        state = State()
        sleep(0.05)
        first_updated_at = state.updated_at
        state.save()
        self.assertLess(first_updated_at, state.updated_at)

    # Tests that two or more state updates are saved at different times.
    def test_two_state_updates_saved(self):
        state = State()
        sleep(0.05)
        first_updated_at = state.updated_at
        state.save()
        second_updated_at = state.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        state.save()
        self.assertLess(second_updated_at, state.updated_at)

    # Tests that save state with a None argument raises an exception.
    def test_state_save_with_None_argument(self):
        state = State()
        with self.assertRaises(TypeError):
            state.save(None)

    # Tests that save state updates the __file_path(JSON file)
    #  in the file_storage.
    def test_state_save_updates_file(self):
        state = State()
        state.save()
        state_id = "State." + state.id
        with open("file.json", "r") as f:
            self.assertIn(state_id, f.read())


class TestState_to_dict(unittest.TestCase):
    """Test cases for to_dict method of the state class."""

    # Tests that state instance is returned as a dictionary.
    def test_state_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    # Tests that to_dict contains correct state keys.
    def test_state_to_dict_keys(self):
        state = State()
        self.assertIn("id", state.to_dict())
        self.assertIn("created_at", state.to_dict())
        self.assertIn("updated_at", state.to_dict())
        self.assertIn("__class__", state.to_dict())

    # Tests that to_dict contains added state attributes
    def test_state_to_dict_added_attributes(self):
        state = State()
        state.region = "Southside"
        state.year_established = 1788
        self.assertEqual("Southside", state.region)
        self.assertIn("year_established", state.to_dict())

    # Tests that to_dict has state datetime attributes as strings.
    def test_state_to_dict_datetime_attributes_type(self):
        state = State()
        state_dict = state.to_dict()
        self.assertEqual(str, type(state_dict["id"]))
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    # Tests that to_dict returns a dictionary with
    #  state attributes(keys and values)
    def test_state_to_dict_valid_attr(self):
        dt = datetime.today()
        state = State()
        state.id = "14151624"
        state.created_at = state.updated_at = dt
        statedict = {
            'id': '14151624',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(state.to_dict(), statedict)

    # Tests that to_dict returns a different state dictionary compared
    #  to the class __dict__ representation.
    def test_state_to_dict_with_class__dict__(self):
        state = State()
        self.assertNotEqual(state.to_dict(), state.__dict__)

    # Tests that to_dict raises an exception when a None argument
    #  is passed in the state class.
    def test_state_to_dict_with_None_argument(self):
        state = State()
        with self.assertRaises(TypeError):
            state.to_dict(None)


if __name__ == "__main__":
    unittest.main()

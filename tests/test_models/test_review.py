#!/usr/bin/python3
"""Defines unittests for models/review.py."""
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
    """Test cases for class review instantiation."""

    # Tests that a new review instance can be created.
    def test_review_instantiates(self):
        self.assertEqual(Review, type(Review()))

    # Tests that new review instance is stored in objects.
    def test_new_review_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    # Tests that review instance id is a public attribute.
    def test_review_id_is_public_attr(self):
        self.assertEqual(str, type(Review().id))

    # Tests that review creation time is public.
    def test_review_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    # Tests that review updated time is public attribute.
    def test_review_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    # Tests that review place_id is public attribute.
    def test_review_place_id_is_public_attr(self):
        self.assertEqual(str, type(Review.place_id))

    # Tests that review user id is public attribute.
    def test_review_user_id_is_public_attr(self):
        self.assertEqual(str, type(Review.user_id))

    # Tests that review text is public attribute.
    def test_review_text_is_public_attr(self):
        self.assertEqual(str, type(Review.text))

    # Tests that reviews instantiate with different unique ids.
    def test_reviews_instantiated_unique_ids(self):
        review1 = Review()
        review2 = Review()
        self.assertNotEqual(review1.id, review2.id)

    # Tests that two or more reviews are created at different times.
    def test_reviews_different_created_at(self):
        review1 = Review()
        sleep(0.05)
        review2 = Review()
        self.assertLess(review1.created_at, review2.created_at)

    # Tests that two or more reviews are updated at different times.
    def test_reviews_different_updated_at(self):
        review1 = Review()
        sleep(0.05)
        review2 = Review()
        self.assertLess(review1.updated_at, review2.updated_at)

    # Tests that review string representation can be output.
    def test_review_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        review = Review()
        review.id = "14151624"
        review.created_at = review.updated_at = dt
        rev_str = review.__str__()
        self.assertIn("[Review] (14151624)", rev_str)
        self.assertIn("'id': '14151624'", rev_str)
        self.assertIn("'created_at': " + dt_repr, rev_str)
        self.assertIn("'updated_at': " + dt_repr, rev_str)

    # Tests that review doesn't save a None argument
    #  as value in the dictionary.
    def test_review_None_arg(self):
        review = Review(None)
        self.assertNotIn(None, review.__dict__.values())

    # Tests that review instantiates with kwargs.
    def test_review_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        review = Review(id="1017", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(review.id, "1017")
        self.assertEqual(review.created_at, dt)
        self.assertEqual(review.updated_at, dt)

    # Tests that review raises an exception when None as a value in kwargs.
    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Test cases for save method."""

    # Tests that updated review is saved at the current time.
    def test_review_updated_at_saved(self):
        review = Review()
        sleep(0.05)
        first_updated_at = review.updated_at
        review.save()
        self.assertLess(first_updated_at, review.updated_at)

    # Tests that two or more review updates are saved at different times.
    def test_two_review_updates_saved(self):
        review = Review()
        sleep(0.05)
        first_updated_at = review.updated_at
        review.save()
        second_updated_at = review.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        review.save()
        self.assertLess(second_updated_at, review.updated_at)

    # Tests that save review with a None argument raises an exception.
    def test_review_save_with_None_argument(self):
        review = Review()
        with self.assertRaises(TypeError):
            review.save(None)

    # Tests that save review updates the __file_path(JSON file)
    #  in the file_storage.
    def test_review_save_updates_file(self):
        review = Review()
        review.save()
        revid = "Review." + review.id
        with open("file.json", "r") as f:
            self.assertIn(revid, f.read())


class TestReview_to_dict(unittest.TestCase):
    """Test cases for to_dict method of the review class."""

    # Tests that review instance is returned as a dictionary.
    def test_review_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    # Tests that to_dict contains correct review keys.
    def test_review_to_dict_keys(self):
        review = Review()
        self.assertIn("id", review.to_dict())
        self.assertIn("created_at", review.to_dict())
        self.assertIn("updated_at", review.to_dict())
        self.assertIn("__class__", review.to_dict())

    # Tests that to_dict contains added review attributes
    def test_review_to_dict_added_attributes(self):
        review = Review()
        review.rooms = "Bedroom"
        review.number_of_beds = 6
        self.assertEqual("Bedroom", review.rooms)
        self.assertIn("number_of_beds", review.to_dict())

    # Tests that to_dict has review datetime attributes as strings.
    def test_review_to_dict_datetime_attributes_type(self):
        review = Review()
        rev_dict = review.to_dict()
        self.assertEqual(str, type(rev_dict["id"]))
        self.assertEqual(str, type(rev_dict["created_at"]))
        self.assertEqual(str, type(rev_dict["updated_at"]))

    # Tests that to_dict returns a dictionary with
    #  review attributes(keys and values)
    def test_review_to_dict_valid_attr(self):
        dt = datetime.today()
        review = Review()
        review.id = "14151624"
        review.created_at = review.updated_at = dt
        reviewdict = {
            'id': '14151624',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(review.to_dict(), reviewdict)

    # Tests that to_dict returns a different review dictionary compared
    #  to the class __dict__ representation.
    def test_review_to_dict_with_class__dict__(self):
        review = Review()
        self.assertNotEqual(review.to_dict(), review.__dict__)

    # Tests that to_dict raises an exception when a None argument
    #  is passed in the review class.
    def test_review_to_dict_with_None_argument(self):
        review = Review()
        with self.assertRaises(TypeError):
            review.to_dict(None)


if __name__ == "__main__":
    unittest.main()

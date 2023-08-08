#!/usr/bin/python3
"""
This module defines the FileStorage class that implements file storage.
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
    Represents a file storage class that serializes instances
    to a JSON file and deserializes
    JSON file to instances.
    Attributes:
    __file_path(str): path to the JSON file.
    __objects(dict): stores all objects by <class name>.id
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        obj_cls_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(obj_cls_name, obj.id)] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        data = {}

        for key, value in FileStorage.__objects.items():
            data[key] = value.to_dict()

        with open(FileStorage.__file_path, "w") as f:
            json.dump(data, f)

    def reload(self):
        """Deserializes the JSON file to __objects only if
        __file_path exists."""
        class_dict = {
                "BaseModel": BaseModel,
                "User": User,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Place": Place,
                "Review": Review
                }
        obj = {}
        try:
            with open(FileStorage.__file_path, "r") as f:
                json_data = json.load(f)
                for key, value in json_data.items():
                    obj[key] = class_dict[value["__class__"]](**value)
                FileStorage.__objects = obj
        except FileNotFoundError:
            pass

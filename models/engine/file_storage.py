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
        obj_cls_name = obj.__class.__name__
        FileStorage.__objects["{}.{}".format(obj_cls_name, obj.id)] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        dict1 = FileStorage.__objects
        obj_dict = {obj: dict1[obj].to_dict() for obj in dict1.keys()}
        with open(FileStorage.__file_path, "w") as f_obj:
            json.dump(obj_dict, f_obj)

    def reload(self):
        """Deserializes the JSON file to __objects only if
        __file_path exists."""
        try:
            with open(FileStorage.__file_path) as f_obj:
                obj_dict = json.load(f_obj)
                for obj in obj_dict.values():
                    cls_name = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval(cls_name)(**obj))
        except FileNotFoundError:
            return

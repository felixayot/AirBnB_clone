#!/usr/bin/python3
"""
This is a module containing the baseclass defination for the AirBnB project
"""

from datetime import datetime
from uuid import uuid4


class BaseModel:
    """
     defines all common attributes/methods for other classes:
    """
    def __init__(self):
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """
        prints a customised representation of the current object
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
         updates the public instance attribute updated_at
         with the current datetime
        """

        self.updated_at = datetime.now()

    def to_dict(self):
        """
        returns a dictionary containing all keys/values
        of __dict__ of the instance
        """

        instance_dict = self.__dict__.copy()

        instance_dict.update({

            "__class__": self.__class__.__name__,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()

            })

        return instance_dict

#!/usr/bin/python3
"""
This is a module containing the baseclass defination for the AirBnB project
"""

from datetime import datetime
from uuid import uuid4


date_fmt = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """
     defines all common attributes/methods for other classes:
    """
    def __init__(self, *args, **kwargs):
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        else:
            str_created_at = kwargs["created_at"]
            str_updated_at = kwargs["updated_at"]

            created_at = datetime.strptime(str_created_at, date_fmt)
            updated_at = datetime.strptime(str_updated_at, date_fmt)

            kwargs["created_at"] = created_at
            kwargs["updated_at"] = updated_at

            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)

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

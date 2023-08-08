#!/usr/bin/python3
"""Module package for models. Contained here are modules
   for classes BaseModel, User, State, City, Amenity, Place and Review.
"""

from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()

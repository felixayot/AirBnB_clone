#!/usr/bin/python3
"""
class that inherits from the BaseModel
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    public attributes
    """
    place_id = ""
    user_id = ""
    text = ""

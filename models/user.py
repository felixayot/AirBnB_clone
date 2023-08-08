#!/usr/bin/python3
"""
class user that inherits from the BaseModel
"""
from models.base_model import BaseModel


class User(BaseModel):
    """
    public class attributes
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""

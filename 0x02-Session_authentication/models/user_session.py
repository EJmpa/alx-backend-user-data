#!/usr/bin/env python3
""" User Session module
"""
from models.base import Base


class UserSession(Base):
    """User Session class"""
    def __init__(self, *args: list, **kwargs: dict):
        """initializes an instance"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

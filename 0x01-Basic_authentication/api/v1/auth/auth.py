#!/usr/bin/env python3
"""
Module containing Auth class for authentication.
"""

from typing import List, TypeVar
from flask import request


class Auth:
    """
    Auth class serves as a template for authentication systems.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to check if authentication is required for a given path.

        Args:
            path (str): The path to check for authentication.
            excluded_paths (List[str]): List of paths excluded from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Method to get the authorization header from the request.

        Args:
            request: Flask request object.

        Returns:
            str: The authorization header or None if not present.
        """
        if request:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to get the current user based on the request.

        Args:
            request: Flask request object.

        Returns:
            TypeVar('User'): The current user or None.
        """
        return None

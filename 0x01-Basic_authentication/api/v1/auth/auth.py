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
            excluded_paths (List[str]): List of paths excluded from
            authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Add a trailing slash to path for comparison
        if path[-1] != '/':
            path += '/'

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Method to get the authorization header from the request.

        Args:
            request: Flask request object.

        Returns:
            str: The authorization header or None if not present.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to get the current user based on the request.

        Args:
            request: Flask request object.

        Returns:
            TypeVar('User'): The current user or None.
        """
        return None

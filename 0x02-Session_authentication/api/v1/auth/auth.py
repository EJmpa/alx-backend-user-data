#!/usr/bin/env python3
"""
Module containing Auth class for authentication.
"""

import os
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

        for ep in excluded_paths:
            if ep[-1] == '*':
                if path.startswith(ep[:-1]):
                    return False
            elif path == ep:
                return False

        return True

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

    def session_cookie(self, request=None):
        """
        Return the value of the cookie named _my_session_id from request.

        Args:
            request: Flask request object.

        Returns:
            str: Cookie value if found, None otherwise.
        """
        if request is None:
            return None

        # Use environment variable SESSION_NAME to define the name of d cookie
        cookie_name = os.getenv("SESSION_NAME", "_my_session_id")

        # Use .get() to access the cookie in the request cookies dictionary
        return request.cookies.get(cookie_name)

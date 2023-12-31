#!/usr/bin/env python3
"""
Module containing BasicAuth class for authentication.
"""

import base64
from typing import TypeVar
from models.user import User
from models.base import DATA
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class inherits from Auth.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Method to extract the Base64 part of the Authorization header for
        Basic Authentication.

        Args:
            authorization_header (str): The Authorization header string.

        Returns:
            str: The Base64 part of the Authorization header,
            or None if not valid.
        """
        if authorization_header is None or \
                not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        # Extract the Base64 part after "Basic "
        base64_part = authorization_header.split("Basic ")[1]

        return base64_part if base64_part else None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Method to decode a Base64 Authorization header.

        Args:
            base64_authorization_header (str): The Base64 Authorization header.

        Returns:
            str: The decoded value as a UTF-8 string, or None if not valid.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_bytes = base64_authorization_header
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('utf-8')
            return message
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Method to extract user email and password from the Base64
        decoded value.

        Args:
            decoded_base64_authorization_header (str): The Base64
            decoded Authorization header.

        Returns:
            tuple: The user email and password, or (None, None) if not valid.
        """
        if decoded_base64_authorization_header is None or \
                not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, pswd = decoded_base64_authorization_header.split(':', 1)

        return email, pswd

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Method to get the User instance based on email and password.

        Args:
            user_email (str): The user email.
            user_pwd (str): The user password.

        Returns:
            TypeVar('User'): The User instance if found, else None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the User instance for a request.

        Args:
            request: The Flask request object.

        Returns:
            User: The User instance, None if not found.
        """
        if request is None:
            return None
        header = self.authorization_header(request)
        if header is None:
            return None
        base64_header = self.extract_base64_authorization_header(header)
        if base64_header is None:
            return None
        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None
        credentials = self.extract_user_credentials(decoded_header)
        if credentials is None:
            return None
        user = self.user_object_from_credentials(*credentials)
        return user

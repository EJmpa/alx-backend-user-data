#!/usr/bin/env python3
"""
Module containing BasicAuth class for authentication.
"""

import base64
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

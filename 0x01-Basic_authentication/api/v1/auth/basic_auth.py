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

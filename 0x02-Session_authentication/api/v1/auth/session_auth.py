#!/usr/bin/env python3
"""
Module for SessionAuth
"""
import uuid
from typing import Optional
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session Authentication"""

    user_id_by_session_id = {}

    def create_session(self, user_id: Optional[str] = None) -> Optional[str]:
        """
        Create a Session ID for a user_id.

        Args:
            user_id (str): User ID.

        Returns:
            str: Session ID if successful, None otherwise.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID
        """
        if session_id is None or type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)

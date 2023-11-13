#!/usr/bin/env python3
"""
Session expieration authentication module for API
"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """session expiration authentication handling"""
    def __init__(self):
        """initiates instance"""
        value = os.getenv('SESSION_DURATION', None)
        if value:
            self.session_duration = int(value)
        else:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """creates a session for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dictionary = {
                'user_id': user_id,
                'created_at': datetime.now()
                }
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns user_id from a session_id"""
        if session_id is None or self.user_id_by_session_id.get(
                session_id) is None:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dictionary.get('user_id')

        created_at = session_dictionary.get('created_at')
        if created_at is None:
            return None

        expiration_date = created_at + timedelta(seconds=self.session_duration)
        if expiration_date < datetime.now():
            return None

        return session_dictionary.get('user_id')

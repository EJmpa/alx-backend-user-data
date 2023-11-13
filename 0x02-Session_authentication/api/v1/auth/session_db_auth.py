#!/usr/bin/env python3
"""
Module for SessionDBAuth
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class
    """
    def create_session(self, user_id=None):
        """
        Creates a Session ID and stores it in the database
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns a User ID by requesting UserSession
        in the database based on session_id
        """
        user_sessions = UserSession.search({'session_id': session_id})
        for user_session in user_sessions:
            delta = datetime.now() - user_session.created_at
            if delta.seconds < self.session_duration:
                return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on the
        Session ID from the request cookie
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_sessions = UserSession.search({'session_id': session_id})
        for user_session in user_sessions:
            user_session.remove()

        return True

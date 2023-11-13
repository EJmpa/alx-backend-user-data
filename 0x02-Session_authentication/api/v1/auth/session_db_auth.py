#!/usr/bin/env python3
"""
Session database authentication module for API
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """session db auth handling"""
    def create_session(self, user_id=None):
        """creates and stores new instance of UserSession and
        returns session id"""
        if user_id is None:
            return None
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        new_session = UserSession(session_id=session_id, user_id=user_id)
        new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the user id by requesting UserSession in the database"""
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_sessions = UserSession.search({'session_id': session_id})
        if user_sessions == []:
            return None
        user_session = user_sessions[0]
        if self.session_duration <= 0:
            return user_session.user_id
        created_at = user_session.created_at
        expiration_date = created_at + timedelta(seconds=self.session_duration)
        if expiration_date < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """destroys the usersession based on the session ID from request"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_sessions = UserSession.search({'session_id': session_id})
        if user_sessions == []:
            return False
        user_session = user_sessions[0]
        user_session.remove()
        return True
